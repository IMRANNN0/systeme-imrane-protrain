"""Opt-in download-only test of all pinned GitHub skills. Never executes their code."""
import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from imrane import initialize
from common import read_json
from skills import install


if __name__ == "__main__":
    if sys.argv[1:] != ["--allow-network"]:
        print("Explicit --allow-network required: GitHub archives only, no model API or source execution")
        sys.exit(2)
    root = ROOT / ".imrane/network-smoke"
    root.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(root)
    workspace = root / "workspace"
    with contextlib.redirect_stdout(io.StringIO()):
        initialize(workspace, apply=True)
    specs = [s for s in read_json(ROOT / "config/skills-lock.json")["skills"] if s["status"] == "github"]
    result = install(workspace, specs, apply=True)
    if result == 0:
        print(f"SKILLS_NETWORK_SMOKE_OK: {len(specs)} pinned GitHub skills downloaded; none executed")
    sys.exit(result)
