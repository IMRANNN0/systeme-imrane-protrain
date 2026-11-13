"""Reviewed source/installation inventory. Never glob runtime into an installation."""
from pathlib import Path

from common import ROOT, read_json, relative_path


def inventory(root=ROOT):
    value = read_json(Path(root) / "config/distribution-files.json")
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ValueError("Missing/invalid distribution inventory")
    for key in ("toolkit", "adapters"):
        items = value.get(key)
        if not isinstance(items, list) or not items or len(items) != len(set(items)):
            raise ValueError("Invalid distribution inventory: " + key)
        for name in items:
            if not isinstance(name, str) or "\\" in name:
                raise ValueError("Invalid distribution path")
            relative_path(Path(root) if key == "toolkit" else Path(root).parent, name)
    required = {"LICENSE", "NOTICE.md", "README.md", "SECURITY.md", "SKILL.md", "bootstrap.ps1", "bootstrap.sh",
                "config/distribution-files.json", "scripts/imrane.py", "scripts/release_check.py",
                "scripts/distribution.py", "tests/test_runtime.py", "tests/test_routing.py", "tests/test_governance_hardening.py"}
    if not required.issubset(value["toolkit"]) or not {"imrane-route.py", "imrane-work.py"}.issubset(value["adapters"]):
        raise ValueError("Distribution contract omits legal, entry, security, test or adapter files")
    return value


def installation_files(root=ROOT):
    root = Path(root).resolve()
    spec = inventory(root)
    files = {}
    for key, base, prefix in (("toolkit", root, "tools/systeme-imrane/"),
                              ("adapters", root.parent, "tools/")):
        for rel in spec[key]:
            source = relative_path(base, rel)
            if not source.is_file() or source.is_symlink() or any(p.is_symlink() for p in source.parents if p.is_relative_to(base)):
                raise ValueError("Missing/linked distribution source: " + rel)
            files[prefix + rel] = source.read_text(encoding="utf-8")
    return files
