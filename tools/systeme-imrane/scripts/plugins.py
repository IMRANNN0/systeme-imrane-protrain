#!/usr/bin/env python3
"""Read-only Codex plugin inventory and workflow plans; no auth/config is exported."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import ROOT, now, read_json, write_json
from dependencies import executable

DISPLAY_NAMES = {
    "documents":"Documents", "pdf":"PDF", "spreadsheets":"Spreadsheets", "presentations":"Presentations",
    "template-creator":"Template Creator", "codex-app-tools":"Codex App Tools", "browser":"Browser",
    "unified-computer-use":"Unified Computer Use", "chrome":"Chrome", "computer-use":"Computer Use",
    "code-review":"Code Review", "visualize":"Visualize", "notion":"Notion", "canva":"Canva",
    "vercel":"Vercel", "product-design":"Product Design", "humanwriting":"HumanWriting",
    "openai-templates":"OpenAI Templates", "pages":"Pages", "sites":"Sites",
    "plugin-management":"Plugin Management", "work-pets":"Work Pets",
    "app-69d669e1d5c88191957786fbcd38b411":"Opera Browser Connector",
    "app-6938a7d323f48191aeabaf579802bf45":"Adobe Acrobat",
    "app-6a54e4fb251081919c813b534af63ddf":"TaskNotify"
}


def sanitize(raw, stderr=""):
    rows = []
    for record in raw.get("installed", []):
        if not record.get("installed"):
            continue
        name = str(record.get("name", ""))
        rows.append({"reference":record.get("pluginId"), "name":name,
                     "display_name":DISPLAY_NAMES.get(name, name), "version":record.get("version"),
                     "marketplace":record.get("marketplaceName"), "installed":True,
                     "enabled":record.get("enabled") is True})
    return {"schema":1, "observed_at":now(), "source":"codex plugin list --json",
            "remote_catalogue_complete":"failed to list remote" not in stderr.casefold(),
            "authentication_verified":False, "plugins":rows,
            "note":"Installed/enabled does not prove OAuth login, tool access or availability on another account. No paths, tokens or permission policies exported."}


def inspect():
    binary = executable("codex")
    if not binary:
        raise ValueError("Codex CLI unavailable: inspect the Plugins UI or install the official client; Claude Code cannot emulate Codex plugins")
    result = subprocess.run([binary, "plugin", "list", "--json"], capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    if result.returncode:
        raise ValueError("Plugin inventory failed; no raw host diagnostics or credentials exported")
    return sanitize(json.loads(result.stdout), result.stderr)


def plan(inventory, profile):
    policy = read_json(ROOT / "config/plugin-profiles.json")["profiles"][profile]
    enabled = {p["name"] for p in inventory["plugins"] if p["installed"] and p["enabled"]}
    baseline = {p["name"]:p for p in read_json(ROOT / "config/codex-plugins-observed.json")["plugins"]}
    missing = [name for name in policy["recommended"] if name not in enabled]
    missing_groups = [group for group in policy["one_of"] if not enabled.intersection(group)]
    commands = []
    for name in missing:
        record = baseline.get(name, {})
        commands.append({"name":name, "display_name":DISPLAY_NAMES.get(name, name),
                         "install_command":["codex","plugin","add",record["reference"]] if record.get("marketplace") == "openai-curated-remote" else None,
                         "action":"Review availability in recipient's Plugins UI; approve installation/permissions and connect personally. Bundled runtimes depend on the host."})
    return {"profile":profile, "core_requires_plugins":False, "inventory_complete":inventory["remote_catalogue_complete"],
            "missing_recommended":commands, "missing_browser_choice_groups":missing_groups,
            "note":"Plan only. Do not install every browser/hosting option; choose the actual workflow. No installation, OAuth or permission change performed."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("inventory","plan"))
    p.add_argument("--output", help="Save sanitized inventory only; never a raw client config")
    p.add_argument("--profile", choices=tuple(read_json(ROOT / "config/plugin-profiles.json")["profiles"]), default="core")
    args = p.parse_args()
    try:
        inventory = inspect()
        if args.output:
            if args.command != "inventory":
                raise ValueError("--output is only valid for inventory")
            target = Path(args.output).resolve()
            if target.exists():
                raise ValueError("Inventory output exists; preserve/review it rather than overwrite")
            write_json(target, inventory)
        result = inventory if args.command == "inventory" else plan(inventory, args.profile)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if inventory["remote_catalogue_complete"] else 1
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("PLUGIN_INVENTORY_ERROR: " + (str(exc) if isinstance(exc, ValueError) else type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
