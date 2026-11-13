"""Read official pinned package data through its own venv, without running install hooks."""
import importlib.metadata
import importlib.util
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    if sys.argv[1:] != ["graphify"]:
        sys.exit("Unsupported package skill")
    distribution = importlib.metadata.distribution("graphifyy")
    if distribution.version != "0.8.13":
        sys.exit("Graphify package version mismatch")
    root = Path(importlib.util.find_spec("graphify").origin).parent
    licenses = [f for f in distribution.files or [] if f.name.upper() == "LICENSE" and ".dist-info" in str(f)]
    if not licenses:
        sys.exit("Pinned package license missing")
    result = {"skill": (root / "skill-codex.md").read_text(encoding="utf-8"),
              "license": distribution.locate_file(licenses[0]).read_text(encoding="utf-8")}
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
