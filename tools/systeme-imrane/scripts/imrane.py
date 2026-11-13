#!/usr/bin/env python3
"""Système Imrane portable command line (Python 3.11+, standard library)."""
from __future__ import annotations

import argparse
import getpass
import json
import math
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from contextlib import ExitStack, contextmanager, nullcontext
from pathlib import Path

from common import (ROOT, VERSION, atomic_write, digest, now, project_by_id,
                    read_json, registry, relative_path, resolve_project, runtime_dir,
                    slug, write_json, governance_lane)

MEMORY_FILES = ("CURRENT.md", "DECISIONS.md", "CONTEXT_INDEX.md", "PROJECT_CONTEXT.md")
EVENTS = ("SessionStart", "UserPromptSubmit", "PostToolUse", "Stop", "PreCompact")


def template(name, **values):
    text = (ROOT / "templates" / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


MANAGED_MANIFEST = ".imrane/managed.json"
MANAGED_LOCK = ".imrane/managed.lock"


def managed_target(workspace, rel):
    """Use the named file itself, without redirecting through another path."""
    try:
        target = relative_path(workspace, rel)
    except RuntimeError:
        raise ValueError(f"Invalid managed path: {rel}") from None
    if target != workspace / rel:
        raise ValueError(f"Linked managed path refused: {rel}")
    return target


def file_bytes(path):
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError(f"Expected a regular managed file: {path.name}")
        # POSIX nonblocking open also protects against a FIFO appearing after
        # lstat. Recheck the descriptor before reading bytes from it.
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
    except FileNotFoundError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError(f"Expected a regular managed file: {path.name}")
        with open(fd, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(fd)


@contextmanager
def managed_lock(workspace):
    lock = managed_target(workspace, MANAGED_LOCK)
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("Managed files are locked; retry after the active updater exits") from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as owner:
            owner.write(f"{os.getpid()}\n")
        yield
    finally:
        lock.unlink(missing_ok=True)


def require_unchanged(workspace, rel, expected):
    target = managed_target(workspace, rel)
    if file_bytes(target) != expected:
        raise ValueError(f"Concurrent change detected: {rel}. Review the plan and retry")
    return target


def stage_managed_file(target, body, cleanup):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".imrane-", dir=target.parent)
    staged = Path(name)
    cleanup.callback(staged.unlink, missing_ok=True)
    with os.fdopen(fd, "wb") as handle:
        handle.write(body)
    return staged


def commit_managed_file(workspace, rel, staged, expected):
    target = require_unchanged(workspace, rel, expected)
    if expected is not None:
        # The lock serializes Imrane writers. A process ignoring it can still
        # change the target between this final comparison and the OS replace.
        os.replace(staged, target)
        return
    try:
        # Publish a complete new file with create-if-absent semantics.
        if os.name == "nt":
            os.rename(staged, target)
        else:
            os.link(staged, target)
    except FileExistsError:
        raise ValueError(f"Concurrent change detected: {rel}. Review the plan and retry") from None


def apply_managed_plan(workspace, plan, manifest, manifest_before):
    completed = {}
    with ExitStack() as cleanup:
        staged = {}
        for rel, action, before, body in plan:
            if action != "unchanged":
                staged[rel] = stage_managed_file(managed_target(workspace, rel), body, cleanup)
            if action == "upgrade":
                source = require_unchanged(workspace, rel, before)
                backup = managed_target(workspace, f".imrane/backups/{now().replace(':', '-')}/{rel}")
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, backup)
                if file_bytes(backup) != before:
                    raise ValueError(f"Concurrent change detected during backup: {rel}. Review the plan and retry")

        # Check the whole batch after staging and backups, before publishing any
        # target. Recheck each target immediately before its own commit as well.
        require_unchanged(workspace, MANAGED_MANIFEST, manifest_before)
        for rel, _, before, _ in plan:
            require_unchanged(workspace, rel, before)
        try:
            for rel, action, before, body in plan:
                require_unchanged(workspace, MANAGED_MANIFEST, manifest_before)
                if action == "unchanged":
                    require_unchanged(workspace, rel, before)
                else:
                    commit_managed_file(workspace, rel, staged[rel], before)
                completed[rel] = digest(body)
        finally:
            # If a later conflict stops a running batch, record only successful
            # files so a subsequent run can recognize them and preserve edits.
            if completed:
                manifest["files"].update(completed)
                manifest["version"] = VERSION
                body = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                if body != manifest_before:
                    target = managed_target(workspace, MANAGED_MANIFEST)
                    staged_manifest = stage_managed_file(target, body, cleanup)
                    commit_managed_file(workspace, MANAGED_MANIFEST, staged_manifest, manifest_before)


