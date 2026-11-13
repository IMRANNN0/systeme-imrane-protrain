#!/usr/bin/env python3
"""Install pinned reviewed skill sources, retain licenses and do not execute them."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from common import ROOT, digest, inside, read_json, registry, relative_path, write_json


def tree_hash(path):
    import hashlib
    h = hashlib.sha256()
    for file in sorted(Path(path).rglob("*")):
        if file.is_symlink():
            raise ValueError("Symlinks are not allowed in imported skill contents")
        if file.is_file():
            h.update(file.relative_to(path).as_posix().encode() + b"\0" + file.read_bytes())
    return h.hexdigest()


def adapt_paths(staged, spec, canonical):
    """Deterministic overlay for upstream paths that assume a plugin checkout."""
    entry = staged / "SKILL.md"
    text = entry.read_text(encoding="utf-8-sig")
    changes = []
    plugin_prefix = "${CLAUDE_PLUGIN_ROOT}/" + spec.get("path", "")
    for old in (plugin_prefix, "${CLAUDE_SKILL_DIR}"):
        if old and old in text:
            text = text.replace(old, canonical.as_posix())
            changes.append(old)
    if changes:
        entry.write_text(text, encoding="utf-8")
        (staged / "IMRANE_OVERLAY.md").write_text(
            "Generated portable-paths-v1 overlay. Upstream instructions otherwise unchanged.\n"
            "Source: " + spec.get("url", "official package") + " @ " + spec.get("commit", "pinned package") + "\n"
            "Rebound plugin-root/skill-dir paths to this canonical local skill directory. Do not edit mirrors.\n", encoding="utf-8")


def unpack_skill(archive, spec, destination):
    """Read a single allowed subtree, with zip-slip/link/size guards."""
    destination = Path(destination)
    total = 0
    with zipfile.ZipFile(archive) as package:
        entries = package.infolist()
        prefixes = {PurePosixPath(info.filename).parts[0] for info in entries if PurePosixPath(info.filename).parts}
        if len(prefixes) != 1:
            raise ValueError("Unexpected GitHub archive roots")
        prefix = next(iter(prefixes))
        scope = PurePosixPath(spec["path"])
        for info in entries:
            parts = PurePosixPath(info.filename)
            if parts.is_absolute() or ".." in parts.parts or "\\" in info.filename:
                raise ValueError("Unsafe archive path")
            relative = PurePosixPath(*parts.parts[1:])
            is_license = relative.name.upper().startswith(("LICENSE", "NOTICE", "COPYING")) and len(relative.parts) == 1
            if spec["path"] != ".":
                if relative.is_relative_to(scope):
                    relative = relative.relative_to(scope)
                elif is_license:
                    relative = PurePosixPath("upstream-license") / relative
                else:
                    continue
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError("Archive symlink rejected")
            if not relative.parts or info.is_dir():
                continue
            if any(p in (".git", "node_modules", ".env", "__pycache__") for p in relative.parts):
                continue
            total += info.file_size
            if info.file_size > 10_000_000 or total > 60_000_000:
                raise ValueError("Skill archive exceeds reviewed size budget")
            target = relative_path(destination, str(relative))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(package.read(info))
    if not (destination / "SKILL.md").is_file():
        raise ValueError("Missing upstream SKILL.md")


def expose(source, destination, mirror_manifest):
    source, destination = Path(source), Path(destination)
    if destination.is_symlink():
        if destination.resolve() != source.resolve():
            raise ValueError("Existing skill link points elsewhere; preserved")
        return
    if destination.exists():
        expected = mirror_manifest.get(str(destination))
        if not expected or tree_hash(destination) != expected:
            raise ValueError("User-edited or unmanaged skill mirror; preserved")
        if tree_hash(source) == expected:
            return
        # Generated mirror is owned and unchanged, but upgrades remain explicit/manual.
        raise ValueError("Skill mirror update needed; review and remove this generated mirror before reinstall")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination.symlink_to(source.resolve(), target_is_directory=True)
    except OSError:
        shutil.copytree(source, destination)
        mirror_manifest[str(destination)] = tree_hash(destination)


def install(workspace, specs, apply=False):
    workspace = Path(workspace).resolve()
    data = registry(workspace) if apply else {"projects": []}
    state_path = workspace / ".imrane/skills-installed.json"
    state = read_json(state_path, {"skills": {}, "mirrors": {}})
    skipped = []
    for spec in specs:
        print(f"{spec['status']}: {spec['name']}" + (" @ " + spec["commit"][:12] if spec.get("commit") else ""))
        if spec["status"] not in ("github", "package"):
            skipped.append(spec["name"])
    if not apply:
        return 0
    with tempfile.TemporaryDirectory(prefix="imrane-skills-") as tmp:
        archives = {}
        for spec in specs:
            if spec["status"] not in ("github", "package"):
                continue
            source = relative_path(workspace, ".agents/skills/" + spec["name"])
            owned = state["skills"].get(spec["name"])
            if source.exists():
                if not owned or tree_hash(source) != owned.get("hash") or owned.get("commit") != spec.get("commit"):
                    raise ValueError("Unmanaged/modified/different-version skill preserved: " + spec["name"])
            else:
                staged = Path(tmp) / ("skill-" + spec["name"])
                staged.mkdir()
                if spec["status"] == "package":
                    if spec["name"] == "graphify":
                        # No import-time side effects in this process; read installed official package data.
                        from dependencies import venv_python
                        command = [str(venv_python(workspace)), str(ROOT / "scripts/package_skill.py"), "graphify"]
                        result = subprocess.run(command, check=True, capture_output=True)
                        package = json.loads(result.stdout.decode("utf-8"))
                        (staged / "SKILL.md").write_text(package["skill"], encoding="utf-8")
                        (staged / "LICENSE").write_text(package["license"], encoding="utf-8")
                        (staged / "PROVENANCE.md").write_text("Official graphifyy==0.8.13 package data. License MIT; see isolated venv dist-info licenses.\n")
                    elif spec["name"] == "canonry":
                        # Canonry distributes a SKILL.md in its pinned npm package; locate it, do not fabricate one.
                        package_root = workspace / ".imrane/npm/node_modules/@canonry/canonry"
                        candidates = list(package_root.rglob("SKILL.md"))
                        if len(candidates) != 1:
                            print("MANUAL: Canonry package skill path ambiguous; use its documented installer")
                            skipped.append("canonry")
                            continue
                        shutil.copytree(candidates[0].parent, staged, dirs_exist_ok=True)
                    else:
                        raise ValueError("Unsupported package skill")
                else:
                    key = spec["repo"] + "@" + spec["commit"]
                    if key not in archives:
                        archive = Path(tmp) / (str(len(archives)) + ".zip")
                        with archive.open("wb") as output:
                            subprocess.run(["gh", "api", f"repos/{spec['repo']}/zipball/{spec['commit']}"], stdout=output, stderr=subprocess.PIPE, check=True)
                        if archive.stat().st_size > 100_000_000:
                            raise ValueError("Repository archive exceeds budget")
                        archives[key] = archive
                    unpack_skill(archives[key], spec, staged)
                adapt_paths(staged, spec, source)
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(staged, source)
                state["skills"][spec["name"]] = {"hash": tree_hash(source), "commit": spec.get("commit"), "repo": spec.get("repo"), "status": spec["status"]}
                write_json(state_path, state, private=True)
            for base in [workspace, *[relative_path(workspace, p["path"]) for p in data["projects"]]]:
                expose(source, base / ".claude/skills" / spec["name"], state["mirrors"])
                if base != workspace:
                    expose(source, base / ".agents/skills" / spec["name"], state["mirrors"])
                write_json(state_path, state, private=True)
    if skipped:
        print("NOT INSTALLED (visible provenance/manual requirements): " + ", ".join(skipped))
        return 1
    print("SKILLS_INSTALLED_OK")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("list", "install"))
    p.add_argument("--workspace", default=str(Path.cwd()))
    p.add_argument("--all", action="store_true")
    p.add_argument("--name", action="append", default=[])
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    try:
        specs = read_json(ROOT / "config/skills-lock.json")["skills"]
        if args.command == "list":
            print(json.dumps(specs, indent=2))
            return 0
        if not args.all and not args.name:
            raise ValueError("Choose --all or --name explicitly")
        if set(args.name) - {s["name"] for s in specs}:
            raise ValueError("Unknown skill name")
        return install(args.workspace, specs if args.all else [s for s in specs if s["name"] in args.name], args.apply)
    except (ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print("SKILL_INSTALL_ERROR: " + (str(exc) if isinstance(exc, ValueError) else type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
