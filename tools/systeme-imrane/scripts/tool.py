#!/usr/bin/env python3
"""Run a known managed tool without modifying global PATH."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

from dependencies import executable, venv_python


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("tool", choices=("lighthouse", "pa11y", "linkinator", "playwright", "canonry", "python", "codex"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    if args.tool == "python":
        binary = venv_python(workspace)
        if not binary.is_file():
            print("Managed Python missing; install complete dependencies first", file=sys.stderr)
            return 1
    else:
        local = workspace / ".imrane/npm/node_modules/.bin" / (args.tool + (".cmd" if os.name == "nt" else ""))
        binary = str(local) if local.is_file() else (executable("codex") if args.tool == "codex" else None)
        if not binary:
            print("Tool missing: install its dependency profile first", file=sys.stderr)
            return 1
    return subprocess.run([str(binary), *args.arguments]).returncode


if __name__ == "__main__":
    sys.exit(main())
