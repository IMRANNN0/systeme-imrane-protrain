"""Shared Codex/Claude lifecycle hooks. Input is untrusted JSON on stdin."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from imrane import snapshot
from common import now, read_json, relative_path, resolve_project, runtime_dir, write_json
from routing import recommend


CHECKPOINT_GUIDANCE = (
    "Restart Checkpoint: resolve the requested project's lane and read its latest .codex/memory/CURRENT.md "
    "before resuming project work. After a verified milestone in long work and before replying on a substantive "
    "turn, update that lane's checkpoint with the "
    "verified stage and result, acceptance check, blocker if any, and one concrete next action. Record a "
    "review date when relevant. Save a snapshot for that lane if native hooks are unavailable or the chat "
    "runs from a different lane. Keep transcripts, credentials and other projects' data out of the note. "
    "A casual or informational turn needs no checkpoint write."
)


def current_excerpt(workspace, project):
    root = relative_path(workspace, project["path"])
    current = root / ".codex/memory/CURRENT.md"
    if current.resolve() != current:
        return "Read CURRENT.md directly after checking its resolved path"
    if not current.is_file():
        return "Missing CURRENT.md"
    with current.open(encoding="utf-8") as handle:
        excerpt = handle.read(1801)
    sections = list(re.finditer(r"^## ", excerpt, re.MULTILINE))
    if len(sections) > 1:
        return excerpt[:sections[1].start()].rstrip()
    if len(excerpt) > 1800:
        return excerpt[:1800].rstrip() + "\nRead CURRENT.md for the rest of this checkpoint."
    return excerpt


def route_prompt(prompt, previous, policy):
    return {**recommend(prompt, previous, policy), "at": now()}


def run_hook(workspace, event, payload):
    project = resolve_project(workspace, payload.get("cwd") or Path.cwd())
    if project is None:
        return {}
    lane = runtime_dir(workspace, project["id"])
    # Separate simultaneous host conversations; hash identifiers instead of trusting paths.
    import hashlib
    session = hashlib.sha256(str(payload.get("session_id", "manual")).encode()).hexdigest()[:20]
    state_path = lane / "sessions" / (session + ".json")
    state = read_json(state_path, {})
    state.update({"project_id": project["id"], "event": event, "at": now()})
    if event in ("SessionStart", "UserPromptSubmit", "Stop", "PreCompact"):
        lifecycle = state.get("lifecycle")
        if not isinstance(lifecycle, dict):
            lifecycle = {}
        lifecycle[event] = state["at"]
        state["lifecycle"] = lifecycle
    context = ""
    if event == "SessionStart":
        graph = read_json(lane / "graphify-state.json", {})
        label = "governance scope" if project.get("kind") == "governance" else "project"
        context = (f"Active {label}: {project['id']} ({project['path']}). Read its AGENTS.md and CONTEXT_INDEX.md only.\n"
                   f"Graphify state: {graph.get('status', 'not-built')}; retrieval is not canonical memory.\n"
                   f"{CHECKPOINT_GUIDANCE}\n\nScoped CURRENT.md excerpt:\n{current_excerpt(workspace, project)}")
        state["checkpoint_context_sent"] = True
        last = read_json(lane / "latest-snapshot.json", {})
        if last:
            context += f"\nRecovery snapshot available privately ({last.get('at', 'unknown')}); read only if needed."
    elif event == "UserPromptSubmit":
        policy = read_json(Path(workspace) / ".codex/model-routing-policy.json")
        state["routing"] = route_prompt(str(payload.get("prompt", "")), state.get("routing", {}), policy)
        route = state["routing"]["route"]
        route_config = policy["routes"][route]
        effort = state["routing"]["reasoning"]
        claude_effort = route_config.get("claude_effort", "high")
        context = (f"Complexity recommendation: {route}; Codex reasoning {effort}; Claude effort {claude_effort}. "
                   f"Configured models: Codex={route_config.get('codex_model') or 'not selected'}, "
                   f"Claude={route_config.get('claude_model') or 'not selected'}. "
                   "Advisory only: hooks cannot change this active task's model or authorize delegation.")
        automatic = read_json(Path(workspace) / ".codex/automatic-routing.json", {})
        if automatic.get("enabled") and automatic.get("host") == "codex":
            context += (" Owner-authorized workspace policy separately requires automatic Codex delegated execution. "
                        "Controllers: use imrane-route.py and one native worker with its selected model/effort; "
                        "workers must execute directly without further delegation. Claude remains advisory.")
        context += f"\n{CHECKPOINT_GUIDANCE}"
        if not payload.get("session_id") or not state.get("checkpoint_context_sent"):
            context += f"\n\nScoped CURRENT.md excerpt ({project['id']}):\n{current_excerpt(workspace, project)}"
            state["checkpoint_context_sent"] = True
    elif event == "PreCompact":
        # Save before any long-running work too: an external host timeout or crash
        # can terminate a process without executing its finally block.
        snapshot(workspace, project["id"], "precompact-before-refresh")
        try:
            from graphify_runtime import mark_stale
            mark_stale(workspace, project["id"])
            config = read_json(Path(workspace) / ".codex/graphify.json", {})
            if project.get("graphify_enabled", False) and config.get("auto_refresh"):
                # A global preference cannot authorize a lane's current corpus or
                # provider. The user can review them and explicitly run refresh.
                context = ("Graphify automatic refresh skipped: review this project's "
                           "corpus and provider, then explicitly authorize a refresh.")
        except Exception as exc:
            # Never expose arbitrary provider exception bodies. Preserve visible failure state.
            write_json(lane / "graphify-state.json", {"status": "error", "error": type(exc).__name__, "at": now()}, private=True)
        finally:
            snapshot(workspace, project["id"], "precompact")
    elif event == "Stop":
        snapshot(workspace, project["id"], "stop")
        try:
            from graphify_runtime import refresh_local
            local_status = refresh_local(workspace, project["id"])
            if local_status != "disabled":
                state["graphify_local"] = {"status": local_status}
        except Exception as exc:
            state["graphify_local"] = {"status": "error", "error": type(exc).__name__}
    # No prompt, tool_input, tool_response, transcript or credentials are retained.
    write_json(state_path, state, private=True)
    if context:
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": context[:3600]}}
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--event", required=True, choices=("SessionStart", "UserPromptSubmit", "PostToolUse", "Stop", "PreCompact"))
    args = parser.parse_args()
    try:
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        raw = sys.stdin.read(1048577)
        if len(raw) > 1048576:
            raise ValueError("Hook payload too large")
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("Hook payload must be an object")
        print(json.dumps(run_hook(Path(args.workspace).resolve(), args.event, payload), ensure_ascii=True))
        return 0
    except Exception as exc:
        # A malformed hook must be visible, never delete continuity or print its input.
        print(f"Systeme Imrane hook failed: {type(exc).__name__}; check workspace configuration.", file=sys.stderr)
        print("{}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