def managed(workspace, files, apply=False, upgrade=False):
    """Plan, stage and revalidate managed files before applying replacements."""
    workspace = Path(workspace).resolve()
    with managed_lock(workspace) if apply else nullcontext():
        return plan_managed(workspace, files, apply, upgrade)


def plan_managed(workspace, files, apply, upgrade):
    manifest_before = file_bytes(managed_target(workspace, MANAGED_MANIFEST))
    manifest = (json.loads(manifest_before.decode("utf-8-sig")) if manifest_before is not None
                else {"version": VERSION, "files": {}})
    plan, conflicts = [], []
    seen = {workspace / MANAGED_MANIFEST, workspace / MANAGED_LOCK}
    for rel, content in files.items():
        target = managed_target(workspace, rel)
        if target in seen:
            raise ValueError(f"Duplicate or reserved managed target: {rel}")
        seen.add(target)
        encoded = content.encode("utf-8")
        existing = file_bytes(target)
        if existing == encoded:
            action = "unchanged"
        elif existing is None:
            action = "create"
        elif upgrade and digest(existing) == manifest["files"].get(rel):
            action = "upgrade"
        else:
            action = "CONFLICT"
            conflicts.append(rel)
        plan.append((rel, action, existing, encoded))
    actions = [(rel, action) for rel, action, _, _ in plan]
    for rel, action in actions:
        print(f"{action}: {rel}")
    if conflicts:
        raise ValueError("Existing files differ; preserved. Review conflicts before applying")
    if apply:
        apply_managed_plan(workspace, plan, manifest, manifest_before)
    return actions


def command_string(parts):
    # Native host shell, not a command assembled from project/user prompt content.
    if os.name == "nt":
        # Claude command hooks on Windows use a shell. Reject shell expansion tokens.
        if any(re.search(r'[%!&|<>^\r\n"]', str(part)) for part in parts):
            raise ValueError("Install path contains unsupported Windows shell characters")
        return " ".join('"' + str(part) + '"' for part in parts)
    return shlex.join(map(str, parts))


def host_files(workspace, prefix=""):
    workspace = Path(workspace).resolve()
    runner = workspace / "tools/systeme-imrane/scripts/hooks.py"
    hooks = {}
    for event in EVENTS:
        command = command_string([sys.executable, "-X", "utf8", runner, "--workspace", workspace, "--event", event])
        handler = {"type": "command", "command": command, "timeout": 300 if event == "PreCompact" else 10}
        if os.name == "nt":
            handler["commandWindows"] = command
        hooks[event] = [{"hooks": [handler]}]
    # Codex hooks.json and the feature flag are supported current local runtime surfaces.
    # Do not set trust, sandbox, approvals, auth or provider values.
    wrapper = ("---\nname: systeme-imrane\ndescription: Initialize, diagnose or maintain this isolated multi-project workspace and its Codex/Claude governance.\n---\n\n"
               f"Read the complete toolkit skill at `{workspace / 'tools/systeme-imrane/SKILL.md'}`. "
               "Use its scripts; do not reconstruct runtime or relax permissions.\n")
    claude_hooks = json.loads(json.dumps(hooks))
    for groups in claude_hooks.values():
        for group in groups:
            for handler in group["hooks"]:
                handler.pop("commandWindows", None)
    files = {
        prefix + ".codex/config.toml": "# Système Imrane: local hooks; trust is granted by the user in the host.\n[features]\nhooks = true\n",
        prefix + ".codex/hooks.json": json.dumps({"hooks": hooks}, indent=2) + "\n",
        prefix + ".claude/settings.json": json.dumps({"hooks": claude_hooks}, indent=2) + "\n",
        prefix + "CLAUDE.md": "Read AGENTS.md first. The same project boundaries, memory and governance apply to Claude Code.\n",
    }
    # Generated discovery wrappers, not independently edited skill copies.
    if not prefix:
        files[".claude/skills/systeme-imrane/SKILL.md"] = wrapper
        files[".agents/skills/systeme-imrane/SKILL.md"] = wrapper
    return files


