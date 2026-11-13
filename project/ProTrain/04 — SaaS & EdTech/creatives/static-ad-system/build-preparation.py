"""Produce a readable brief and record the inspected workflow state."""
from pathlib import Path
import hashlib
import html
import json

HERE = Path(__file__).resolve().parent
COMPONENT = HERE.parents[1]
WORKSPACE = Path("{{IMRANE_WORKSPACE_ROOT}}")
batch = json.loads((HERE / "six-concepts.json").read_text(encoding="utf-8-sig"))
lessons = json.loads((HERE / "protrain-lessons.json").read_text(encoding="utf-8-sig"))
skill = WORKSPACE / ".agents/skills/static-ad-creative-system/SKILL.md"
mirror = WORKSPACE / ".claude/skills/static-ad-creative-system/SKILL.md"
original = COMPONENT / "creatives/02-match-profile-a01/protrain-match-profile-a01-v3-final.png"
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert len(batch["concepts"]) == 6
assert batch["priority_order"] == ["03", "01", "06"]
assert len(lessons["lessons"]) == 10
assert digest(skill) == digest(mirror)
assert digest(original) == lessons["source"]["sha256"]
assert str(skill).replace("\\", "/") in (WORKSPACE / "AGENTS.md").read_text(encoding="utf-8-sig")
assert "protrain-lessons.json" in (COMPONENT / "AGENTS.md").read_text(encoding="utf-8-sig")
assert "protrain" not in skill.read_text(encoding="utf-8").lower()

preflight = {
    "date": "2026-11-13", "concept": "03", "objective": "Purchase",
    "method": "Installed static-ad-creative-system applied before generation",
    "consulted": [str(skill), "protrain-lessons.json", "six-concepts.json", "../../editing-system/brand/README.md"],
    "hook_source": batch["concepts"][2]["source_hook"],
    "hook_proposal": batch["concepts"][2]["proposed_final_hook"],
    "visual_argument": "Let the viewer inspect an actual recommendation and the explanation attached to it",
    "composition": "Dominant real report crop and exact editable text, original corporate logo plus Match product label, one next action",
    "sources_ready": ["Corporate logo", "Brand tokens", "Cairo Arabic font"],
    "required_before_production": ["Genuine report screenshot/PDF", "Actual destination flow to select a truthful CTA"],
    "source_handling": "Inspect the supplied asset; retain genuine report text and omit personal details from the ad",
    "next_action": "Read actual supplied report, select one clear recommendation reason and finalize the concept before creating pixels",
    "status": "WAITING_FOR_PRODUCT_EVIDENCE", "images_generated": 0,
    "budget": "Unspecified; does not block creative preparation", "launch_authorized": False,
}
(HERE / "03-preflight.json").write_text(json.dumps(preflight, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

descriptions = {
    "01": "Rendre visible une erreur de choix précise, puis montrer une raison liée au dossier.",
    "02": "Deux exemples pédagogiques à 14/20, avec deux filières. Aucun résultat du produit inventé.",
    "03": "Un extrait réel du rapport, avec une recommandation et sa raison lisibles.",
    "04": "Comparer le dossier aux exigences réelles d’un programme, sans inventer de critères.",
    "05": "Un échange parent–étudiant autour d’une raison concrète, sans faux témoignage.",
    "06": "Montrer ce que le rapport apporte à la recherche personnelle avec un vrai exemple.",
}
escape = html.escape
sections = []
for concept in batch["concepts"]:
    number = concept["id"]
    sections.append(f"<section><h2>{number} · {escape(concept['name'])}</h2><p class='hook' lang='ar' dir='rtl'>{escape(concept['proposed_final_hook'])}</p><p>{escape(descriptions[number])}</p><details><summary>Hook source conservé</summary><p lang='ar' dir='rtl'>{escape(concept['source_hook'])}</p></details><p><strong>CTA proposé :</strong> <span lang='ar' dir='rtl'>{escape(concept['cta']['proposed'])}</span></p><p class='note'>CTA à vérifier avec la destination réelle. Les propositions restent des briefs, pas des publicités finalisées.</p></section>")
document = """<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ProTrain Match · Batch statique 01</title><style>body{margin:0;background:#F6F4EE;color:#0F2A1F;font:17px/1.65 Arial,sans-serif}main{max-width:900px;margin:auto;padding:40px 24px}h1{font-size:36px;line-height:1.2}h2{font-size:23px;margin-top:0}section{padding:26px 0;border-top:1px solid #bfcac3}.hook{font-size:29px;line-height:1.6;font-weight:700}.note,summary{font-size:14px;color:#4A5C54}a{color:#0A6B43}header{margin-bottom:36px}strong{font-weight:700}</style><main><header><p>ProTrain Match · 13 novembre 2026</p><h1>Six briefs de static ads</h1><p><strong>Objectif : Purchase.</strong> Priorité de production : 03, puis 01 et 06. Budget à définir.</p><p>La production de 03 attend un vrai extrait du rapport. Aucun visuel publicitaire n’a été généré dans ce batch.</p><p>Les dix erreurs du premier essai sont conservées dans <a href="protrain-lessons.json">la note du projet</a>. Les choix ci-dessous sont des hypothèses créatives à tester.</p></header>""" + "".join(sections) + "<footer><p>Sources complètes et conditions : <a href='six-concepts.json'>briefs structurés</a> · <a href='03-preflight.json'>préparation de 03</a></p></footer></main></html>"
(HERE / "batch-01-briefs.html").write_text(document, encoding="utf-8")
verification = {
    "date": "2026-11-13", "reviewer": "Root controller, independent of drafting worker",
    "shared_skill_sha256": digest(skill), "canonical_mirror_match": True,
    "automatic_consultation": {"mechanism": "Inherited workspace AGENTS directive plus component-specific AGENTS sources", "scope": "{{IMRANE_WORKSPACE_ROOT}} workspace", "tool_interceptor": False, "host_catalog_refresh_verified": False},
    "observed_checks": ["Six briefs parse and include evidence gaps", "Priority03,01,06 preserved", "Ten failures mapped to prevention and review questions", "Client-specific context excluded from shared skill", "Original rejected PNG bytes preserved", "Root and component instructions reference the correct files", "Actual03 preflight created with missing proof visible"],
    "validation": {"yaml": "Parsed using existing js-yaml", "official_python_validator": "Unavailable: PyYAML missing; no successful official-validator claim", "semantic_review": "Distinct ad concepts; owner hooks separate from proposals; technical pass separate from owner acceptance; no universal style bans"},
    "production_status": "Waiting for genuine product evidence; preparation complete", "images_generated": 0,
}
(HERE / "system-verification.json").write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
handoff = {"date": "2026-11-13", "source": "ProTrain-local rejected-image review", "destination": "{{IMRANE_WORKSPACE_ROOT}}/.agents/skills/static-ad-creative-system/SKILL.md", "authorization": "Owner explicitly requested retaining project mistakes and reusing the general method in other projects", "transferred": "Sanitized decision rules only", "excluded": ["Client name", "Product offer and price", "Images", "Transcript", "Business memory", "Campaign data"], "reviewer": "Root controller", "shared_skill_sha256": digest(skill), "network_indexing": False}
(HERE / "shared-skill-handoff.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Validated routing, sanitized shared skill, six briefs, ten lessons, unchanged original PNG; wrote readable brief and actual03 preflight")
