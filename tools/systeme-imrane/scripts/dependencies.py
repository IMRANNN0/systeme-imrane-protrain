"""Dependency checks and explicit package-manager plans, never shell interpolation."""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

from common import ROOT, read_json


def version_tuple(text):
    match = re.search(r"(?<![a-zA-Z])v?(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(map(int, (match.group(1), match.group(2), match.group(3) or "0"))) if match else None


def executable(command):
    if command == "@python":
        return sys.executable
    found = shutil.which(command + ".cmd") if os.name == "nt" else None
    found = found or shutil.which(command)
    if found and "microsoft/windowsapps" in found.replace("\\", "/").lower():
        return None  # A Windows Store alias is not a working installation.
    return found


def inspect_dependencies(profile, workspace=None):
    config = read_json(ROOT / "config/dependencies.json")
    rows = []
    for spec in config["system"]:
        if profile == "core" and spec["profile"] != "core":
            continue
        binary = executable(spec["command"])
        row = {"name": spec["name"], "minimum": spec["minimum"], "status": "missing"}
        if binary:
            try:
                result = subprocess.run([binary, *spec.get("version_args", ["--version"])],
                                        capture_output=True, text=True, timeout=10, errors="replace")
                version = version_tuple(result.stdout + result.stderr)
                minimum = version_tuple(spec["minimum"])
                row["version"] = ".".join(map(str, version)) if version else None
                row["status"] = "ok" if result.returncode == 0 and version and version >= minimum else "outdated-or-unverified"
            except (OSError, subprocess.SubprocessError):
                row["status"] = "unusable"
        rows.append(row)
    if profile == "complete" and workspace is not None:
        rows.extend(inspect_managed(workspace))
    return rows


def inspect_managed(workspace):
    workspace = Path(workspace).resolve()
    rows = []
    python = venv_python(workspace)
    graph = {"name": "managed:graphify", "required": "0.8.13", "status": "missing"}
    if python.exists():
        try:
            result = subprocess.run([str(python), "-c", "import graphify.llm,openai,tiktoken; import importlib.metadata as m; print(m.version('graphifyy')); print(m.version('openai')); print(m.version('tiktoken'))"], capture_output=True, text=True, timeout=10)
            versions = result.stdout.splitlines()
            graph["status"] = "ok" if result.returncode == 0 and len(versions) == 3 and versions[0] == "0.8.13" else "outdated-or-unverified"
            graph["version"] = versions[0] if versions else None
        except (OSError, subprocess.SubprocessError):
            graph["status"] = "unusable"
    rows.append(graph)
    module_names = {"Pillow": "PIL.Image", "pypdf": "pypdf", "python-docx": "docx", "openpyxl": "openpyxl", "PyYAML": "yaml", "reportlab": "reportlab"}
    for requirement in read_json(ROOT / "config/dependencies.json")["python"]:
        name, version = requirement.split("==")
        if name.startswith("graphifyy"):
            continue
        row = {"name": "managed-python:" + name, "required": version, "status": "missing"}
        if python.exists():
            try:
                result = subprocess.run([str(python), "-c", "import importlib,importlib.metadata as m,sys; importlib.import_module(sys.argv[2]); print(m.version(sys.argv[1]))", name, module_names[name]], capture_output=True, text=True, timeout=10)
                installed = result.stdout.strip()
                row.update({"version": installed or None, "status": "ok" if result.returncode == 0 and installed == version else "missing-or-different-version"})
            except (OSError, subprocess.SubprocessError):
                row["status"] = "unusable"
        rows.append(row)
    for spec in read_json(ROOT / "config/npm-tools-lock.json")["packages"]:
        if spec.get("profile") == "optional-host":
            continue
        manifest = workspace / ".imrane/npm/node_modules" / spec["name"] / "package.json"
        installed = read_json(manifest, {})
        row = {"name": "managed:" + spec["name"], "required": spec["version"], "version": installed.get("version"), "status": "missing-or-different-version"}
        if installed.get("version") == spec["version"]:
            binary_name = {"@canonry/canonry": "canonry"}.get(spec["name"], spec["name"])
            binary = workspace / ".imrane/npm/node_modules/.bin" / (binary_name + (".cmd" if os.name == "nt" else ""))
            if spec["name"] == "sharp":
                node = executable("node")
                command = [node, "-e", "const s=require(process.argv[1]); process.stdout.write(s.versions.vips);", str(manifest.parent)] if node else None
            else:
                command = [str(binary), "--help" if binary_name == "canonry" else "--version"] if binary.is_file() else None
            if command:
                try:
                    result = subprocess.run(command, capture_output=True, text=True, timeout=10, errors="replace")
                    row["status"] = "ok" if result.returncode == 0 and result.stdout.strip() else "unusable"
                except (OSError, subprocess.SubprocessError):
                    row["status"] = "unusable"
            else:
                row["status"] = "missing-binary-or-runtime"
        rows.append(row)
    browser = {"name": "managed:chromium", "status": "missing"}
    playwright = workspace / ".imrane/npm/node_modules/playwright"
    node = executable("node")
    if node and playwright.exists():
        try:
            result = subprocess.run([node, "-e", "const p=require(process.argv[1]); process.stdout.write(require('fs').existsSync(p.chromium.executablePath())?'ok':'missing');", str(playwright)], capture_output=True, text=True, timeout=10)
            browser["status"] = "ok" if result.returncode == 0 and result.stdout == "ok" else "missing-or-unusable"
        except (OSError, subprocess.SubprocessError):
            browser["status"] = "unusable"
    rows.append(browser)
    return rows


def system_plan(profile, rows, system=None):
    system = system or platform.system()
    if system not in ("Windows", "Darwin"):
        raise ValueError("System package installation supports Windows/macOS; CI can run portable tests elsewhere")
    manager = "winget" if system == "Windows" else "brew"
    config = read_json(ROOT / "config/dependencies.json")
    status = {r["name"]: r["status"] for r in rows}
    commands = []
    for spec in config["system"]:
        if spec["name"] not in status or status[spec["name"]] == "ok" or "bundled_with" in spec:
            continue
        if system == "Windows":
            verb = "install" if status[spec["name"]] == "missing" else "upgrade"
            commands.append([manager, verb, "--id", spec["winget"], "--exact", "--source", "winget"])
        else:
            verb = "install" if status[spec["name"]] == "missing" else "upgrade"
            commands.append([manager, verb, spec["brew"]])
    return manager, commands


def venv_python(workspace):
    return Path(workspace) / ".imrane/venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def install_dependencies(workspace, profile, apply=False):
    workspace = Path(workspace).resolve()
    rows = inspect_dependencies(profile)
    manager, commands = system_plan(profile, rows)
    if profile == "complete":
        vpython = venv_python(workspace)
        commands.extend([[sys.executable, "-m", "venv", str(vpython.parent.parent)],
                         [str(vpython), "-m", "pip", "install", *read_json(ROOT / "config/dependencies.json")["python"]]])
        lock = read_json(ROOT / "config/npm-tools-lock.json")
        packages = [f"{p['name']}@{p['version']}" for p in lock["packages"] if p.get("profile", "complete") == "complete"]
        npm = executable("npm") or ("npm.cmd" if os.name == "nt" else "npm")
        commands.append([npm, "install", "--prefix", str(workspace / ".imrane/npm"), "--no-audit", "--no-fund", *packages])
        commands.append([str(workspace / ".imrane/npm/node_modules/.bin" / ("playwright.cmd" if os.name == "nt" else "playwright")), "install", "chromium"])
    for command in commands:
        print("PLAN: " + json.dumps(list(map(str, command))))
    print("Host login, provider keys and MCP/plugin connections are personal setup; see docs/INSTALLATION.md.")
    if not apply:
        return 0
    if any(command[0] == manager for command in commands) and not shutil.which(manager):
        raise ValueError(f"Install {manager} from its official site, then rerun; no unreviewed shell bootstrap is executed")
    for command in commands:
        # Do not recreate a populated venv on each invocation.
        if command[1:3] == ["-m", "venv"] and venv_python(workspace).exists():
            continue
        subprocess.run(command, check=True)
    print("DEPENDENCY_INSTALL_FINISHED: reopen terminal and rerun doctor; no success inferred from package-manager exit alone.")
    return 0
