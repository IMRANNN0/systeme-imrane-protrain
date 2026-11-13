"""Record read-only landing QA and preserve existing project memories."""
from pathlib import Path
import json
import subprocess

COMPONENT = Path(__file__).resolve().parents[2]
LANE = COMPONENT.parent
MEMORY = LANE / ".codex/memory"
WORKSPACE = Path("{{IMRANE_WORKSPACE_ROOT}}")


def add(path: Path, marker: str, text: str, prepend=False):
    existing = path.read_text(encoding="utf-8-sig")
    if marker in existing:
        return
    content = text + "\n\n" + existing if prepend else existing.rstrip() + "\n\n" + text + "\n"
    path.write_text(content, encoding="utf-8")


marker = "## Landing branding and read-only QA - 13 November 2026"
add(MEMORY / "CURRENT.md", marker, """## Landing branding and read-only QA - 13 November 2026

### Restart checkpoint
- Stage: current landing inspected read-only; five exact naming changes prepared. Implementation blocked because actual editable landing source is absent. User explicitly forbids form entry/submission, matching/report/payment/database mutation, deploy/publish and unrelated-page edits. Do not clone production or patch archived homepage HTML as a workaround.
- Target: https://protraincompany.com/en/etudier-en-france/campus-france. User explicitly authorizes proposed identity ProTrain Match by ProTrain Company, preserving current2free/7full/199DH offer and value proposition. This instruction resolves page-task commercial scope; it does not authorize backend or funnel changes.
- Current page: H1Which programs in France should you choose on Études en France? Lead explains profile-based7programs with2free. No visible Match name. Display199DH includingVAT, online/PDF. FAQ says last2of7free,5unlocked by payment. Current body promises private email link; actual delivery was not tested.
- Actual browser checks: IAB desktop1440x1000 and mobile390x844. MainCTA See my programs ->#o_shortlist_start works. First empty stage inspected; other3stage structures DOM only. DefaultBaccalaureate/L1 form has12required fields; no values edited, no Next/Submit clicked. FormPOST/en/etudier-en-france/campus-france/start observed only. FAQoffer/free/consulting accordions and mobilemenu open/close checked. General link destinations read; phone/WhatsApp/contact actions not activated. No consolewarn/error entries captured; no full error-free claim.
- Layout: no observed horizontal overflow; mobile controls stack and mainCTA visible. Captured mobilemenu open while toggle aria-expanded remainedfalse. Requiredbacstream label lacks adjacentfield-styleasterisk. Fixedconsultationbar competes with product action; no funnel change made. Existing15November2026deadline conflicts with current indexed officialCampusFranceMaroccalendar15December2026for its connected formations; directdetailedpagefetch403, officialsearchresultread. Deadline correction needs separate approval, not silently changed.
- Source inventory:1388scoped paths, no actualOdoo module/controller/view or landingfrontend source; no attached worktree/artifact. Existingpackage is Remotionvideo, not applicable to landing. Historicalediting-system/brand/website-source.html untouched. No landing build/lint/postchange QA possible; unrelatedvideo checks not run.
- Deliverables:04 — SaaS & EdTech/landing-page-qa/2026-11-13/{qa-report.html,qa-report.json,branding-proposal.json,source-inventory.json,desktop-dom.json,mobile-dom.json,mobile-form.json,branding-targets.json,faq-offer.json,faq-consulting.json,console-warnings-errors.json,screenshots/}. Six saved screenshots inspected/accepted. Fullpage07contains scrollreveal/stitching artifacts and is rejected as layout evidence; do not infer real blank sections. Desktopcaptures soft; exact text checked in currentDOM.
- Proposedonly: replaceexistingherokicker with approvedidentity; nameacademictool inlead; nameMatch informhelper/reportFAQ; separateoptionalProTrainCompany humanservice inFAQ. KeepH1,2/7/199,currentCTA/action/formfields and allfunctionality. Zero website/source edits. No simulated afterscreenshots or deploy.
- Validation: controller reviewed liveUI, savedcaptures, actualDOM/formmetadata and5precise proposals; sourceworker independently inventoriedlane. CUAcompletion summary sent and viewportoverride reset. Allprohibited-actionflags false. Nodependencyinstall/networkindexing/externalmessages.
- Next action: user provides authentic editable landing module/template checkout and localpreview/build/lint instructions. Then implement the alreadyauthorized branding-only five text edits and repeat safe empty-formdesktop/mobileQA. Seek separate scope for deadline/formlabel/sharednav/CTA-funnel changes.
""", prepend=True)
add(MEMORY / "DECISIONS.md", "## Landing identity and safe QA scope - 13 November 2026", """## Landing identity and safe QA scope - 13 November 2026

Owner selects ProTrain Match by ProTrain Company for the existing English Campus France landing, with2programsfree/7full/199DH unchanged and human consulting distinct. Only local branding edits authorized after read-only inspection; form filling, submission, fake profiles, matching/report generation, payments/customer mutations, deployment and unrelated pages expressly prohibited. Source unavailable: preserve live site, propose exact text edits, request actual source rather than reconstruct. Five proposed edits and read-only audit saved in component landing-page-qa/2026-11-13. Deadline and shared-navigation/formlabel/funnel changes require separate scope.""")
add(MEMORY / "CONTEXT_INDEX.md", "## Campus France landing branding and QA", """## Campus France landing branding and QA

- `04 — SaaS & EdTech/landing-page-qa/2026-11-13/qa-report.html`: readable original-page summary, six inspection steps, screenshots, findings and limits.
- Same folder `qa-report.json`, `branding-proposal.json`, `source-inventory.json`: structured current evidence, five proposed text-only changes and missing source limitation.
- `screenshots/01` through `06` accepted; capture07 rejected for unrevealed animation/stitching artifacts. Do not treat raw downloaded DOM/archive as editable landing source.
- Actual landing source/build still unavailable; no form action, backend call, payment or deployment tested.""")
add(MEMORY / "PROJECT_CONTEXT.md", "## Campus France landing scope - 13 November 2026", """## Campus France landing scope - 13 November 2026

The English landing is live at https://protraincompany.com/en/etudier-en-france/campus-france. Owner requests product identity ProTrain Match by ProTrain Company and expressly preserves current2free/7full/199DH structure. Actual page source is not in the provided client lane; Remotion code and archival homepage HTML are not its implementation. Current read-only QA and exact proposed branding edits are in the component landing-page-qa/2026-11-13. Product/backend behavior and purchase flow were not exercised.""")

payload = {"dispatch_id": "53b6c7d33c1b46c2aa858dbc38385e77", "status": "finished", "worker_id": "/root/landing_source_review"}
result = subprocess.run(["python", str(WORKSPACE / "tools/imrane-route.py"), "--workspace", str(WORKSPACE), "--cwd", str(COMPONENT), "--session-id", "protrain-landing-qa-01a1d2f3"], input=json.dumps(payload), text=True, encoding="utf-8", capture_output=True, timeout=20)
print(result.stdout)
print(result.stderr)
result.check_returncode()
result = subprocess.run(["python", str(WORKSPACE / "tools/systeme-imrane/scripts/imrane.py"), "snapshot", "--workspace", str(WORKSPACE), "--id", "protrain"], text=True, encoding="utf-8", capture_output=True, timeout=30)
print(result.stdout)
print(result.stderr)
result.check_returncode()
snapshot = json.loads((WORKSPACE / "tmp/codex-session/projects/protrain/latest-snapshot.json").read_text(encoding="utf-8-sig"))
assert len(snapshot["memory"]) == 4
assert marker in snapshot["memory"]["CURRENT.md"]
print("ProTrain checkpoint and four-memory snapshot verified; no network indexing")
