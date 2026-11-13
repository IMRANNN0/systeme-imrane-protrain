"""Build a read-only landing-page audit report from captured evidence."""
from pathlib import Path
from html import escape
import hashlib
import json

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text(encoding="utf-8-sig"))
desktop, mobile = load("desktop-dom.json"), load("mobile-dom.json")
proposal, inventory = load("branding-proposal.json"), load("source-inventory.json")
fields = desktop["forms"][0]["fields"]
required = [{"id": field["id"], "label": field["label"].strip()} for field in fields if field.get("required")]
screens = [
    ("01-desktop-hero.jpg", "Desktop landing and original offer", "1440 × 1000 viewport"),
    ("02-desktop-empty-form.jpg", "Desktop empty first form stage", "No fields edited or Next clicked"),
    ("03-desktop-report-faq.jpg", "Expanded complete-report FAQ", "Read-only accordion interaction"),
    ("04-mobile-hero.jpg", "Mobile landing and main CTA", "390 × 844 viewport"),
    ("05-mobile-empty-form.jpg", "Mobile empty first form stage", "Single-column fields; no input"),
    ("06-mobile-navigation.jpg", "Mobile navigation open", "Opened and closed without following action links"),
]
accepted_screens = []
for filename, title, note in screens:
    path = HERE / "screenshots" / filename
    assert path.is_file() and path.stat().st_size > 0
    accepted_screens.append({"file": "screenshots/" + filename, "title": title, "note": note, "saved_file_inspected": True, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

findings = [
    {"id": "B01", "type": "Branding", "priority": "High", "finding": "No visible ProTrain Match name in the inspected landing text. The visitor sees the agency identity and a matching promise without an explicit product identifier.", "evidence": ["01-desktop-hero.jpg", "04-mobile-hero.jpg", "desktop-dom.json"], "action": "Apply the five proposed naming-only changes in the actual source when available.", "approval": "Branding scope already authorized; actual source required"},
    {"id": "C01", "type": "Content accuracy", "priority": "High", "finding": "The hero states a November 15, 2026 Études en France deadline. Campus France Maroc's currently indexed official calendar states December 15, 2026 at 23:59 Moroccan time for the connected formations it lists. The blanket landing date needs verification against the relevant applicant procedure.", "evidence": ["01-desktop-hero.jpg", "04-mobile-hero.jpg"], "source": "https://www.maroc.campusfrance.org/calendrier-de-la-procedure-de-candidature-20262027", "source_limit": "Official search result consulted on 13 November 2026; direct fetch of the detailed deadline page returned403. This is external content research, separate from captured page UX.", "action": "Confirm the applicable deadline and approve a separate content correction. Do not silently change it in the branding patch.", "approval": "Separate approval required for deadline copy"},
    {"id": "U01", "type": "Offer separation", "priority": "Medium", "finding": "The landing's report offer is clear, but optional human assistance is only mentioned late in the FAQ. Agency consultation links remain prominent, including the fixed mobile bar.", "evidence": ["04-mobile-hero.jpg", "05-mobile-empty-form.jpg", "faq-consulting.json"], "action": "Use explicit tool and separate-service wording in the proposed branding copy. Any consultation CTA hierarchy or funnel change needs separate approval.", "approval": "Naming clarification authorized; funnel changes not authorized"},
    {"id": "A01", "type": "Required-field clarity", "priority": "Low", "finding": "Moroccan bac stream is required in the default Baccalaureate/L1 DOM state, but its visible label lacks the asterisk shown on adjacent required fields.", "evidence": ["02-desktop-empty-form.jpg", "05-mobile-empty-form.jpg", "desktop-dom.json"], "action": "Consider a label-only required marker correction after approval; do not alter field requirements or validation.", "approval": "Outside the naming-only patch"},
    {"id": "A02", "type": "Navigation accessibility state", "priority": "Low", "finding": "The mobile offcanvas was visibly open and had role=dialog and aria-modal=true while its toggle still reported aria-expanded=false.", "evidence": ["06-mobile-navigation.jpg"], "action": "Review the toggle state in the actual shared navigation implementation. Do not modify the shared component under this single-page branding task.", "approval": "Separate shared-navigation scope required"},
]
report = {
    "date": "2026-11-13", "timezone": "Africa/Casablanca", "page": desktop["url"],
    "status": "READ_ONLY_QA_COMPLETE_IMPLEMENTATION_BLOCKED_BY_MISSING_SOURCE",
    "original_page": {
        "headline": desktop["headings"][0]["text"],
        "subheadline": load("branding-targets.json")["hero"]["paragraphs"][1]["text"],
        "identity": "Agency branding; no visible ProTrain Match match in captured body text",
        "offer": "2 programs free; complete report of 7 programs for 199 DH including VAT; online and PDF, as displayed",
        "free_selection_detail": "FAQ says the last 2 of the ranked 7 are shown in full, with the other 5 unlocked by payment",
        "main_cta": {"label": "See my programs", "href": "#o_shortlist_start", "observed": "Same-page navigation reaches the empty first form stage"},
        "promised_journey": "Profile → 2 free programs and private email link → optional 199 DH unlock → full 7 online/PDF. Only landing, empty first stage, FAQ and navigation inspected; outcomes not exercised.",
        "form": {"method": "POST", "action": "/en/etudier-en-france/campus-france/start", "stages": ["Profile", "French and grades", "Wishes", "Contact"], "visually_inspected_stages": ["Profile"], "other_stages": "DOM structure only; no Next or Submit interaction", "required_default_fields_count": len(required), "required_default_fields": required, "default_context": "Page-supplied Morocco nationality/residence, Baccalaureate currentlevel and L1 target; not edited", "optional_fields": ["French test level with No test yet default", "Subject grades", "Additional study fields", "Cities", "Licence field when applicable"]},
    },
    "branding": {"applied_changes": [], "proposed_changes": proposal["edits"], "preserved": proposal["unchanged"]},
    "source": inventory,
    "qa_steps": [
        {"step": 1, "inspection": "Desktop landing, offer and naming", "result": "Loads; clear benefit and 2/7/199 offer; product name missing", "evidence": ["01-desktop-hero.jpg"]},
        {"step": 2, "inspection": "Desktop mainCTA to empty form", "result": "Anchor works; first stage inspected; required marker inconsistency", "evidence": ["02-desktop-empty-form.jpg"]},
        {"step": 3, "inspection": "Free/full report and optional consulting FAQ", "result": "Accordions work; free selection and paid report contents explained; separate-service naming proposed", "evidence": ["03-desktop-report-faq.jpg", "faq-offer.json", "faq-consulting.json"]},
        {"step": 4, "inspection": "Mobile landing", "result": "390 × 844 reflows; main CTA visible, no horizontal overflow; fixed consultation bar competes with product action", "evidence": ["04-mobile-hero.jpg", "mobile-dom.json"]},
        {"step": 5, "inspection": "Mobile empty form", "result": "Single-column controls fit viewport; first 6 controls have 58 px height; later stages not entered", "evidence": ["05-mobile-empty-form.jpg", "mobile-form.json"]},
        {"step": 6, "inspection": "Mobile navigation and action destinations", "result": "Menu opens/closes; destinations inspected. Toggle expansion attribute needs review. Telephone/WhatsApp/contact actions not activated.", "evidence": ["06-mobile-navigation.jpg"]},
    ],
    "layout": {"desktop_viewport": desktop["viewport"], "mobile_viewport": mobile["viewport"], "mobile_overflow_elements": mobile["overflowElements"], "mobile_cta_size": mobile["mainCta"][0]["rect"], "coverage_limit": "One desktop and one mobile viewport, not exhaustive device coverage"},
    "findings": findings,
    "console": {"captured_errors_and_warnings": load("console-warnings-errors.json"), "result": "No captured warning/error entries in this inspection session", "limit": "This does not establish absence of all errors or validate unvisited results/payment routes"},
    "local_checks": {"landing_build": "NOT_RUN_SOURCE_UNAVAILABLE", "landing_lint": "NOT_RUN_SOURCE_UNAVAILABLE", "unrelated_video_checks": "Not run; Remotion checks cannot validate this site", "post_change_qa": "NOT_APPLICABLE_NO_BRANDING_IMPLEMENTATION"},
    "files": {"application_source_modified": [], "audit_artifacts": "Only files in this audit folder were created, plus scoped project continuity notes. The existing website-source archive, videos and unrelated pages were not modified."},
    "needs": ["Actual editable landing template/module checkout and local preview/build/lint instructions", "Separate approval for deadline correction", "Separate approval for form-label/shared-navigation fixes or CTA/funnel changes", "Branding approval is already provided; no repeat permission needed once source exists"],
    "safety": {"personal_data_entered": False, "form_filled": False, "next_clicked": False, "submit_clicked": False, "form_submitted": False, "fake_student_created": False, "matching_triggered": False, "report_generated": False, "payment_made": False, "customer_record_modified": False, "deployed_or_published": False, "remote_content_changed": False},
    "screenshots": accepted_screens,
    "rejected_capture": {"file": "screenshots/07-mobile-full-page.jpg", "reason": "Full-page capture contains unrevealed scroll-animation regions and a fixed-header stitching artifact. Not accepted and not used to infer real page gaps or layout defects."},
    "limits": ["No source or editable local landing; no local branding edits or after-change screenshots", "No functional form validation, later-stage navigation, matching, delivery or checkout tests because prohibited", "The browser keyboard scroll command reported an automation timeout; subsequent DOM showed scrollY0. Not treated as a website error.", "Desktop screenshots are soft; exact copy/attributes were checked against current DOM. No font-fidelity or full accessibility compliance claim.", "Viewport override reset after responsive inspection"],
}
(HERE / "qa-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

e = escape
step_rows = "".join(f"<tr><td>{s['step']}</td><td>{e(s['inspection'])}</td><td>{e(s['result'])}</td></tr>" for s in report["qa_steps"])
edits = "".join(f"<article><h3>{e(edit['id'])}</h3><p><code>{e(edit['target_selector'])}</code></p><p class='label'>Current</p><blockquote>{e(edit['current'])}</blockquote><p class='label'>Proposed, not applied</p><blockquote>{e(edit['proposed'])}</blockquote></article>" for edit in proposal["edits"])
issues = "".join(f"<li><strong>{e(f['id'])} · {e(f['priority'])} · {e(f['type'])}</strong><p>{e(f['finding'])}</p><p>{e(f['action'])}</p>" + (f"<p><a href='{e(f['source'])}'>Official calendar reference</a></p>" if f.get("source") else "") + "</li>" for f in findings)
figures = "".join(f"<figure><img loading='lazy' src='{e(s['file'])}' alt='{e(s['title'])}'><figcaption>{e(s['title'])} · {e(s['note'])}</figcaption></figure>" for s in accepted_screens)
required_list = ", ".join(e(field["label"].replace("\n", " ")) for field in required)
document = f"""<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>ProTrain Match landing QA · 13 November 2026</title><style>body{{margin:0;background:#fff;color:#212529;font:16px/1.6 Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:36px 24px}}h1{{font-size:32px;line-height:1.2}}h2{{margin-top:40px;border-top:1px solid #d5ddd9;padding-top:20px}}h3{{font-size:18px}}a{{color:#0a6b43}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #d5ddd9;text-align:left;vertical-align:top;padding:12px}}blockquote{{margin:8px 0;padding:12px 18px;border-left:3px solid #0a6b43;background:#f6f4ee}}code{{overflow-wrap:anywhere}}article{{margin:24px 0}}.label{{font-weight:bold;margin-bottom:4px}}figure{{margin:24px 0}}img{{max-width:100%;height:auto;display:block;border:1px solid #d5ddd9}}figcaption{{font-size:14px;color:#4a5c54}}.note{{padding:16px;background:#f6f4ee}}@media(min-width:800px){{.screens{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}.screens img{{max-height:750px;width:auto;object-fit:contain;object-position:top}}}}@media print{{details{{display:block}}img{{max-height:650px}}}}</style><main><p>13 November 2026 · Africa/Casablanca</p><h1>ProTrain Match branding and landing-page QA</h1><p class='note'><strong>Read-only inspection complete. No branding edits applied.</strong> The actual landing source is unavailable in the provided workspace. This report proposes exact edits; it is not a reconstructed landing page or a production change.</p><p><a href='{e(report['page'])}'>Inspected landing page</a> · <a href='qa-report.json'>Structured evidence and limits</a> · <a href='branding-proposal.json'>Exact proposed changes</a> · <a href='source-inventory.json'>Source inventory</a></p>
<h2>1. Original page</h2><p><strong>Headline:</strong> {e(report['original_page']['headline'])}</p><p><strong>Subheadline:</strong> {e(report['original_page']['subheadline'])}</p><p>The main action “See my programs” goes to the same-page empty four-stage form. The displayed offer is 2 free programs and 7 in the complete report for 199 DH, including VAT, online and as a PDF. The FAQ specifies that the last 2 of the ranked 7 are free.</p><p>The promise is understandable, while the tool is not identified as ProTrain Match and human consulting remains prominent in the navigation and fixed mobile bar.</p><p><strong>Form:</strong> Profile, French and grades, Wishes, Contact. Only Profile was visually exercised. The remaining stages were inspected in the DOM without opening them. Twelve fields are marked required under the page's default Baccalaureate/L1 state: {required_list}.</p>
<h2>2. Branding changes</h2><p><strong>Applied: none.</strong> Five text-only changes are ready for the actual template. The H1, 2 free / 7 full / 199 DH offer, current CTA labels and destinations, form schema, payment, matching, report logic and other pages remain unchanged.</p>{edits}
<h2>3. Files modified</h2><p>No application or landing-source files were modified. Only audit evidence/proposal/report files in this folder and scoped project continuity notes were written. The existing downloaded homepage reference is not editable landing source and was left intact.</p>
<h2>4. Desktop and mobile QA</h2><table><thead><tr><th>Step</th><th>Inspection</th><th>Result</th></tr></thead><tbody>{step_rows}</tbody></table><p>Desktop viewport 1440 × 1000; mobile 390 × 844. Mobile document width 375 matches client width 375; no observed horizontal overflow. The main mobile CTA is approximately 213 × 58 CSS px. No form inputs were changed.</p><div class='screens'>{figures}</div><p>One full-page capture was rejected because unrevealed scroll-animation regions and fixed-header stitching produced misleading blanks. It is not evidence of a real page layout defect.</p>
<h2>5. Errors, warnings and limits</h2><ul>{issues}</ul><p>No console warning/error entries were captured in this session. No landing build/lint or after-change QA could run without actual source. The unrelated Remotion project was not used as a substitute. Full accessibility, unvisited wizard steps and purchase functionality remain untested.</p>
<h2>6. Required input and approvals</h2><p>Provide the authentic editable landing template/module checkout and its local preview/build/lint instructions to implement the already authorized branding edits. Deadline correction, shared navigation/form-label fixes, or any CTA hierarchy/funnel change require separate scope approval.</p>
<h2>7. Safety confirmation</h2><p>No personal data entered, form fill, Next/Submit click, form submission, fake profile, matching, report generation, payment, customer record mutation, deployment or publication occurred. Live interactions were limited to read-only page capture, anchor navigation, FAQ expansion and mobile menu open/close.</p></main></html>"""
(HERE / "qa-report.html").write_text(document, encoding="utf-8")
print("Saved complete read-only QA report, five proposed edits, six accepted screenshots and explicit source/testing limitations")
