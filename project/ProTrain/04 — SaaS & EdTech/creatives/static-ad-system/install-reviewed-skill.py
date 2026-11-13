"""Install reviewed generic guidance and its workspace routing rule."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

NAME = "static-ad-creative-system"
ROOT = Path("{{IMRANE_WORKSPACE_ROOT}}")
LOCAL = Path(__file__).resolve().parent
SOURCE = LOCAL / "skill-draft" / NAME
MARKER = "<!-- static-ad-creative-system:start -->"
RULE = """

<!-- static-ad-creative-system:start -->
## Static advertising image workflow

For static ad concepts, marketing-image production, or creative reviews, read
`{{IMRANE_WORKSPACE_ROOT}}/.agents/skills/static-ad-creative-system/SKILL.md` before the concept
or generation prompt, then consult it again against the actual exported image.
Read the selected project's current brand, claim sources, and durable creative
feedback referenced by its AGENTS.md or CURRENT.md. Keep client-specific feedback
inside that project. Save new observed failures and owner preferences locally so
the next relevant image task consults them. Apply the method proportionately;
unrelated illustration and general image edits do not inherit an ad strategy.

This is an instruction-based workflow, not a technical interception of image-tool
calls. It does not authorize publication, spending, contact, or network indexing.
<!-- static-ad-creative-system:end -->
"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=".static-ad-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
        os.replace(temp_name, path)
    finally:
        Path(temp_name).unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    manifest_path = ROOT / ".imrane" / f"{NAME}-install.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"files": {}}
    relative_files = ["SKILL.md"]
    if (SOURCE / "references/review-checklist.md").exists():
        relative_files.append("references/review-checklist.md")
    if (SOURCE / "agents/openai.yaml").exists():
        relative_files.append("agents/openai.yaml")
    payloads: dict[Path, bytes] = {}
    for name in relative_files:
        payload = (SOURCE / name).read_bytes()
        if any(token in payload.decode("utf-8").lower() for token in ("protrain", "199 dh", "clients/protrain")):
            raise SystemExit("Client-specific content must remain in the local lesson record")
        for library in (".agents/skills", ".claude/skills"):
            payloads[ROOT / library / NAME / name] = payload
    router = ROOT / "AGENTS.md"
    original_router = router.read_bytes()
    router_text = original_router.decode("utf-8-sig")
    if MARKER in router_text:
        if RULE.strip() not in router_text:
            raise SystemExit("Existing routing block differs; preserve for review")
    else:
        payloads[router] = (router_text.rstrip() + RULE).encode("utf-8")
    plan = []
    for path, payload in payloads.items():
        resolved = path.resolve()
        if not resolved.is_relative_to(ROOT.resolve()):
            raise SystemExit("Destination escapes the intended workspace")
        before = digest(path.read_bytes()) if path.exists() else None
        after = digest(payload)
        relative = path.relative_to(ROOT).as_posix()
        if before == after:
            action = "unchanged"
        elif path == router:
            action = "append-scoped-routing-rule"
        elif before is None:
            action = "create"
        elif manifest["files"].get(relative) == before:
            action = "update-managed"
        else:
            raise SystemExit("Unmanaged existing file preserved: " + relative)
        plan.append({"path": relative, "action": action, "before": before, "after": after})
    if args.apply:
        for row in plan:
            path = ROOT / row["path"]
            before = digest(path.read_bytes()) if path.exists() else None
            if before != row["before"]:
                raise SystemExit("Intervening change preserved: " + row["path"])
        for row in plan:
            if row["action"] != "unchanged":
                atomic_write(ROOT / row["path"], payloads[ROOT / row["path"]])
        files = {row["path"]: row["after"] for row in plan if row["path"] != "AGENTS.md"}
        installed = {"version": 1, "name": NAME, "origin": "Owner-requested, reviewed generic creative workflow", "installed_on": "2026-11-13", "files": files, "routing": "AGENTS.md scoped static-ad block", "invocation": "Instruction based; host catalog refresh not claimed"}
        atomic_write(manifest_path, (json.dumps(installed, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"applied": args.apply, "plan": plan}, indent=2))


if __name__ == "__main__":
    main()
