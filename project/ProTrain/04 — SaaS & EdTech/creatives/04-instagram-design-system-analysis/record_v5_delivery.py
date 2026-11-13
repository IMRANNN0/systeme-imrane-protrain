from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
component = root.parent.parent
lane = component.parent
v5 = component/'creatives/03-static-01-campus-confusion/v5'
image = v5/'Creative01V5.png'
sha = hashlib.sha256(image.read_bytes()).hexdigest()
checks = json.loads((v5/'render-checks.json').read_text(encoding='utf-8'))
assert checks['academicRasterCount'] == 5 and checks['codeDrawnAcademicSymbols'] == 0
assert checks['pixelStability']['changedOutsideAcademicCircles'] == 0
assert all(checks['exactCopy'].values()) and checks['v4Preserved']
inventory = json.loads((root/'inventory-measurements.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest() == f['sha256_before'] for f in inventory['inventory'])
assets = []
for p in sorted((v5/'assets').glob('generated-*.png')):
    assets.append({'file':'assets/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(assets) == 5
review = {
    'date':'2026-11-13','status':'ACTUAL_V5_PREVIEW_REVIEWED_AWAITING_IMRAN',
    'full_and_phone_images_viewed':True,'sha256':sha,
    'asset_origin':'Built-in ImageGen, five independent transparent photographic raster assets; full exact prompts and original saved paths in imagegen-provenance.json.',
    'observed':['Laptop, flask, brass scales, calculator and open book replaced five vector symbols in their original circles.','Arabic/French full and phone reading remains identical to V4.','No clipped objects or visible original flag remnants.','Original logo/student/photo/ribbon layout/footer remain visually unchanged; pixel comparison confirms zero differences outside circles.'],
    'technical_checks':checks['pixelStability'],'all_originals_unchanged':True,
    'limitations':['Info object is smallest in locked circle; tiny field names remain secondary at phone size.','Objects are illustrative generated assets, not real Match recommendations or product proof.','Existing hybrid raster plate, source softness, brand fallback fonts and historical footer limitations remain.'],
    'generated_assets':assets,'owner_approval':False,'publication':False,
}
(v5/'controller-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

system = component/'creatives/static-ad-system'
path = system/'active-creative.json'
active = json.loads(path.read_text(encoding='utf-8'))
old_preview = active.get('current_preview',{})
if old_preview.get('version') == 'V4':
    active.setdefault('previous_previews',[]).append(old_preview)
active['status'] = 'V5_GENERATED_CHOICE_IMAGES_AWAITING_IMRAN_REVIEW'
active['authoritative_source'] = 'Latest owner requests generating the five visual assets as images and then inserting them into the existing creative'
active['production_authorization'] = 'Same Creative01 revision: actual ImageGen images replace SVG academic symbols; no new layout, alternatives, Creative02 or publication'
active['reference_system_request']['copy'] = 'Exact current hook/promise/CTA rendered in V4 and preserved byte-for-byte visually in V5 outside circles'
active['current_preview'] = {'version':'V5','export':'creatives/03-static-01-campus-confusion/v5/Creative01V5.png','source':'creatives/03-static-01-campus-confusion/v5/Creative01V5.html','sha256':sha,'status':'AWAITING_IMRAN_REVIEW','method':'Five actual ImageGen transparent PNG objects composited into existing academic circles; no code-drawn academic symbols','provenance':'creatives/03-static-01-campus-confusion/v5/imagegen-provenance.json','limits':review['limitations']}
path.write_text(json.dumps(active,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

path = system/'protrain-lessons.json'
lessons = json.loads(path.read_text(encoding='utf-8'))
cases = lessons.setdefault('subsequent_cases',[])
if not any(x.get('creative') == 'Creative01V5' for x in cases):
    cases.append({'creative':'Creative01V5','date':'2026-11-13','status':'AWAITING_IMRAN_REVIEW','artifact':'creatives/03-static-01-campus-confusion/v5/Creative01V5.png','sha256':sha,'owner_feedback':'Replace code-drawn academic symbols by generated images and place them into the creative','correction':'Five actual built-in ImageGen raster assets generated, saved with provenance and composited inside original circles','review':review,'owner_approval':False})
entries = lessons.setdefault('revision_lessons',[])
lesson_id = 'PT13_GENERATED_CHOICE_ASSETS'
if not any(x.get('id') == lesson_id for x in entries):
    entries.append({'id':lesson_id,'source_case':'Creative01V4','recorded_on':'2026-11-13','failure':'Generic flat SVG academic symbols did not provide the generated-image treatment the owner wanted','prevention':'When this owner requests generated visuals, invoke ImageGen for the actual raster assets first, inspect and save them, then composite into the established template; distinguish asset origin from the composition engine','review_question':'Are these academic visuals actual generated images, and do they retain readability and photographic coherence at phone size?','scope':'This ProTrain circle treatment; not a blanket rejection of SVG or editable code typography','correction_implemented':'V5 uses five actual generated PNGs, no academic symbol paths. Zero changed pixels outside the five existing circles.','status':'CORRECTED_AWAITING_IMRAN_REVIEW'})
path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker = '## Creative01 V5 actual generated choice images — 13 November 2026'
note = f'''## Creative01 V5 actual generated choice images — 13 November 2026

- Stage: latest owner explicitly requests generate visualassets as images then insert into samecreative. OneV5 completed and viewedfull+phone. Finalcreative approvalpending; noCreative02/alternatives/launch.
- Lastverified: `04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v5/Creative01V5.png`,1080x1350 SHA256{sha}. Phone360x450; samefolder HTML/render/sourceZIP/comparison/review/provenance.
- Actualgeneration:5independent builtinImageGen calls withtransparentbackground created laptop, glassflask, brassscales, calculator andopenbook. OriginalgeneratedPNGs copiedunchangedfromCODEXgenerated_images into v5/assets/generated-*.png. RGBA1254x1254alpharange0..255. Exactprompts/sourcepaths/hashrecords retained. No CLI fallback, externalAPIrunner orSVGsubstitution.
- Controlledrevision:5SVGacademicpath symbols replaced by5rasterimages in samecirclepositions with sameexistingcovers/labels. ExactH/P/C andfonts loaded; renderer verifies13,687changedpixels insidecircles, ZEROoutside. AllV4archivehashes and20D:/Instagramoriginals preserved. Rootviewed finalfull+phone; noobjectclipping/flagremnants. TinyInfoandfieldlabels remainphone-scale limitation; nopurchaseproof.
- Learning: PT13recordsownerrequest for actualgeneratedimagery, notcodeicons for this treatment; no universalSVGban. Activebrief nowV5; priorV4preview/PNG retained. Noform/matching/report/payment/site/campaign/Creative02/dependencyinstall/networkindexing. Historicalcontactfooter unchanged, notlaunchverified.
- Next: Imranreviews V5PNG and givesapproval/corrections tosamecandidate. Do notlaunch orcreateCreative02 withoutapproval.

'''
path = lane/'.codex/memory/CURRENT.md'
text = path.read_text(encoding='utf-8')
if marker not in text:
    path.write_text(note+text,encoding='utf-8')
path = lane/'.codex/memory/DECISIONS.md'
text = path.read_text(encoding='utf-8')
if marker not in text:
    path.write_text(text+'\n\n'+marker+'\n\nOwner explicitly requires actualgeneratedimage assets for thefiveacademicvisuals, thencompositinginto samecreative. V5does this; nofinalapproval/Creative02/launch. Preserve layout/logo/copy and V4history.\n',encoding='utf-8')
path = lane/'.codex/memory/CONTEXT_INDEX.md'
text = path.read_text(encoding='utf-8')
if 'v5/Creative01V5.png' not in text:
    path.write_text(text+'\n\n## Creative01 V5 generated image assets — 13 November 2026\n\n- `04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v5/Creative01V5.png`: five actualImageGenPNGs in samecirclepositions, exactcopy/layoutpreserved. Adjacentimagegen-provenance.json contains prompts/origins; render-checks verifies zerooutside-circlepixeldifferences. Ownerreviewpending.\n',encoding='utf-8')
print(json.dumps({'status':'V5_AWAITING_IMRAN','sha256':sha,'actual_generated_images':len(assets),'originals_preserved':True}))