def initialize(workspace, apply=False, upgrade=False):
    workspace = Path(workspace).resolve()
    files = {
        "AGENTS.md": template("workspace-AGENTS.md"),
        ".gitignore": template("workspace.gitignore"),
        ".graphifyignore": template("graphifyignore"),
        "secrets/.env.example": "# Private values belong in graphify.env (ignored), never in this example.\nGEMINI_API_KEY=\nOLLAMA_API_KEY=\n",
    }
    for name in MEMORY_FILES:
        rel = ".codex/memory/" + name
        if not (workspace / rel).exists():
            files[rel] = template("governance-" + name)
    initial = {
        ".codex/governance.json": {"version": 1, "id": "governance", "path": ".", "kind": "governance", "name": "Workspace governance", "graphify_enabled": True},
        ".codex/graphify-scope.json": {"include": ["AGENTS.md", ".codex/memory"], "exclude": []},
    }
    for rel, value in initial.items():
        if not (workspace / rel).exists():
            files[rel] = json.dumps(value, indent=2) + "\n"
    for rel, source in ((".codex/model-routing-policy.json", "models.json"), (".codex/graphify.json", "graphify.json"), (".codex/automatic-routing.json", "automatic-routing.json")):
        if not (workspace / rel).exists():
            files[rel] = (ROOT / "config" / source).read_text(encoding="utf-8")
    if not (workspace / ".codex/projects.json").exists():
        files[".codex/projects.json"] = json.dumps({"version": 1, "default_project": None, "projects": []}, indent=2) + "\n"
    for name in ("WORKSPACE_GOVERNANCE", "HANDOFF_POLICY", "SKILLS_POLICY", "PROJECT_LANE_BOOTSTRAP_CHECKLIST"):
        files[f"docs/governance/{name}.md"] = (ROOT / "templates" / f"{name}.md").read_text(encoding="utf-8")
    files.update(host_files(workspace))
    from distribution import installation_files
    files.update(installation_files(ROOT))
    managed(workspace, files, apply, upgrade)


