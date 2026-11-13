"""Shared portable primitives. No business state or machine-specific paths."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default


def atomic_write(path, text, private=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".imrane-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        if private:
            os.chmod(temp, 0o600)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def write_json(path, obj, private=False):
    atomic_write(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n", private)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def inside(root, value):
    root, value = Path(root).resolve(), Path(value).resolve()
    if not value.is_relative_to(root):
        raise ValueError("Path escapes the selected workspace")
    return value


def relative_path(root, text):
    p = Path(text)
    if p.is_absolute() or any(part == ".." for part in p.parts):
        raise ValueError("A relative path without parent traversal is required")
    return inside(root, Path(root) / p)


def slug(value):
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value):
        raise ValueError("Project id must match [a-z][a-z0-9-]{0,63}")
    return value


def registry(workspace):
    data = read_json(Path(workspace) / ".codex/projects.json")
    if not isinstance(data, dict) or not isinstance(data.get("projects"), list):
        raise ValueError("Workspace not initialized: run init --apply first")
    ids, paths = set(), set()
    for project in data["projects"]:
        slug(project["id"])
        path = relative_path(workspace, project["path"])
        if path == Path(workspace).resolve():
            raise ValueError("The governance root cannot be a business project")
        if project["id"] in ids or str(path).casefold() in paths:
            raise ValueError("Duplicate project identity/path")
        ids.add(project["id"])
        paths.add(str(path).casefold())
    return data


def project_by_id(workspace, project_id):
    for project in registry(workspace)["projects"]:
        if project["id"] == project_id:
            return project
    governance = governance_lane(workspace)
    if governance and governance["id"] == project_id:
        return governance
    raise ValueError("Unknown project id")


def governance_lane(workspace):
    """Optional local extension: root context without registering a business project."""
    value = read_json(Path(workspace) / ".codex/governance.json")
    if value is None:
        return None
    if (value.get("id") != "governance" or value.get("path") != "."
            or value.get("kind") != "governance"):
        raise ValueError("Invalid governance descriptor")
    if any(p["id"] == value["id"] for p in registry(workspace)["projects"]):
        raise ValueError("Governance identity collides with a business project")
    return value


def resolve_project(workspace, cwd, allow_selector=True):
    data = registry(workspace)
    work = Path(cwd).resolve()
    matches = [p for p in data["projects"]
               if work.is_relative_to(relative_path(workspace, p["path"]))]
    if matches:
        return max(matches, key=lambda p: len(relative_path(workspace, p["path"]).parts))
    # Never inject another project's context when a hook runs outside this workspace.
    if not work.is_relative_to(Path(workspace).resolve()):
        return None
    if allow_selector and work == Path(workspace).resolve():
        selector = read_json(Path(workspace) / "tmp/codex-session/ACTIVE_PROJECT.json", {})
        chosen = selector.get("project_id", data.get("default_project"))
        selected = next((p for p in data["projects"] if p["id"] == chosen), None)
        if selected:
            return selected
    return governance_lane(workspace)


def runtime_dir(workspace, project_id):
    slug(project_id)
    return Path(workspace) / "tmp/codex-session/projects" / project_id


def safe_error(exc):
    # Provider exceptions can contain authorization headers, URLs and body content.
    # Persist only an exception class; never stringify arbitrary SDK exceptions.
    return type(exc).__name__
