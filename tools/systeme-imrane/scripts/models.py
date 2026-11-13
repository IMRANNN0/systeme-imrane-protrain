#!/usr/bin/env python3
"""Plan or explicitly migrate a personal policy; never change active/global models."""
import argparse
import copy
import sys
from pathlib import Path

from common import ROOT, now, read_json, registry, relative_path, write_json


def migrate(workspace, preset=None, apply=False):
    workspace = Path(workspace).resolve()
    registry(workspace)
    target = relative_path(workspace, ".codex/model-routing-policy.json")
    old = read_json(target, {})
    result = read_json(ROOT / "config/models.json")
    # Preserve personal bindings, Claude effort and additional custom routes.
    for name, existing in old.get("routes", {}).items():
        if name not in result["routes"]:
            result["routes"][name] = copy.deepcopy(existing)
            continue
        for key in ("codex_model", "claude_model", "claude_effort", "reasoning_effort"):
            if key in existing:
                result["routes"][name][key] = existing[key]
        if "reasoning_effort" not in existing and "reasoning_effort" in old:
            result["routes"][name]["reasoning_effort"] = old["reasoning_effort"]
    if preset:
        if preset != "codex-sol-luna-6":
            raise ValueError("Unknown Codex preset")
        for name, binding in read_json(ROOT / "config/codex-sol-luna-6.json")["routes"].items():
            result["routes"][name].update(binding)
    changed = result != old
    print(f"{'UPDATE' if changed else 'UNCHANGED'}: personal routing policy v{result['version']}; "
          f"Codex preset={preset or 'none; bindings preserved'}; Claude bindings preserved")
    for name, binding in result["routes"].items():
        print(f"  {name}: Codex={binding.get('codex_model') or 'unconfigured'} / "
              f"{binding.get('reasoning_effort', 'high')}; Claude={binding.get('claude_model') or 'unconfigured'} / "
              f"{binding.get('claude_effort', 'high')}")
    if apply and changed:
        if old:
            backup = relative_path(workspace, ".imrane/backups/models-" + now().replace(":", "-") + ".json")
            write_json(backup, old, private=True)
        write_json(target, result, private=True)
    if not apply:
        print("PLAN ONLY: inspect account model availability, then repeat with --apply if approved.")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--preset", choices=("codex-sol-luna-6",))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        migrate(args.workspace, args.preset, args.apply)
    except (ValueError, OSError) as exc:
        print("MODEL_POLICY_ERROR: " + str(exc), file=sys.stderr)
        sys.exit(2)
