"""JSON CLI and self-contained, escaped HTML board."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

from .core import (Scope, WorkError, advance, defaults, gate, is_blocked, metrics, now,
                   patch_record, read_json, slug, targets)

BOARD_MARKER = "<!-- imrane-work board v1 -->"


def check(record, scope):
    readiness = {target: {"ready": not (errors := gate(record, target, scope)), "errors": errors} for target in targets(record)}
    return {"id": record["id"], "project": scope.project, "stage": record["stage"], "record_valid": True,
            "gates": readiness, "metrics": metrics(record),
            "validation_limit": "Mechanical checks only. Evidence content, independence and sanitization are user attestations; no source is executed or browsed."}


def score(record):
    p = record["priority"]
    return p["impact"] * p["urgency"] / p["effort"]


def board(records, scope):
    escape = lambda value: html.escape(str(value), quote=True)
    active = sorted((r for r in records if not is_blocked(r) and r["stage"] != "follow-up"), key=lambda r: (-score(r), r["id"]))
    blocked = sorted((r for r in records if is_blocked(r)), key=lambda r: r["id"])
    completed = sorted((r for r in records if not is_blocked(r) and r["stage"] == "follow-up"), key=lambda r: r["id"])
    sections = []
    for label, values in (("Recommended next work", active), ("Blocked", blocked), ("Follow-up", completed)):
        rows = []
        for r in values:
            m = metrics(r)
            passed = sum(e["result"] == "pass" and e["kind"] in ("measured", "observed") for e in r["evidence"])
            reason = r["blocker"]["reason"] if r["blocker"]["active"] else r["priority"]["reason"]
            if is_blocked(r):
                reason += "; " + "; ".join(i["description"] for i in r["brief"]["missing_inputs"] if i["disposition"] == "blocking")
            metrics_text = "; ".join(f"{key}: {'unmeasured' if value is None else round(value, 3)}" for key, value in m.items())
            rows.append("<tr>" + "".join(f"<td>{escape(v)}</td>" for v in (r["id"] + ": " + r["title"], r["stage"], r["owner"], r["next_action"], f"{score(r):.2f}: {reason}", f"{passed}/{len(r['evidence'])} passed observed/measured", metrics_text)) + "</tr>")
        sections.append(f"<h2>{label}</h2><table><thead><tr>" + "".join(f"<th>{x}</th>" for x in ("Work", "Stage", "Owner", "Next action", "Score / reason", "Evidence", "Metrics")) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>")
    top = "".join(f"<li>{escape(r['id'])}: {score(r):.2f} — {escape(r['priority']['reason'] or 'No priority reason supplied; review before choosing.')} Next: {escape(r['next_action'])}</li>" for r in active[:3])
    return BOARD_MARKER + "\n<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'\"><title>Local work board</title><style>body{font:15px system-ui;margin:2rem;color:#19232d;background:#faf9f5}table{border-collapse:collapse;width:100%;margin-bottom:2rem}th,td{border:1px solid #c9ccc8;padding:.65rem;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e4e8e3}h1{font-size:2rem}p{max-width:85ch}</style><body>" + f"<h1>{escape(scope.project)} · local work board</h1><p>Generated {escape(now())}. Exact selected lane only. Priority recommendation = impact × urgency ÷ effort; heuristic, no automatic selection. Follow-up means recorded local handoff readiness; this tool sends nothing.</p><h2>Top 3 recommendations</h2><ol>{top}</ol>" + "".join(sections) + "<p>Evidence/source checks are mechanical. Unmeasured outcomes stay unmeasured. No network resources or executable scripts.</p></body></html>"


def output_path(scope, reference, suffix):
    path = scope.path(reference)
    if path.suffix.lower() != suffix:
        raise WorkError(f"output must use {suffix} extension")
    relative = path.relative_to(scope.root)
    if any(part.startswith(".") for part in relative.parts) and not path.is_relative_to(scope.store):
        raise WorkError("output cannot modify hidden/configuration directories")
    if path.is_relative_to(scope.store) and path != scope.store / "board.html" and not path.is_relative_to(scope.store / "exports"):
        raise WorkError("output may only use board.html or exports within private work store")
    return path


def parser():
    p = argparse.ArgumentParser(description="Offline scoped work management (Python 3.10+). JSON output; no external sending or execution.")
    p.add_argument("--workspace", required=True, help="explicit workspace root containing .codex/projects.json")
    p.add_argument("--project", required=True, help="registered active ID or governance; no aggregation")
    commands = p.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="create at qualification from JSON; safe defaults for omitted fields")
    create.add_argument("--input", required=True)
    for name in ("show", "update", "advance", "check", "lesson-export"):
        command = commands.add_parser(name)
        command.add_argument("--id", required=True)
        if name == "update":
            command.add_argument("--input", required=True, help="shallow editable-field JSON patch; nested objects/arrays replace")
        if name == "advance":
            command.add_argument("--to", required=True)
        if name == "lesson-export":
            command.add_argument("--lesson-id", required=True)
            command.add_argument("--output", required=True)
    commands.add_parser("board").add_argument("--output", help="new scoped HTML path or managed board; default .imrane/work/board.html")
    return p


def run(args):
    scope = Scope(args.workspace, args.project)
    if args.command in ("create", "update"):
        patch = read_json(scope.path(args.input))
    if args.command == "create":
        if not isinstance(patch, dict):
            raise WorkError("create input must be object")
        item_id = slug(patch.get("id"))
        record = patch_record(defaults(item_id, scope.project), patch, scope, create=True)
        with scope.lock():
            scope.save(record)
        return {"ok": True, "record": record, "metrics": metrics(record)}, 0
    if args.command == "board":
        path = output_path(scope, args.output or ".imrane/work/board.html", ".html")
        with scope.lock():
            records = []
            folder = scope.path(scope.store / "items")
            if folder.exists():
                for candidate in sorted(folder.glob("*.json")):
                    record, _ = scope.load(candidate.stem)
                    records.append(record)
            expected = None
            if path.exists():
                raw = path.read_bytes()
                if not raw.startswith(BOARD_MARKER.encode()):
                    raise WorkError("refusing to overwrite unrelated HTML output")
                expected = hashlib.sha256(raw).hexdigest()
            scope.write(path, board(records, scope), expected)
        return {"ok": True, "project": scope.project, "items": len(records), "output": str(path)}, 0
    if args.command in ("show", "check"):
        record, _ = scope.load(args.id)
        if args.command == "show":
            return {"ok": True, "record": record, "metrics": metrics(record)}, 0
        result = check(record, scope)
        ready = not result["gates"] or any(g["ready"] for g in result["gates"].values())
        return {"ok": ready, **result}, 0 if ready else 1
    with scope.lock():
        record, expected = scope.load(args.id)
        if args.command == "update":
            updated = patch_record(record, patch, scope)
            scope.save(updated, expected)
            return {"ok": True, "record": updated, "metrics": metrics(updated)}, 0
        if args.command == "advance":
            updated = advance(record, args.to, scope)
            scope.save(updated, expected)
            return {"ok": True, "record": updated, "metrics": metrics(updated)}, 0
        if args.command == "lesson-export":
            slug(args.lesson_id, "lesson-id")
            lesson = next((x for x in record["lessons"] if x["id"] == args.lesson_id), None)
            if lesson is None:
                raise WorkError("lesson not found")
            if lesson["status"] != "approved" or not lesson["sanitized"] or not lesson["reviewer"].strip() or not lesson["reviewed_at"]:
                raise WorkError("export requires approved, sanitized and reviewed lesson")
            if not all(lesson[key].strip() for key in ("summary", "context", "limitations", "proposed_change")):
                raise WorkError("export requires meaningful summary, context, limitations and proposed_change")
            path = output_path(scope, args.output, ".json")
            # No record/project/title/brief/evidence included. Sanitization remains reviewer's attestation.
            payload = {"schema_version": 1, "kind": "reviewed-lesson", "lesson": lesson}
            scope.write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            return {"ok": True, "output": str(path), "lesson_id": lesson["id"], "note": "Local export only. Shared promotion requires separate review."}, 0
    raise WorkError("unsupported command")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result, code = run(args)
    except (WorkError, OSError, KeyError, TypeError) as exc:
        result, code = {"ok": False, "errors": [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code
