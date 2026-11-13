"""Record this analysis milestone while retaining all prior project evidence."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
component = root.parent.parent
lane = component.parent
system = component/'creatives/static-ad-system'
active_path = system/'active-creative.json'
lessons_path = system/'protrain-lessons.json'
active = json.loads(active_path.read_text(encoding='utf-8'))
lessons = json.loads(lessons_path.read_text(encoding='utf-8'))
baseline = {k:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest() for k,v in lessons.items()}
active['reference_system_request'] = {
    'recorded_on':'2026-11-13',
    'status':'REFERENCE_ANALYSIS_COMPLETE_AWAITING_IMRAN_APPROVAL',
    'owner_instruction':'Reverse engineer D:/Instagram existing identity; select one existing reference; first deliver analysis/fixed-vs-variable/template proposal/missing assets and stop before reconstruction or V4.',
    'proposed_reference':'D:/Instagram/imgi_32_656179671_18077289212628783_6745418022262791529_n.webp',
    'report':'creatives/04-instagram-design-system-analysis/design-system-analysis.html',
    'proposal':'creatives/04-instagram-design-system-analysis/template-proposal.json',
    'approval_scope':'Proposed reference, badge-variable scope and explicit exceptions require owner approval. No new art direction, alternatives, V4 reconstruction or Creative02 authorized now.',
    'copy':'Current hook/promise/CTA unchanged and unrendered in new reference system.',
    'prior_versions':'Historical V1/V2 preserved. Prior technical checks do not approve them or the proposed reference.',
}
lesson_id = 'PROTRAIN_EXISTING_IDENTITY_REFERENCE_FIRST_20261113'
entries = lessons.setdefault('reference_system_updates',[])
if not any(x.get('id') == lesson_id for x in entries):
    entries.append({
        'id':lesson_id, 'date':'2026-11-13', 'type':'EXPLICIT_OWNER_WORKFLOW_INSTRUCTION',
        'instruction':'Preserve existing Instagram identity; choose one actual primary reference, lock its fixed elements, expose only approved copy/image/support variables. Do not combine unrelated layouts or introduce decorative redesign.',
        'review_questions':['Is each fixed element traceable to the single approved reference?', 'Are sampled raster values distinguished from official tokens and font identity uncertainty?', 'Were exact mixed-script copy fit and phone export actually inspected before claiming success?', 'Do source flags, agency promises and footer still make sense for France-only academic matching?'],
        'scope':'ProTrain Instagram creative system. Analysis requested now; reference selection and exceptions remain proposed until Imran approves.',
        'observations':'Selected candidate #32 has multi-country flags and agency admission copy; neither becomes a Match claim. Long hook fit, Arabic companion and label/footer treatment unresolved.',
        'artifact':'creatives/04-instagram-design-system-analysis/design-system-analysis.html',
        'production_status':'NOT_RECONSTRUCTED_NO_V4',
    })
active_path.write_text(json.dumps(active,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lessons_path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(hashlib.sha256(json.dumps(lessons[k],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest() == v for k,v in baseline.items())

marker = '## Instagram reference system analysis — 13 November 2026'
checkpoint = '''## Instagram reference system analysis — 13 November 2026

- Stage: analysis complete, awaiting Imran approval of one actual existing reference before template reconstruction/Creative01V4. Latest owner asks faithful existing Instagram identity, not a new direction or hybrid. Earlier Behance directions and V2 are historical/unapproved.
- Done when: 20-original inventory, measured/sample evidence, grouped layouts, single-reference recommendation, locked/variable proposal and missing-source limits delivered; no reconstruction before approval.
- Last verified: D:/Instagram has20raster originals. All20SHA-256 hashes unchanged before/after controller and worker analysis. #32and#29 decoded visually. Source#32=864x1080, flatgreen#017950/yellow#F9CB30/white#FFFFFF; these are compressed-raster samples, not official tokens. Approximate ribbonangle-4.4°, visiblelogo128x123 at(32,30), footer45px. Instagramfont and exacttypeweights/sizes unknown.
- Proposed only: #32orientation-confusion composition, uniform×1.25to1080x1350; no imports from#29 or photo families. Lock paper/logo/shapes/grid/typography/geometry/footer; variableH/P/C/mainimage and explicitly approvedbadgeinteriors. Multi-countryflags need France-only semantic adaptation, not actualrecommendations. Original editableCanva/PSD/AI/SVG provenance not located inInstagram/component; cleanlayers/highreslogo missing.
- Evidence: 04 — SaaS & EdTech/creatives/04-instagram-design-system-analysis/{design-system-analysis.html,template-proposal.json,inventory-measurements.json,reference-32-geometry.json,analysis-review.json,verification.json}. AllJSON/reportlinks/exactcopy/referencehash checks PASS. This is document/data QA only, not futurecreativeRTL/mobileQA. Bounded native measurement worker completed, dispatch3f39e1ebd8e94436bb948382d274eab0 finished.
- Retained latest hook/promise/CTA exactly; active-creative.json gains scopedreference_system_request; lessons append ownerreference-firstinstruction, all previousnodes unchanged. No oldartwork, sharedskill orsource modified; noV4/generation/form/payment/publication/dependencyinstall/networkindexing.
- Next action: Imran approves single#32reference andbadgevariable scope, resolves footer/Matchlabel/Arabicfont exceptions; then reconstruct reference first, compare visually, fit exactcopy and export/review full+phone. Do not silently shrink text or change locked geometry if hookoverflows. Do not startCreative02.

'''
current = lane/'.codex/memory/CURRENT.md'
text = current.read_text(encoding='utf-8')
if marker not in text:
    current.write_text(checkpoint+text,encoding='utf-8')
index = lane/'.codex/memory/CONTEXT_INDEX.md'
text = index.read_text(encoding='utf-8')
if '04-instagram-design-system-analysis/design-system-analysis.html' not in text:
    index.write_text(text+'\n\n## Existing Instagram design system — 13 November 2026\n\n- `04 — SaaS & EdTech/creatives/04-instagram-design-system-analysis/design-system-analysis.html`:20source inventory, groups, measuredcolors/geometry, #32proposed primaryreference, locked/variable layers, missingeditableassets and ownerapprovalstop. NoV4 reconstructed.\n',encoding='utf-8')
decisions = lane/'.codex/memory/DECISIONS.md'
text = decisions.read_text(encoding='utf-8')
decision_marker = '## ProTrain Instagram identity must be reused — 13 November 2026'
if decision_marker not in text:
    decisions.write_text(text+'\n\n'+decision_marker+'\n\nOwner requests reverse engineering the20originals atD:/Instagram, preserving them untouched. Deliver analysis, oneactualreference recommendation, fixed/variable scope, proposedtemplate andmissingassets first, then waitforImranapproval. No newdirection, hybridlayout, reconstruction orCreative01V4 beforeapproval. #32is proposed, not accepted. PreserveexactH/P/C and previouslessons; only approvedcopy/image/designatedsupportcontent mayvary in the future.\n',encoding='utf-8')
receipt={'prior_lesson_nodes_preserved':True,'new_guideline_status':'EXPLICIT_OWNER_INSTRUCTION','reference_status':'PROPOSED_AWAITING_APPROVAL','prior_node_hashes':baseline,'new_node':'reference_system_updates'}
(root/'record-preservation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Analysis checkpoint recorded; historical lesson nodes preserved.')
