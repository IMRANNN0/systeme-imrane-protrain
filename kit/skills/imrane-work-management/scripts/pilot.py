#!/usr/bin/env python3
"""Run an offline synthetic work-management lifecycle in a new scratch directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def stamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New owned scratch directory; existing output is never overwritten")
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    output = Path(args.output).resolve()
    if output == skill_dir or output.is_relative_to(skill_dir) or skill_dir.is_relative_to(output):
        raise SystemExit("Choose a new scratch directory outside the installed skill")
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / "synthetic-workspace"
    workspace.mkdir()
    config = workspace / ".codex"
    config.mkdir()
    (workspace / "demo-client").mkdir()
    (config / "projects.json").write_text(json.dumps({"version": 1, "default_project": None, "projects": [{"id": "demo-client", "path": "demo-client", "name": "Synthetic demo"}]}), encoding="utf-8")
    (config / "governance.json").write_text(json.dumps({"version": 1, "id": "governance", "path": ".", "kind": "governance"}), encoding="utf-8")
    cli = script_dir / "imrane-work.py"
    events = []
    serial = 0

    def command(*arguments, expected=0, project="governance"):
        result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(cli), "--workspace", str(workspace), "--project", project, *arguments], capture_output=True, text=True, encoding="utf-8")
        if result.returncode != expected:
            raise AssertionError(f"{arguments[0]} returned {result.returncode}, expected {expected}: {result.stdout} {result.stderr}")
        payload = json.loads(result.stdout)
        events.append({"operation": arguments[0], "returncode": result.returncode, "stage": payload.get("record", {}).get("stage"), "at": stamp()})
        return payload

    def input_file(value):
        nonlocal serial
        serial += 1
        path = workspace / f"input-{serial}.json"
        path.write_text(json.dumps(value, indent=2), encoding="utf-8")
        return str(path)

    def patch(value, item="pricing-pilot"):
        return command("update", "--id", item, "--input", input_file(value))

    criteria = ["Each scenario reconciles clicks, orders, revenue and contribution", "The recommendation separates maximum revenue from maximum profit"]
    brief = {"goal": "Choose a price in a synthetic fixed-budget scenario", "deliverable": "pricing-memo.md and calculation-evidence.json", "in_scope": ["Four explicit hypothetical price/CVR scenarios"], "out_of_scope": ["Real market prediction", "Advertising spend", "Publishing"], "inputs": ["source.json: invented fixture assumptions, not real client data"], "missing_inputs": [], "acceptance": criteria}
    command("create", "--input", input_file({"id": "pricing-pilot", "title": "Synthetic pricing decision", "owner": "Synthetic production fixture", "mode": "standard", "domain": "financial", "brief": brief, "next_action": "Inspect the hypothetical source assumptions", "priority": {"impact": 4, "urgency": 3, "effort": 2, "reason": "A bounded calculation precedes any hypothetical pricing decision"}}))
    command("advance", "--id", "pricing-pilot", "--to", "production", expected=2)
    command("advance", "--id", "pricing-pilot", "--to", "research")
    source = {"synthetic": True, "budget": 2000, "cpc": 1, "variable_cost": 120, "prices": [250, 300, 350, 400], "cvr": [0.04, 0.035, 0.03, 0.025], "currency": "hypothetical units", "limitation": "No overhead, taxes, refunds, payment fees or capacity effects; outputs are contribution after ads, not full net profit"}
    (workspace / "source.json").write_text(json.dumps(source, indent=2), encoding="utf-8")
    research = {"id": "source-observation", "criterion": "Research assumptions", "kind": "observed", "source": "source.json", "observed_at": stamp(), "result": "pass", "notes": "Fixture assumptions inspected. CVR inputs are hypotheses, not measured market rates."}
    patch({"evidence": [research], "next_action": "Plan calculation and review tasks"})
    command("advance", "--id", "pricing-pilot", "--to", "plan")
    tasks = [{"id": "calculate", "title": "Calculate four scenario rows", "owner": "Synthetic production fixture", "status": "todo", "depends_on": []}, {"id": "write-memo", "title": "Write recommendation with limitations", "owner": "Synthetic production fixture", "status": "todo", "depends_on": ["calculate"]}]
    patch({"tasks": tasks, "next_action": "Calculate scenarios from explicit assumptions"})
    command("advance", "--id", "pricing-pilot", "--to", "production")
    rows = []
    for price, cvr in zip(source["prices"], source["cvr"]):
        orders = source["budget"] / source["cpc"] * cvr
        revenue = price * orders
        contribution = revenue - source["variable_cost"] * orders - source["budget"]
        rows.append({"price": price, "cvr": cvr, "cps": source["cpc"] / cvr, "orders": orders, "revenue": revenue, "contribution_after_ads": contribution})
    # Independent arithmetic oracle rather than reading the recommendation back.
    assert [round(r["contribution_after_ads"]) for r in rows] == [8400, 10600, 11800, 12000]
    assert [round(r["orders"]) for r in rows] == [80, 70, 60, 50]
    profit_price = max(rows, key=lambda row: row["contribution_after_ads"])["price"]
    max_revenue = max(r["revenue"] for r in rows)
    revenue_prices = [r["price"] for r in rows if abs(r["revenue"] - max_revenue) < 0.0001]
    assert profit_price == 400 and revenue_prices == [300, 350]
    (workspace / "calculation-evidence.json").write_text(json.dumps({"synthetic": True, "checked_at": stamp(), "rows": rows, "maximum_contribution_price": profit_price, "maximum_revenue_prices": revenue_prices, "limitations": source["limitation"]}, indent=2), encoding="utf-8")
    memo = "# Synthetic pricing memo\n\nFixture only; no real business recommendation.\n\n| Price | Orders | Revenue | Contribution after ads |\n| --- | --- | --- | --- |\n"
    memo += "".join(f"| {r['price']} | {r['orders']:.0f} | {r['revenue']:.0f} | {r['contribution_after_ads']:.0f} |\n" for r in rows)
    memo += "\n400 maximizes contribution in these assumptions; 300 and 350 tie for maximum revenue. CVR is an invented input. " + source["limitation"] + ".\n"
    (workspace / "pricing-memo.md").write_text(memo, encoding="utf-8")
    for task in tasks:
        task["status"] = "done"
    evidence = [research] + [{"id": f"criterion-{i+1}", "criterion": criterion, "kind": "measured", "source": "calculation-evidence.json", "observed_at": stamp(), "result": "pass", "notes": "Independent arithmetic oracle checks rows and distinct objective maxima; memo states exclusions"} for i, criterion in enumerate(criteria)]
    patch({"tasks": tasks, "evidence": evidence, "review": {"reviewer": "", "independent": False, "required": True, "verdict": "pending", "notes": "Parent review needed"}})
    command("advance", "--id", "pricing-pilot", "--to", "review")
    command("advance", "--id", "pricing-pilot", "--to", "delivery", expected=2)
    # Exercise a real review loop and require fresh evidence after returning to production.
    command("advance", "--id", "pricing-pilot", "--to", "production")
    evidence = json.loads(json.dumps(evidence))
    for entry in evidence:
        entry["observed_at"] = stamp()
    patch({"evidence": evidence, "next_action": "Recheck exclusions and scenario arithmetic"})
    command("advance", "--id", "pricing-pilot", "--to", "review")
    patch({"review": {"reviewer": "Parent verifier", "independent": True, "required": True, "verdict": "pass", "notes": "Independent row oracle and actual memo inspected; synthetic scope and cost exclusions explicit"}})
    command("advance", "--id", "pricing-pilot", "--to", "delivery")
    ready = command("show", "--id", "pricing-pilot")
    assert ready["metrics"]["time_to_first_delivery_seconds"] is None
    command("advance", "--id", "pricing-pilot", "--to", "follow-up", expected=2)
    decision = {"id": "objective-choice", "prediction": "Maximum revenue and maximum contribution may select different prices", "rationale": "Price changes both orders and contribution per order", "test": "Calculate four explicit fixed-budget cases", "observation": "Maximum contribution at 400; maximum revenue at 300 and 350", "outcome": "supported", "decided_at": stamp()}
    lesson = {"id": "separate-objectives", "summary": "Separate revenue and contribution objectives in scenario tables", "context": "Hypothetical fixed-budget pricing exercises", "limitations": "No observed demand curve or full net profit; validate real costs and CVR before applying", "status": "draft", "reviewer": "", "reviewed_at": "", "sanitized": False, "proposed_change": "Keep explicit objective and exclusions in future financial review checklists"}
    patch({"decisions": [decision], "lessons": [lesson], "delivery": {"summary": "Synthetic memo and calculation evidence prepared locally", "artifact": "pricing-memo.md", "delivered_at": stamp(), "channel": "local pilot artifact; no external sending"}, "next_action": "Measure comparable real tasks before claiming productivity improvement"})
    command("advance", "--id", "pricing-pilot", "--to", "follow-up")
    command("lesson-export", "--id", "pricing-pilot", "--lesson-id", lesson["id"], "--output", ".imrane/work/exports/lesson.json", expected=2)
    lesson.update(status="approved", reviewer="Parent verifier", reviewed_at=stamp(), sanitized=True)
    patch({"lessons": [lesson]})
    command("lesson-export", "--id", "pricing-pilot", "--lesson-id", lesson["id"], "--output", ".imrane/work/exports/lesson.json")
    # Visible blocker and escaped HTML on an independent light item.
    blocked_brief = dict(brief, missing_inputs=[{"description": "Await synthetic input", "disposition": "blocking", "reason": ""}])
    command("create", "--input", input_file({"id": "blocked-demo", "title": "<script>bad()</script> blocked fixture", "owner": "Synthetic owner", "mode": "light", "brief": blocked_brief, "next_action": "Resolve the synthetic missing input"}))
    command("advance", "--id", "blocked-demo", "--to", "production", expected=2)
    board_result = command("board")
    board_path = Path(board_result["output"])
    board_text = board_path.read_text(encoding="utf-8")
    assert "&lt;script&gt;bad()&lt;/script&gt;" in board_text and "<script>bad()" not in board_text
    assert "Blocked" in board_text and "pricing-pilot" in board_text
    check = command("check", "--id", "pricing-pilot")
    final = command("show", "--id", "pricing-pilot")
    assert final["record"]["stage"] == "follow-up"
    assert final["metrics"]["revision_cycles"] == 1
    assert final["metrics"]["escaped_errors"] is None
    exported = json.loads((workspace / ".imrane/work/exports/lesson.json").read_text(encoding="utf-8"))
    assert set(exported) == {"schema_version", "kind", "lesson"}
    assert "brief" not in exported and "project" not in exported
    # Governance cannot read nested business data; exercise the actual CLI boundary.
    child_payload = workspace / "demo-client/private.json"
    child_payload.write_text("{}", encoding="utf-8")
    command("create", "--input", str(child_payload), expected=2)
    verification = {"ok": True, "synthetic": True, "network_calls": 0, "existing_workspace_files_modified": False, "completed_at": stamp(), "operation_count": len(events), "stage": final["record"]["stage"], "metrics": final["metrics"], "oracle": {"maximum_contribution_price": profit_price, "maximum_revenue_prices": revenue_prices}, "negative_controls": ["standard skip blocked", "missing review blocked", "missing handoff blocked", "unreviewed lesson blocked", "material input blocker enforced", "HTML escaped", "nested client input rejected"], "board": str(board_path), "board_sha256": hashlib.sha256(board_path.read_bytes()).hexdigest(), "limitations": ["Synthetic duration is instrumentation evidence, not measured productivity gain", "Escaped errors unmeasured", "No native Codex/Claude autoload or macOS host test"]}
    (output / "events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")
    (output / "verification.json").write_text(json.dumps(verification, indent=2), encoding="utf-8")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
