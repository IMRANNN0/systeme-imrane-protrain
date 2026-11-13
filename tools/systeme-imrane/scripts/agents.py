#!/usr/bin/env python3
"""Generate host-specific agent roles from personal model bindings, never launch one."""
import argparse
import json
import re
import sys
from pathlib import Path

from imrane import managed
from common import read_json, registry

INSTRUCTIONS = (
    "Own only the explicitly assigned task. Read the active lane rules and bounded context. "
    "You are not alone in this workspace: preserve others' edits. Establish acceptance checks, "
    "protect secrets and project boundaries, verify your result and report evidence and residual risks. "
    "Do not publish, contact external parties, expand permissions or spawn more agents without authorization."
)


def generate(workspace, apply=False, upgrade=False):
    workspace = Path(workspace).resolve()
    data = registry(workspace)
    policy = read_json(workspace / ".codex/model-routing-policy.json")
    files = {}
    for route, spec in policy["routes"].items():
        if not re.fullmatch(r"[a-z][a-z_]{0,63}", route):
            raise ValueError("Invalid route identifier")
        for host in ("codex", "claude"):
            model = spec.get(host + "_model")
            if not model:
                print(f"UNCONFIGURED: {host} / {route}; advisory routing remains available")
                continue
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/\[\]-]{0,150}", model):
                raise ValueError("Model ids must be plain identifiers; shell/YAML fragments are rejected")
            name = "route-" + route.replace("_", "-")
            if host == "codex":
                effort = spec.get("reasoning_effort", policy.get("reasoning_effort", "high"))
                if effort not in ("low", "medium", "high", "xhigh"):
                    raise ValueError("Unsupported automatic Codex reasoning effort")
                text = (f"name = {json.dumps(name.replace('-', '_'))}\n"
                        f"description = {json.dumps(spec['label'] + ' explicitly delegated project worker')}\n"
                        f"model = {json.dumps(model)}\nmodel_reasoning_effort = {json.dumps(effort)}\n"
                        f"developer_instructions = {json.dumps(INSTRUCTIONS)}\n")
                rel = f".codex/agents/{name}.toml"
            else:
                effort = spec.get("claude_effort", "high")
                if effort not in ("low", "medium", "high", "max"):
                    raise ValueError("Unsupported configured Claude effort")
                text = f"---\nname: {name}\ndescription: {spec['label']} explicitly delegated project worker\nmodel: {json.dumps(model)}\neffort: {effort}\n---\n\n{INSTRUCTIONS}\n"
                rel = f".claude/agents/{name}.md"
            files[rel] = text
            for project in data["projects"]:
                files[project["path"] + "/" + rel] = text
    if not files:
        print("No agent roles generated. Choose accessible models in the policy first.")
        return 1
    managed(workspace, files, apply, upgrade)
    print("Agent files generated/planned only; reload and inspect the host's role list. No active model was changed.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--upgrade", action="store_true")
    args = parser.parse_args()
    try:
        sys.exit(generate(args.workspace, args.apply, args.upgrade))
    except (ValueError, OSError) as exc:
        print("AGENT_CONFIG_ERROR: " + str(exc), file=sys.stderr)
        sys.exit(2)
