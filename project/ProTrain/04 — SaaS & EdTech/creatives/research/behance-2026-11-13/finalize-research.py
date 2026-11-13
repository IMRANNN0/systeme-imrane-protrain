from pathlib import Path
import hashlib,json,zipfile

HERE=Path(__file__).parent
PROJECT=HERE.parents[2]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
data=json.loads((HERE/'references.json').read_text(encoding='utf-8'))
lesson_path=PROJECT/'creatives/static-ad-system/protrain-lessons.json'
lessons=json.loads(lesson_path.read_text(encoding='utf-8'))
old={k:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')) for k,v in lessons.items()}
entry={
    'id':'PTM_BEHANCE_RESEARCH_20261113',
    'date':'2026-11-13',
    'owner_instruction':'Research and art direction only. Do not create or modify Static Ads. Wait for Imran to select the visual direction before any further Creative 01 V2 production.',
    'report':'creatives/research/behance-2026-11-13/index.html',
    'observed':'Eleven real Behance projects opened; six selected projects visually inspected beyond covers. Source images and attribution retained. V1 and V2 export hashes preserved.',
    'recommendation':'Editorial decision as proposed foundation; use explanatory relationships for Matching and genuine report excerpts for proof-led angles.',
    'approval':'PROPOSED_AWAITING_IMRAN — not a new owner-approved style rule',
    'source_state':'During research current local brief changed to HOOK → PROMISE → CTA, documented unrendered messaging. Historical V2 two-line correction remains preserved. Report distinguishes source states; neither copy version applied to artwork.',
    'prevention':'Verify subject and actual compositions on direct project pages; search rank and project descriptions do not prove relevance or performance. Keep source observations, proposed adaptations and performance unknowns separate.',
    'review_question':'Does the chosen visual clarify the specific academic decision, retain usable promise/CTA at phone scale, and accurately distinguish illustration from real output?',
    'scope':'This research selection and pending proposal only. No blanket motif ban, shared-skill promotion, ad generation, campaign change or publication.'
}
updates=lessons.setdefault('research_updates',[])
if not any(x.get('id')==entry['id'] for x in updates):updates.append(entry)
lesson_path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
after=json.loads(lesson_path.read_text(encoding='utf-8'))
retained=all(json.dumps(after[k],sort_keys=True,ensure_ascii=False,separators=(',',':'))==v for k,v in old.items() if k!='research_updates')
expected={
 'v1':'c66e6e5ba4ffedc24d572f8e77ce2cfa191eab974de6efab3d80280f1b1ee167',
 'v2':'80af3a38fb10a22e89a25963ed6acdfbc779a187e49989cbcb6ca46d74dd0e83'
}
preservation={}
for version,target in expected.items():
    p=PROJECT/f'creatives/03-static-01-campus-confusion/{version}/Creative01{version.upper()}.png'
    actual=sha(p)
    preservation[version]={'path':str(p),'sha256':actual,'matches_recorded':actual==target}
    assert actual==target
assets=[]
for r in data['references']:
    for key,url_key in [('image','image_url'),('secondary_image','secondary_image_url')]:
        if key not in r:continue
        p=HERE/r[key]
        raw=p.read_bytes()
        assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP',str(p)
        assets.append({'reference':r['id'],'file':r[key],'source':r[url_key],'sha256':sha(p),'bytes':len(raw),'format':'WEBP','method':'Browser-observed page asset, saved by pageAssets.bundle; copied unchanged'})
report=(HERE/'index.html').read_text(encoding='utf-8')
assert report.count('<article class="ref"')==6
assert report.count('<article class="direction ')==3
assert 'Current source-state distinction' in report
assert 'HOOK → PROMISE → CTA' in report
assert '.secondary-preview{display:block;max-width:100%;height:auto}' in report
for r in data['references']:assert r['url'].replace('&','&amp;') in report
source_paths=['AGENTS.md','editing-system/brand/README.md','editing-system/brand/protrain-palette.json','PROTRAIN_MATCH_CONTEXTE.md','creatives/static-ad-system/active-creative.json','creatives/static-ad-system/six-concepts.json','creatives/static-ad-system/batch-01-briefs.html']
verification={
 'date':'2026-11-13','artifact':'index.html','sha256':sha(HERE/'index.html'),'bytes':len(report.encode()),
 'scope':'Research/art direction only; no ad source or export modified',
 'direct_projects_opened':11,'selected_projects_visually_inspected':6,'reference_assets':assets,
 'source_files':[{ 'path':p,'sha256':sha(PROJECT/p)} for p in source_paths],
 'report_validation':{'references':6,'directions':3,'external_render_dependencies':0,'all_selected_direct_links_present':True,'image_assets_valid_webp':True,'standalone_images_and_fonts_embedded':True},
 'browser_review':{
  'method':'CUA in-app browser via temporary localhost-only server scoped to research directory',
  'desktop':{'width':1280,'document_scroll_width':1265,'observed':'Header, reference analysis, enlarged SaaS and KAB previews, and three-direction comparison inspected'},
  'phone':{'width':390,'document_scroll_width':375,'expanded_reference_notes':6,'secondary_image_width':339,'secondary_parent_width':339,'observed':'Reference section inspected; expanded images fit their containers'},
  'narrow':{'width':320,'document_scroll_width':305,'overflow_in_checked_ref_direction_status_swatch_system_groups':[],'observed':'Palette/source-state note and Arabic/Latin type sample inspected; tables intentionally scroll within their wrappers'},
  'interactions':['Expand/collapse all reference notes','Open/close source preview dialog','Dialog source link targets correct project','Section navigation'],
  'viewport_restored':True,
  'limitations':['Browser FontFaceSet iteration returned no entries; exact font-load status not claimed. Embedded font assets and computed Cairo/Poppins family declarations confirmed; visible Arabic and Latin sample inspected.','Print layout not visually inspected; HTML is the primary deliverable.','No paid-report conversion or live payment-flow test performed.']
 },
 'independent_content_review':{'worker':'/root/art_direction_review','result':'Passed with responsive secondary-image sizing, approval-label correction and verification-file completion; first two fixed and this file supplies the third','scope':'Content and metadata only; root performed browser checks'},
 'ad_preservation':preservation,
 'prior_lesson_nodes_semantically_unchanged':retained,
 'pending':'Imran selects or revises the proposed direction; no production, alternative or Creative 02 before approval',
 'source_state_note':'Current unrendered messaging update discovered during research and reconciled in report. Historical handoff/two-line V2 distinction retained; no copy applied to ads.',
 'approval_status':'AWAITING_IMRAN',
 'no_publication':True
}
assert retained
(HERE/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
readme='''ProTrain Match — Visual Research & Art Direction\n13 November 2026\n\nOpen index.html in a browser. It is self-contained: source previews, original logo and local font files are embedded. No server or internet is required to read it. Behance source links require internet. Click previews to enlarge; expand notes for the full critique.\n\nSix actual, visually inspected Behance references; three proposed directions; one recommended foundation; a four-angle system; RTL/mobile rules; screened-out projects and evidence limitations.\n\nRecommendation: A — Editorial decision, with mechanism diagrams or genuine evidence according to the angle. PROPOSAL ONLY, awaiting Imran. Existing V1/V2 ads and comparison remain untouched. The current documented HOOK → PROMISE → CTA wording is unrendered and distinct from the historical V2 candidate.\n\nFiles\n- index.html: primary standalone report\n- references.json: source names, designers, exact URLs, observations and exclusions\n- verification.json: artifact/source hashes, browser review and preserved ad hashes\n- assets/: unchanged attributed browser exports and historical V1 phone copy\n- build-report.py: regenerates HTML from local report source/data\n\nThe source art is included for attributed research only; it is not licensed here for advertising reuse. No ad production, publication, spending, campaign or account change was performed.\n'''
(HERE/'README.txt').write_text(readme,encoding='utf-8')
package=HERE/'ProTrain-Match-Behance-Research.zip'
files=[HERE/'index.html',HERE/'references.json',HERE/'verification.json',HERE/'README.txt',HERE/'build-report.py']+list((HERE/'assets').glob('*'))
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(HERE).as_posix())
with zipfile.ZipFile(package) as z:assert z.testzip() is None
print(json.dumps({'report_sha256':verification['sha256'],'ad_hashes_preserved':all(v['matches_recorded'] for v in preservation.values()),'prior_lesson_nodes_retained':retained,'zip_bytes':package.stat().st_size,'package':str(package)}))
