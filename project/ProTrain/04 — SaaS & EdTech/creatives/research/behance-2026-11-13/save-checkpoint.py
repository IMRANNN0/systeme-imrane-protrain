from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).parent
LANE=HERE.parents[3]
memory=LANE/'.codex/memory'
heading='## Behance visual research delivered — 13 November 2026'
checkpoint='''## Behance visual research delivered — 13 November 2026

### Restart checkpoint
- Current stage: research/art-direction report delivered locally, awaiting Imran's selected visual direction. No Static Ad was created or modified; existing V1/V2 and their comparison are preserved.
- Done when: Imran can browse six real, attributed Behance references with offline previews, compare three directions, and review the four-angle system, mobile/RTL rules and limitations.
- Last verified: self-contained `04 — SaaS & EdTech/creatives/research/behance-2026-11-13/index.html`, source `references.json`, `verification.json` and ZIP package. Eleven actual projects opened; six selected pages and compositions inspected beyond covers. Root browser QA at1280/390/320px, modal and expand/collapse checked; source/metadata review by /root/art_direction_review. No page-level horizontal overflow at checked widths. Prior lesson nodes semantically preserved.
- Recommendation: A Editorial decision as proposed foundation, using simple mechanism relationships for Matching and genuine excerpts for Report. This is not owner approval or purchase-performance evidence. No new shared-skill rule was promoted.
- Source-state distinction: concurrent documentation-only HOOK → PROMISE → CTA update discovered and read; current exact messaging remains unrendered. The original handoff's two-line V2 correction is historical, not silently applied to new copy. Preserve current active-creative.json and last_rendered_candidate status. No production until Imran chooses direction and applicable brief is clear.
- Preservation: V1 SHA256 c66e6e5ba4ffedc24d572f8e77ce2cfa191eab974de6efab3d80280f1b1ee167; V2 SHA256 80af3a38fb10a22e89a25963ed6acdfbc779a187e49989cbcb6ca46d74dd0e83. Both matched. Report SHA256 b556e5c4ceb45a3f0557b9d4d34cf5b74f7385371fca275265b0058ba26fb0e2.
- Next action: Imran reviews the HTML and selects or revises a direction. Do not produce an alternative, Creative02, new C01 version, campaign or publication from this research task. Actual proof-led creatives03/06 still need genuine captures.
- Limits: no conversion evidence, live purchase-flow test or print-layout visual verification. Localhost browser preview used a temporary directory-scoped server; the saved HTML does not need it. Source previews remain attributed research material, not licensed ad assets.

'''
current=memory/'CURRENT.md'
text=current.read_text(encoding='utf-8')
if heading not in text:current.write_text(checkpoint+text,encoding='utf-8')
index=memory/'CONTEXT_INDEX.md'
idx=index.read_text(encoding='utf-8')
if '## Behance art direction research — 13 November 2026' not in idx:
    index.write_text(idx+'\n\n## Behance art direction research — 13 November 2026\n\n- `04 — SaaS & EdTech/creatives/research/behance-2026-11-13/index.html`: standalone browsable report, six actual references, three proposed directions and four-angle system. Direction selection pending; no ad changes.\n- Same folder: references.json, verification.json, README.txt and ProTrain-Match-Behance-Research.zip; lesson record research_updates retains the pending proposal and research-only instruction.\n',encoding='utf-8')
decisions=memory/'DECISIONS.md'
d=decisions.read_text(encoding='utf-8')
if '## PROTRAIN-BEHANCE-20261113' not in d:
    decisions.write_text(d+'''\n\n## PROTRAIN-BEHANCE-20261113 — research-only scope confirmed, 13 November 2026

Owner requested independent Behance visual research before further static-ad production. Deliver a browsable report with real inspected projects, direct links, previews, three directions and a proposed system. Do not create or modify a Static Ad in this task. Imran must select the direction before further Creative01V2 production. Existing V2 remains awaiting approval; its presence does not authorize a revision or Creative02. The report's DirectionA recommendation is proposed, not accepted. Current documentation-only messaging remains unrendered. Local report and evidence: `04 — SaaS & EdTech/creatives/research/behance-2026-11-13/`.
''',encoding='utf-8')
print(json.dumps({'memory_updated':[str(current),str(index),str(decisions)],'snapshot':'starting'}),flush=True)
subprocess.run([sys.executable,'{{IMRANE_WORKSPACE_ROOT}}/tools/systeme-imrane/scripts/imrane.py','snapshot','--workspace','{{IMRANE_WORKSPACE_ROOT}}','--id','protrain'],check=True)
