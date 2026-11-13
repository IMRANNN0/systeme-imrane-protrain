"""Run only after the actual V4 full/phone exports have been reviewed."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
component = root.parent.parent
lane = component.parent
v4 = component/'creatives/03-static-01-campus-confusion/v4'
image = v4/'Creative01V4.png'
review = json.loads((v4/'controller-review.json').read_text(encoding='utf-8'))
assert review['full_and_phone_images_viewed'] is True
assert image.exists()
sha = hashlib.sha256(image.read_bytes()).hexdigest()
inventory = json.loads((root/'inventory-measurements.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest() == f['sha256_before'] for f in inventory['inventory'])

system = component/'creatives/static-ad-system'
active_path = system/'active-creative.json'
active = json.loads(active_path.read_text(encoding='utf-8'))
active['status'] = 'V4_REFERENCE32_PREVIEW_AWAITING_IMRAN_REVIEW'
active['authoritative_source'] = 'Latest owner go-ahead to produce one preview matching the selected existing Instagram design'
active['production_authorization'] = 'One Creative01 V4 reference-based preview authorized; no Creative02, alternatives or publication'
active['messaging_status'] = 'Current exact hook/promise/CTA rendered in V4; prior versions preserved'
active['reference_system_request']['status'] = 'REFERENCE32_AUTHORIZED_FOR_ONE_PREVIEW_V4_DELIVERED_AWAITING_REVIEW'
active['reference_system_request']['approval_scope'] = 'Owner said OK create a preview to check design fidelity. This is production permission, not final creative/campaign approval.'
active['current_preview'] = {
    'version':'V4', 'export':'creatives/03-static-01-campus-confusion/v4/Creative01V4.png',
    'source':'creatives/03-static-01-campus-confusion/v4/Creative01V4.html',
    'sha256':sha, 'status':'AWAITING_IMRAN_REVIEW',
    'method':'Hybrid original unchanged reference raster plate plus code-native editable copy/supporting overlays',
    'limits':review['limitations'],
}
active_path.write_text(json.dumps(active,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lessons_path = system/'protrain-lessons.json'
lessons = json.loads(lessons_path.read_text(encoding='utf-8'))
cases = lessons.setdefault('subsequent_cases',[])
if not any(x.get('creative') == 'Creative01V4' for x in cases):
    cases.append({
        'creative':'Creative01V4','date':'2026-11-13','status':'AWAITING_IMRAN_REVIEW',
        'artifact':'creatives/03-static-01-campus-confusion/v4/Creative01V4.png','sha256':sha,
        'scope':'One preview based on selected actual Instagram32, after owner go-ahead. Not a new identity.',
        'method':'Keep original photo/background/logo/footer plate, native editable copy and choice interiors; no new photo generation.',
        'review':review,'owner_approval':False,
    })
lessons_path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker = '## Creative01 V4 reference32 preview — 13 November 2026'
note = f'''## Creative01 V4 reference32 preview — 13 November 2026

- Stage: owner explicitly said OK make onepreview matching selectedInstagramdesign. This authorizes production, not finalapproval. OneCreative01V4 exported and independently viewed full+phone; await Imranfeedback. NoCreative02/alternative/publication.
- Last verified: `04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v4/Creative01V4.png`,1080x1350, SHA256{sha}. EditableHTML/assets/render script/source archive and referencecomparison in samefolder. Controllerreview records actualinspection/limits.
- Method: hybrid nativeeditablecopy/supportoverlays on unchanged original#32rasterplate. Preserve student/photo/paper/logo/halftone/route/ribbon composition and originalcontactfooter. NoImageGen/newphoto. This is not a fullyseparatedPSD; background+subject remainflattened. CurrentexactH/P/C preserved; no firstlineextraquestionmark. Cairo/Poppins brandfallback is notcertifiedIGfont.
- Scope: fivecountryflags replaced byillustrativeacademicchoicecontents in originalcirclepositions. Corporateartunchanged with editableMatchlabel. Historicalwww.protrain.ma/footer retained forreferencefidelity; currentfunnel suitability notverified orupdated. No productUI/recommendation proof oradmissionclaim.
- Preservation: all20D:/Instagramoriginalhashes recheckedunchanged. V1/V2/historicalanalysis remainpreserved. Activecreative recordsV4candidate; lessons append reviewwithout deletingpriorfeedback. Noform/matching/report/payment/site/campaign/dependencyinstall/networkindexing.
- Next action: Imranreviews actualV4PNG againstreference and providesapproval/corrections. Refine onlysamecandidate; resolveoriginaleditableassets/font/footer beforeproductionautomation/launch.

'''
current = lane/'.codex/memory/CURRENT.md'
text = current.read_text(encoding='utf-8')
if marker not in text:
    current.write_text(note+text,encoding='utf-8')
decisions = lane/'.codex/memory/DECISIONS.md'
text = decisions.read_text(encoding='utf-8')
if marker not in text:
    decisions.write_text(text+'\n\n'+marker+'\n\nOwner approves making one reference32-basedpreview to evaluatefaithfulness. Productionpermission only; nofinalcreativeapproval, Creative02 orpublication. Reuseoriginalidentity, keepcurrentexactcopy and preserveoldassets.\n',encoding='utf-8')
index = lane/'.codex/memory/CONTEXT_INDEX.md'
text = index.read_text(encoding='utf-8')
if 'v4/Creative01V4.png' not in text:
    index.write_text(text+'\n\n## Creative01 V4 reference preview — 13 November 2026\n\n- `04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v4/Creative01V4.png` and adjacent HTML, phonepreview, sourceZIP, referencecomparison andcontrollerreview. Owner reviewpending; hybrid originalrasterplate + editabletext/supportoverlays.\n',encoding='utf-8')
print(json.dumps({'v4_sha256':sha,'originals_unchanged':True,'status':'AWAITING_IMRAN_REVIEW'}))
