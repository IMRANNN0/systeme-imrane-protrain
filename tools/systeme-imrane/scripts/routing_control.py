"""Recipient opt-in only. Write consent metadata, never start a worker or change a model."""
from pathlib import Path
import tomllib

from common import ROOT, now, read_json, registry, write_json


def configure(workspace, enable=False, apply=False):
    workspace = Path(workspace).resolve()
    data = registry(workspace)
    target = workspace / ".codex/automatic-routing.json"
    current = read_json(target, read_json(ROOT / "config/automatic-routing.json"))
    if enable:
        policy = read_json(workspace / ".codex/model-routing-policy.json", {})
        missing = []
        for route in read_json(ROOT / "config/models.json")["routes"]:
            if not policy.get("routes", {}).get(route, {}).get("codex_model"):
                missing.append("model:" + route)
            for base in [workspace, *[workspace / p["path"] for p in data["projects"]]]:
                role = base / ".codex/agents" / ("route-" + route.replace("_", "-") + ".toml")
                if not role.is_file():
                    missing.append("role:" + role.relative_to(workspace).as_posix())
                    continue
                try:
                    value = tomllib.loads(role.read_text(encoding="utf-8"))
                    binding = policy.get("routes", {}).get(route, {})
                    if value.get("model") != binding.get("codex_model") or value.get("model_reasoning_effort") != binding.get("reasoning_effort", policy.get("reasoning_effort", "high")):
                        raise ValueError("Stale role binding")
                except (OSError, ValueError, UnicodeError):
                    missing.append("invalid/stale-role:" + role.relative_to(workspace).as_posix())
        if missing:
            raise ValueError("Configure accessible models and explicitly generate/review all six Codex roles before opt-in: " + ", ".join(missing))
    print(("ENABLE" if enable else "DISABLE") + ": recipient Codex native delegation policy; one worker; no nested delegation; host support/trust must be verified separately")
    if apply:
        current.update({"enabled": bool(enable), "host": "codex", "max_workers": 1,
                        "nested_delegation": False, "controller_changes_model": False,
                        "claude_enabled": False, "authorized_by": "recipient CLI --enable --apply" if enable else None,
                        "updated_at": now()})
        write_json(target, current, private=True)
    else:
        print("PLAN ONLY: repeat with --apply to record your choice. No worker was launched.")
    return 0