def project_add(args):
    workspace = Path(args.workspace).resolve()
    data = registry(workspace)
    slug(args.id)
    if args.id == "governance":
        raise ValueError("The governance identity is reserved for the workspace root")
    if any(p["id"] == args.id for p in data["projects"]):
        p = project_by_id(workspace, args.id)
        if p["path"] != args.path or p["name"] != args.name:
            raise ValueError("Project id already registered with different settings")
        if args.git_init:
            path = relative_path(workspace, p["path"])
            if not (path / ".git").exists():
                if args.apply:
                    subprocess.run(["git", "init", "-b", "codex/bootstrap", str(path)], check=True)
                else:
                    print("PLAN: repair missing independent Git repository")
        if getattr(args, "set_default", False) and data.get("default_project") != args.id:
            print("UPDATE: explicitly selected default project")
            if args.apply:
                data["default_project"] = args.id
                write_json(workspace / ".codex/projects.json", data)
        print("UNCHANGED: registered project")
        return
    path = relative_path(workspace, args.path)
    first = path.relative_to(workspace).parts[0].casefold() if path != workspace else ""
    if path == workspace or first.startswith(".") or first in {"tools", "secrets", "tmp", "docs", "config", "graphify-out"}:
        raise ValueError("Choose an independent project folder, not governance/runtime")
    if any(str(relative_path(workspace, p["path"])).casefold() == str(path).casefold() for p in data["projects"]):
        raise ValueError("Project path already registered")
    prefix = path.relative_to(workspace).as_posix() + "/"
    files = {
        prefix + "AGENTS.md": template("project-AGENTS.md", project=args.name, project_id=args.id),
        prefix + ".gitignore": template("project.gitignore"),
        prefix + ".graphifyignore": template("graphifyignore"),
        prefix + ".codex/graphify-scope.json": json.dumps({"include": ["AGENTS.md", "src", "docs", ".codex/memory"], "exclude": []}, indent=2) + "\n",
    }
    for name in MEMORY_FILES:
        files[prefix + ".codex/memory/" + name] = template(name, project=args.name)
    files.update(host_files(workspace, prefix))
    # Normal governance edits do not reset project/runtime state on reinstall.
    managed(workspace, files, args.apply)
    if args.apply:
        data["projects"].append({"id": args.id, "name": args.name, "path": path.relative_to(workspace).as_posix(), "graphify_enabled": True})
        if getattr(args, "set_default", False):
            data["default_project"] = args.id
        write_json(workspace / ".codex/projects.json", data)
        if args.git_init:
            if (path / ".git").exists():
                print("UNCHANGED: Git repository exists")
            else:
                subprocess.run(["git", "init", "-b", "codex/bootstrap", str(path)], check=True)
    elif args.git_init:
        print("PLAN: independent Git repository (no commit or publication)")


def snapshot(workspace, project_id, reason="manual"):
    project = project_by_id(workspace, project_id)
    path = relative_path(workspace, project["path"])
    lane = runtime_dir(workspace, project_id)
    # Snapshot canonical memory verbatim locally. This is private, ignored and never injected whole.
    memory, missing, errors = {}, [], {}
    for name in MEMORY_FILES:
        source = path / ".codex/memory" / name
        if source.is_symlink() or any(parent.is_symlink() for parent in source.parents if parent.is_relative_to(path)):
            errors[name] = "UnsafePath"
            continue
        if not source.is_file():
            missing.append(name)
            continue
        try:
            memory[name] = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors[name] = type(exc).__name__
    try:
        graph = read_json(lane / "graphify-state.json", {"status": "not-built"})
    except (ValueError, OSError) as exc:
        graph = {"status": "error", "error": type(exc).__name__}
    data = {"schema": 2, "project_id": project_id, "at": now(), "reason": reason,
            "memory": memory, "graphify": graph, "complete": not missing and not errors,
            "missing": missing, "errors": errors,
            "completeness": {"expected": len(MEMORY_FILES), "saved": len(memory), "status": "incomplete" if missing or errors else "complete"}}
    name = data["at"].replace(":", "-") + ".json"
    write_json(lane / "snapshots" / name, data, private=True)
    write_json(lane / "latest-snapshot.json", data, private=True)
    return data


def dependency_status(profile, workspace=None):
    from dependencies import inspect_dependencies
    return inspect_dependencies(profile, workspace)


def is_imrane_hook(command, workspace, event):
    """Inspect the supported direct Python command without executing it."""
    try:
        args = shlex.split(command, posix=os.name != "nt")
        if os.name == "nt":
            args = [arg[1:-1] if arg.startswith('"') and arg.endswith('"') else arg for arg in args]
        if len(args) < 6:
            return False
        executable, runner = args[0], args[-5]
        flags = args[1:-5]
        options = dict(zip(args[-4::2], args[-3::2]))
        if options.keys() != {"--workspace", "--event"} or options["--event"] != event:
            return False
        # Keep the command a direct invocation. -c, -m and shell prefixes can
        # change what runs even if the expected runner appears in an argument.
        if "-X" in flags:
            index = flags.index("-X")
            if flags[index:index + 2] != ["-X", "utf8"]:
                return False
            del flags[index:index + 2]
        if any(flag not in ("-B", "-u", "-Xutf8") for flag in flags):
            return False
        python = Path(executable)
        found_python = str(python) if python.is_absolute() and python.is_file() else shutil.which(executable)
        if not found_python:
            return False
        if (not re.fullmatch(r"(?:(?:python|pypy)(?:\d+(?:\.\d+)?)?t?|py)(?:\.exe)?", python.name, re.I)
                and Path(found_python).resolve() != Path(sys.executable).resolve()):
            return False
        expected = workspace / "tools/systeme-imrane/scripts/hooks.py"
        return (Path(runner).is_absolute() and Path(runner).resolve() == expected
                and expected.is_file() and Path(options["--workspace"]).is_absolute()
                and Path(options["--workspace"]).resolve() == workspace)
    except (OSError, RuntimeError, ValueError):
        return False


