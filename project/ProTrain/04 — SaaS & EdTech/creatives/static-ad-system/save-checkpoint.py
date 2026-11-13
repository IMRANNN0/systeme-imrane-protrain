"""Save scoped project continuity and sanitized shared-workflow continuity."""
from pathlib import Path
import json
import os
import subprocess

COMPONENT = Path(__file__).resolve().parents[2]
LANE = COMPONENT.parent
WORKSPACE = Path("{{IMRANE_WORKSPACE_ROOT}}")


def prepend_once(path: Path, marker: str, text: str) -> None:
    existing = path.read_text(encoding="utf-8-sig")
    if marker not in existing:
        path.write_text(text + "\n\n" + existing, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = path.read_text(encoding="utf-8-sig")
    if marker not in existing:
        path.write_text(existing.rstrip() + "\n\n" + text + "\n", encoding="utf-8")


project_marker = "## Static image system and first-six preparation - 13 November 2026"
project_text = """## Static image system and first-six preparation - 13 November 2026

### Restart checkpoint
- Stage: durable static-ad workflow installed and current six briefs prepared; pixel production awaits actual report evidence for first-priority03. User explicitly rejected prior static ad and asked retain mistakes for future work, with sanitized reuse in other projects.
- Automatic consultation: workspace AGENTS static-ad directive -> {{IMRANE_WORKSPACE_ROOT}}/.agents/skills/static-ad-creative-system/SKILL.md; component AGENTS -> creatives/static-ad-system/protrain-lessons.json, brand sources and six-concepts.json. Instruction-based loading, not an image-tool interceptor; catalog hot reload not claimed.
- Ten retained failures: generic hook, absent profile/reason mechanism, passive dominant portrait, unclear floating folder, meaningless kicker/underline, template motif accumulation, competing text hierarchy, vague next action, decoration substituted for proof, technical-only review/absent original branding. Preferences apply to observed treatments, no universal portrait/paper/underline bans.
- The prior protrain-match-profile-a01-v3-final.png is REJECTED_BY_OWNER for creative direction. Historical technical checks remain valid but do not establish approval. PNG unchanged; review/delivery metadata now records rejection.
- Latest owner batch supersedes prior six:01wrongchoice,02personalization,03insideReport,04academicFit,05parent,06whyPay. Purchase confirmed; budget unknown. Owner priority03then01then06, others unranked. Source hooks preserved separately from proposals.02uses explicitly fictional14/20 equal averages and branches, no actual Match outputs inferred. Original18image plan remains a possible backlog, not approved spend or completed production.
- Local outputs: creatives/static-ad-system/{protrain-lessons.json,six-concepts.json,batch-01-briefs.html,03-preflight.json,preparation-review.json,system-verification.json,shared-skill-handoff.json}. Exact brand tokens/source assets retained. Corporate logo+plain Match text planned; no separate approved Match logo supplied. Cairo local font verified; Poppins file unconfirmed.
- Proof gap: no report screenshot/PDF in local scoped material or supplied by user; connected Drive searches returned scripts document only, public landing fetch failed.03and06require genuine report evidence. User03-first sequencing holds all pixel production; conditional briefs remain useful. Exact destination flow needed to finalize truthful CTA. Price omitted from images by explicit owner instruction; paid report/free form distinction maintained. Website2free wording not promoted over approved terms.
- Shared handoff: owner explicitly authorized reuse of transferable rules. Only sanitized skill text transferred; no client names, prices, business memories, transcripts or images. Canonical and hash-tracked Claude mirror match SHA256c83d3d4a8d5b124abe532584f082629f9780df7a0a6cd2915ae8c007e2abfcab. Scoped routing installed in workspace and component AGENTS.
- Validation: actual rejected PNG viewed and hash preserved; ten lessons and six briefs independently reviewed; actual03preflight shows missing evidence. Shared YAML parsed using existingjs-yaml. Official Python validator lackedPyYAML; no successful official-validator claim. Worker attempted temporary-target dependency fetch before stop instruction; DNS failed and nothing installed. No new dependency, generated ad, publication, campaign, spend, external message or network indexing.
- Next action: receive actual anonymized report screenshot/PDF, inspect one recommendation/reason and real destination, then produce03 with original logo and editable text layers. Budget/payment/purchase tracking are later launch checks; do not block preparation on budget or invent performance results.
"""
mem = LANE / ".codex/memory"
prepend_once(mem / "CURRENT.md", project_marker, project_text)
append_once(mem / "DECISIONS.md", "## Static creative retention and Purchase batch - 13 November 2026", """## Static creative retention and Purchase batch - 13 November 2026

Owner requests durable before/after static-image review, local retention of actual ProTrain mistakes, and sanitized reusable rules for other projects. Implemented canonical static-ad-creative-system skill plus inherited workspace routing and component-specific sources. Prior static creative direction is rejected; legibility is not acceptance. Latest six-brief batch uses Purchase, price-free image copy,03-first actual-report evidence and then01/06priority; no budget or launch authorization. Preserve source hooks and proposed edits separately; no fabricated screenshots. See component creatives/static-ad-system/shared-skill-handoff.json and system-verification.json. No client-specific facts transferred to shared skill.""")
append_once(mem / "CONTEXT_INDEX.md", "## Static image workflow and current six briefs", """## Static image workflow and current six briefs

- `04 — SaaS & EdTech/AGENTS.md`: automatic static-work source loading.
- `04 — SaaS & EdTech/creatives/static-ad-system/protrain-lessons.json`: ten retained failures and owner rejection status.
- Same folder `six-concepts.json` and `batch-01-briefs.html`: current Purchase batch, priority03/01/06 and source/proposed hooks.
- Same folder `03-preflight.json`, `system-verification.json`, `preparation-review.json` and `shared-skill-handoff.json`: genuine proof gap, inspected state and authorized sanitized transfer.
- Shared method: `{{IMRANE_WORKSPACE_ROOT}}/.agents/skills/static-ad-creative-system/SKILL.md`. No new image generated; start03when real report source arrives.""")
append_once(mem / "PROJECT_CONTEXT.md", "## Static advertising image method - 13 November 2026", """## Static advertising image method - 13 November 2026

Use component AGENTS and local static-ad-system lessons before/after future static advertising work. Shared generic static-ad-creative-system holds transferable process only. Original first static image was rejected for creative direction; never infer approved styling from its technical checks. Current batch goal is Purchase; evidence-led03is first and awaits actual report. These workflow changes do not establish report accuracy, payment readiness, campaign performance or publication.""")

gov = WORKSPACE / ".codex/memory"
gov_marker = "## Standing static-ad creative workflow - 13 November 2026"
gov_text = """## Standing static-ad creative workflow - 13 November 2026

### Restart checkpoint
- Stage: owner-requested generic static-ad skill installed and linked from workspace AGENTS. Canonical .agents/skills/static-ad-creative-system/SKILL.md plus identical hash-tracked .claude/skills view. Installation manifest .imrane/static-ad-creative-system-install.json.
- Method: consult selected project's brand/claims/retained feedback; define specific hook and visual argument before generation; distinguish true product evidence from illustration; choose exact original branding/editable text composition from start; inspect actual export for persuasion and technical fidelity separately. Retain local feedback and owner acceptance separately from technical checks and unmeasured performance.
- Scope: relevant static advertising work in this workspace. Instruction-based consultation, not technical image-tool interception or verified catalog hot reload. No blanket stylistic bans or forced fixed variant counts.
- Validation: unchanged staged/canonical/mirror SHA256c83d3d4a8d5b124abe532584f082629f9780df7a0a6cd2915ae8c007e2abfcab; existingjs-yaml parsed frontmatter; scoped routing/source references and installer idempotence checked; controller reviewed sanitized instructions. Official Python validator lacksPyYAML, no successful official-validator claim. No new dependency installed.
- Privacy: owner explicitly authorized transferable lessons; only reviewed generic rules copied. Client identities, offers, assets, transcripts and business memories remain in their selected lane. No network indexing, publication, campaign, contact or spend.
- Next action: future relevant tasks load shared skill and selected project notes, then apply only checks useful for that brief. Keep newly observed failures local unless reviewed for generic reuse.
"""
prepend_once(gov / "CURRENT.md", gov_marker, gov_text)
append_once(gov / "DECISIONS.md", "## Standing static-ad workflow - 13 November 2026", """## Standing static-ad workflow - 13 November 2026

Owner requested a reusable method for learning from rejected static creative and consulting those lessons before and after future image-ad work. Installed a new owner-authored generic static-ad-creative-system skill and scoped workspace AGENTS rule, preserving imported skills and client boundaries. Canonical source and hash-tracked mirror are governed by .imrane/static-ad-creative-system-install.json. No technical interception, aesthetic universal ban or external action authorized by this workflow.""")
append_once(gov / "CONTEXT_INDEX.md", "## Static-ad creative workflow", """## Static-ad creative workflow

- `.agents/skills/static-ad-creative-system/SKILL.md`: reusable concept, source-evidence, production and actual-output review method.
- `AGENTS.md` static advertising image section: inherited consultation directive.
- `.imrane/static-ad-creative-system-install.json`: canonical/mirror hashes and installation scope.
- Project-specific lessons and evidence remain in the selected lane, not governance.""")

payload = {"dispatch_id": "4a5db9a00ca14cf196cdcf5ef7308d18", "status": "finished", "worker_id": "/root/static_creative_system"}
result = subprocess.run(["python", str(WORKSPACE / "tools/imrane-route.py"), "--workspace", str(WORKSPACE), "--cwd", str(COMPONENT), "--session-id", "protrain-creative-system-01a1d2f3"], input=json.dumps(payload), text=True, encoding="utf-8", capture_output=True, timeout=20)
print(result.stdout)
print(result.stderr)
result.check_returncode()
for scope in ("protrain", "governance"):
    result = subprocess.run(["python", str(WORKSPACE / "tools/systeme-imrane/scripts/imrane.py"), "snapshot", "--workspace", str(WORKSPACE), "--id", scope], text=True, encoding="utf-8", capture_output=True, timeout=30)
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()
    snapshot = json.loads((WORKSPACE / "tmp/codex-session/projects" / scope / "latest-snapshot.json").read_text(encoding="utf-8-sig"))
    assert set(snapshot["memory"]) == {"CURRENT.md", "DECISIONS.md", "CONTEXT_INDEX.md", "PROJECT_CONTEXT.md"}
    assert (project_marker if scope == "protrain" else gov_marker) in snapshot["memory"]["CURRENT.md"]
print("Scoped continuity and both four-memory snapshots verified; no network refresh")
