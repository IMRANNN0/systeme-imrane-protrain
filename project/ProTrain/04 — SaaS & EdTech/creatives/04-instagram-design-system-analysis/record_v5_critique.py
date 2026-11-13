from pathlib import Path
import json
import hashlib

component = Path(__file__).resolve().parent.parent.parent
lane = component.parent
v5 = component/'creatives/03-static-01-campus-confusion/v5'
findings = [
    'Generated object replacement changes asset origin but leaves the weak visual argument: five floating subject symbols do not clarify how a profile relates to proposed formations.',
    'Passport and dominant portrait signal general study-abroad or visa support more strongly than the specific academic matching tool.',
    'Student photo, miniature still-life cutouts, white badge containers and paper/dotted collage lack a sufficiently coherent relationship in this execution; this is not a blanket rejection of ProTrain identity.',
    'Three heavy tilted text bands compete at mobile scale; the long promise is dense and the CTA has large visual weight.',
    'Arabic/French reading order remains decipherable and was inspected; typography is still optically awkward and heavy. Do not falsely reclassify correct bidi as broken.',
    'Match label and field captions are too small to establish product recognition at phone size.',
    'White CTA ribbon resembles another statement; telephone and historical website footer introduce competing action cues.',
]
review = {'date':'2026-11-13','status':'OWNER_DISSATISFIED_NOT_APPROVED','artifact':'Creative01V5.png','sha256':hashlib.sha256((v5/'Creative01V5.png').read_bytes()).hexdigest(),'actual_full_and_phone_reinspected':True,'findings':findings,'controller_responsibility':'Previous review emphasized technical fidelity and bounded pixel changes, and underweighted persuasion, optical hierarchy and complete composition before delivery. Isolated micro-fixes were delivered without resolving the overall creative problem.','independent_review':'Native bounded reviewer independently viewed full and phone exports and returned the same priority concerns.','scope':'Critique and retained feedback only. No artwork edits, generation, copy rewrite, new layout, Creative02 or publication authorized/performed.','still_valid_evidence':'V5 does use actual ImageGen raster assets, preserves exact copy and original fixed pixels, and retains existing identity. These technical facts do not establish creative approval or performance.'}
(v5/'owner-critique.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
system = component/'creatives/static-ad-system'
path = system/'active-creative.json'
active = json.loads(path.read_text(encoding='utf-8'))
active['status'] = 'V5_OWNER_DISSATISFIED_CRITIQUE_COMPLETE'
active['current_preview']['status'] = 'OWNER_DISSATISFIED_NOT_APPROVED'
active['current_preview']['owner_critique'] = 'creatives/03-static-01-campus-confusion/v5/owner-critique.json'
active['latest_request_scope'] = 'Honest critique only after owner dissatisfaction; no new artwork or layout authorized by this turn'
path.write_text(json.dumps(active,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path = system/'protrain-lessons.json'
lessons = json.loads(path.read_text(encoding='utf-8'))
for case in lessons.get('subsequent_cases',[]):
    if case.get('creative') == 'Creative01V5':
        case['status'] = 'OWNER_DISSATISFIED_NOT_APPROVED'
        case['owner_critique_file'] = 'creatives/03-static-01-campus-confusion/v5/owner-critique.json'
entries = lessons.setdefault('revision_lessons',[])
if not any(x.get('id') == 'PT14_WHOLE_CREATIVE_REVIEW' for x in entries):
    entries.append({'id':'PT14_WHOLE_CREATIVE_REVIEW','source_case':'Creative01V5','recorded_on':'2026-11-13','failure':'Successive localized icon/tool corrections passed technical checks but did not resolve the overall concept, hierarchy or product recognition; owner expressed dissatisfaction with the result and repeated iteration.','prevention':'Before delivery assess the entire exported creative at phone size, separately from tool use, exact-copy checks and pixel preservation. Inspect a clear viewer problem, product-specific meaning, intentional visual relationship and first-read hierarchy.','review_questions':findings,'scope':'This execution and review process. No general ban on portraits, paper ribbons, generated objects or established ProTrain branding.','status':'OBSERVED_FAILURE_NO_NEW_DESIGN_PRODUCED'})
path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
marker = '## Creative01 V5 owner dissatisfaction and critique — 13 November 2026'
path = lane/'.codex/memory/CURRENT.md'
text = path.read_text(encoding='utf-8')
if marker not in text:
    path.write_text(marker+'\n\n- Stage: owner dissatisfied with V5 and repeated iteration; requests honestcritique only. Rootreinspected actualfull+phone and nativeindependentreviewer concurred. Noartwork generated/edited thisturn.\n- Findings: weakproduct-specificvisualargument; passportdominant/generalstudyabroadsignal; floatingphotographicminis inUI-likecircles lackrelationship; denseheavytiltedtexttiers compete; Matchidentityweak/tiny; contactfooter diffusesCTA. Bidi isdecipherable, notfalselyclassifiedbroken. ActualImageGengeneration/exactcopy/pixelpreservation remainvalidtechnicalfacts, notcreativeapproval.\n- Evidence: `04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v5/owner-critique.json`. Activebrief marksOWNER_DISSATISFIED_NOT_APPROVED; PT14retains whole-creative-review failure withoutdeletingearlierevidence. V5PNGunchanged.\n- Next: explainprioritydiagnosis candidly toImran. Beforeanynewrender, consolidateoneconcretevisualcorrectionproposal withinexistingidentity/currentcopy; anycopy/lockedlayoutchanges need their ownreview. No automaticregeneration/Creative02/publication.\n\n'+text,encoding='utf-8')
print('Critique saved; V5 artwork unchanged, owner dissatisfaction recorded, previous technical evidence retained.')