def hook_event_issue(groups, workspace, event, codex):
    if not isinstance(groups, list) or not groups:
        return "missing or empty hook groups"
    expected = False
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("matcher", ""), str):
            return "invalid hook group"
        handlers = group.get("hooks")
        if not isinstance(handlers, list) or not handlers:
            return "invalid or empty hook handlers"
        for handler in handlers:
            kind = handler.get("type") if isinstance(handler, dict) else None
            if not isinstance(kind, str) or not kind.strip():
                return "invalid hook handler type"
            timeout = handler.get("timeout", 1)
            if (type(timeout) not in (int, float) or timeout <= 0
                    or (isinstance(timeout, float) and not math.isfinite(timeout))):
                return "invalid hook timeout"
            if kind != "command":
                continue
            command = handler.get("command")
            windows = handler.get("commandWindows", command) if codex else command
            if any(not isinstance(value, str) or not value.strip() for value in (command, windows)):
                return "missing or invalid hook command"
            active_command = windows if os.name == "nt" else command
            if not group.get("matcher") and is_imrane_hook(active_command, workspace, event):
                expected = True
    return None if expected else "missing unfiltered Système Imrane command for this workspace and event"


def reject_json_constant(value):
    raise ValueError("Non-JSON numeric constant")


def check_scope_hooks(workspace, path, scope, errors):
    for rel in (".codex/config.toml", ".codex/hooks.json", ".claude/settings.json"):
        label = f"{scope}: {rel}"
        target = path / rel
        try:
            if target.resolve() != target:
                errors.append(f"{label}: linked configuration path refused")
                continue
            if not stat.S_ISREG(target.stat().st_mode):
                errors.append(f"{label}: expected a regular configuration file")
                continue
            source = target.read_text(encoding="utf-8-sig")
            settings = (tomllib.loads(source) if target.suffix == ".toml"
                        else json.loads(source, parse_constant=reject_json_constant))
        except FileNotFoundError:
            errors.append(f"{label}: missing file")
            continue
        except (OSError, RuntimeError, ValueError):
            # Parse exceptions can quote user config. Report only scoped labels.
            errors.append(f"{label}: unreadable or invalid {'TOML' if target.suffix == '.toml' else 'JSON'}")
            continue
        if not isinstance(settings, dict):
            errors.append(f"{label}: expected a configuration object")
            continue
        if target.suffix == ".toml":
            features = settings.get("features")
            if not isinstance(features, dict) or features.get("hooks") is not True:
                errors.append(f"{label}: expected features.hooks = true")
            continue
        if rel == ".claude/settings.json" and settings.get("disableAllHooks") is True:
            errors.append(f"{label}: hooks are disabled")
        hooks = settings.get("hooks")
        if not isinstance(hooks, dict):
            errors.append(f"{label}: missing or invalid hooks object")
            continue
        for event in EVENTS:
            issue = hook_event_issue(hooks.get(event), workspace, event, rel == ".codex/hooks.json")
            if issue:
                errors.append(f"{label}: {event}: {issue}")


