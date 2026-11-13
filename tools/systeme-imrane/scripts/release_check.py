#!/usr/bin/env python3
"""Fail-closed checks for this distribution, not a claim about a user's projects."""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path

from common import ROOT, read_json

REQUIRED = ["SKILL.md", "README.md", "SECURITY.md", "LICENSE", "NOTICE.md", "agents/openai.yaml",
            "bootstrap.ps1", "bootstrap.sh", "config/skills-lock.json", "config/npm-tools-lock.json",
            "config/plugin-catalogue.json", "config/dependencies.json", "config/graphify.json", "config/models.json",
            "config/codex-sol-luna-6.json", "scripts/models.py", "scripts/routing.py"]
DOCS = ["INSTALLATION", "COMMANDS", "ARCHITECTURE", "GRAPHIFY", "SKILLS", "PLUGINS", "MAINTENANCE", "VERIFICATION", "MODEL_ROUTING"]


def audit(root=ROOT):
    root = Path(root)
    errors = []
    required = REQUIRED + [f"docs/{name}.md" for name in DOCS]
    for rel in required:
        if not (root / rel).is_file():
            errors.append("missing " + rel)
    files = []
    for directory, folders, names in os.walk(root):
        folders[:] = [name for name in folders if name not in {".git", ".imrane", "__pycache__", "node_modules", ".venv"}]
        files.extend(Path(directory) / name for name in names)
    for file in files:
        rel = file.relative_to(root).as_posix()
        if file.is_symlink():
            errors.append("distribution symlink " + rel)
            continue
        if file.suffix in {".pyc", ".key", ".mp4", ".png", ".zip"} or file.name in {"graphify.env", "auth.json", "settings.local.json"}:
            errors.append("private/generated artifact " + rel)
        if file.stat().st_size > 2_000_000:
            errors.append("unexpectedly large distribution file " + rel)
            continue
        text = file.read_text(encoding="utf-8")
        if re.search(r"(?i)(?:[A-Z]:[\\/]Users[\\/]|/Users/|/home/)[\w.-]+[\\/]", text):
            errors.append("personal absolute path " + rel)
        if re.search(r"AIza[0-9A-Za-z_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|sk-proj-[A-Za-z0-9_-]{30,}", text):
            errors.append("possible live credential " + rel)
        if file.suffix == ".py":
            try:
                ast.parse(text)
            except SyntaxError:
                errors.append("invalid Python " + rel)
        if file.suffix == ".json":
            try:
                json.loads(text)
            except ValueError:
                errors.append("invalid JSON " + rel)
        if file.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")) or "<" in target:
                    continue
                path = (file.parent / target.split("#")[0]).resolve()
                if not path.is_relative_to(root.resolve()) or not path.exists():
                    errors.append(f"broken/outside documentation link {rel}: {target}")
    lock = read_json(root / "config/skills-lock.json", {})
    entries = lock.get("skills", [])
    if len(entries) != lock.get("inventory_count") or not entries:
        errors.append("catalogue coverage count mismatch")
    names = [s.get("name") for s in entries]
    if len(names) != len(set(names)):
        errors.append("duplicate skill name")
    for spec in entries:
        if spec.get("status") not in ("github", "package", "unresolved"):
            errors.append("unknown skill status")
        if spec.get("status") in ("github", "package"):
            if not re.fullmatch(r"[0-9a-f]{40}", spec.get("commit", "")) or not spec.get("license"):
                errors.append("unpinned/unlicensed source " + spec["name"])
        if spec.get("status") == "github" and not spec.get("path"):
            errors.append("missing skill path")
        if not spec.get("reason"):
            errors.append("unexplained catalogue status")
    for spec in read_json(root / "config/npm-tools-lock.json", {}).get("packages", []):
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?", spec.get("version", "")):
            errors.append("unlocked npm version")
    if not (root / "SKILL.md").read_text(encoding="utf-8").startswith("---\nname: systeme-imrane\n"):
        errors.append("invalid skill entrypoint")
    inventory = read_json(root / "config/codex-plugins-observed.json", {})
    for plugin in inventory.get("plugins", []):
        if set(plugin) - {"reference", "name", "display_name", "version", "marketplace", "installed", "enabled"}:
            errors.append("unreviewed private field in plugin snapshot")
    return errors


if __name__ == "__main__":
    problems = audit()
    if problems:
        print(json.dumps({"errors": problems}, indent=2))
        sys.exit(1)
    print("RELEASE_CHECK_OK")