def check_workspace(workspace):
    workspace = Path(workspace).resolve()
    data = registry(workspace)
    errors = []
    governance = governance_lane(workspace)
    for project in data["projects"] + ([governance] if governance else []):
        path = relative_path(workspace, project["path"])
        for rel in ("AGENTS.md", "CLAUDE.md", ".graphifyignore", ".codex/graphify-scope.json"):
            if not (path / rel).is_file():
                errors.append(f"{project['id']}: missing {rel}")
        for rel in MEMORY_FILES:
            if not (path / ".codex/memory" / rel).is_file():
                errors.append(f"{project['id']}: missing {rel}")
        check_scope_hooks(workspace, path, project["id"], errors)
        state = read_json(runtime_dir(workspace, project["id"]) / "graphify-state.json", {})
        print(f"{project['id']}: graphify={state.get('status', 'not-built')}")
    if not governance:
        check_scope_hooks(workspace, workspace, "root", errors)
    print(json.dumps({"projects": len(data["projects"]), "governance": bool(governance), "errors": errors}, ensure_ascii=False))
    return 1 if errors else 0


def configure_secrets(workspace):
    registry(workspace)
    if not sys.stdin.isatty():
        raise ValueError("Use your own interactive terminal; secrets are not accepted through chat/arguments")
    path = Path(workspace) / "secrets/graphify.env"
    if path.exists():
        raise ValueError("Credential file exists; edit it privately rather than overwrite it")
    values = {name: getpass.getpass(name + " (empty to skip): ").strip()
              for name in ("GEMINI_API_KEY", "OLLAMA_API_KEY")}
    if any("\n" in value or "\r" in value for value in values.values()):
        raise ValueError("Keys must be single line")
    content = "".join(f"{key}={value}\n" for key, value in values.items() if value)
    if os.name == "nt":
        # Create an empty file, restrict ACL by authenticated SID, then write secret
        # content without replacing the protected inode/ACL with an inherited temp file.
        atomic_write(path, "", private=True)
        try:
            identity = subprocess.run(["whoami.exe", "/user", "/fo", "csv", "/nh"], capture_output=True, text=True, check=True)
            match = re.search(r"S-\d-(?:\d+-)+\d+", identity.stdout)
            if not match:
                raise ValueError("Authenticated SID unavailable")
            subprocess.run(["icacls.exe", str(path), "/inheritance:r", "/grant:r", f"*{match.group(0)}:(F)"], capture_output=True, check=True)
            with path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            path.unlink(missing_ok=True)
            raise ValueError("Could not protect credentials; no secret file retained") from None
    else:
        atomic_write(path, content, private=True)
    print("Credentials saved privately; values not displayed. Configure provider models before indexing.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "project-add", "select", "check", "snapshot", "secrets", "doctor", "deps"):
        p = sub.add_parser(name)
        p.add_argument("--workspace", default=str(Path.cwd()))
        if name in ("init", "project-add", "deps"):
            p.add_argument("--apply", action="store_true", help="Explicitly execute the displayed plan")
        if name == "init":
            p.add_argument("--upgrade", action="store_true")
        if name in ("project-add", "select", "snapshot"):
            p.add_argument("--id", required=True)
        if name == "project-add":
            p.add_argument("--path", required=True)
            p.add_argument("--name", required=True)
            p.add_argument("--git-init", action="store_true")
        if name in ("doctor", "deps"):
            p.add_argument("--profile", choices=("core", "complete"), default="core")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            initialize(args.workspace, args.apply, args.upgrade)
        elif args.command == "project-add":
            project_add(args)
        elif args.command == "select":
            project_by_id(args.workspace, args.id)
            write_json(Path(args.workspace) / "tmp/codex-session/ACTIVE_PROJECT.json", {"project_id": args.id})
            print("Selected " + args.id)
        elif args.command == "snapshot":
            result = snapshot(args.workspace, args.id)
            print("Snapshot saved: " + result["project_id"])
        elif args.command == "check":
            return check_workspace(args.workspace)
        elif args.command == "secrets":
            configure_secrets(args.workspace)
        elif args.command == "doctor":
            rows = dependency_status(args.profile, args.workspace)
            print(json.dumps(rows, indent=2))
            return 1 if any(r["status"] != "ok" for r in rows) else 0
        elif args.command == "deps":
            from dependencies import install_dependencies
            return install_dependencies(args.workspace, args.profile, args.apply)
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
