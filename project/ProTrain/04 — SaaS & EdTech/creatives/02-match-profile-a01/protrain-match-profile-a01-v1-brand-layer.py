from PIL import Image, ImageDraw
from pathlib import Path
import json, shutil
out=Path(r'{{PROTRAIN_PROJECT_ROOT}}/04 — SaaS & EdTech/creatives/02-match-profile-a01')
src=Path(r'C:/Users/Administrator/.codex/generated_images/01a1d2fd-907a-7172-8da2-b396a2fa59bc/exec-d61b5b88-28b6-41e9-b0bc-ba9c6d179433.png')
logo_path=Path(r'{{PROTRAIN_PROJECT_ROOT}}/04 — SaaS & EdTech/editing-system/brand/protrain-logo-site.png')
shutil.copy2(src,out/'protrain-match-profile-a01-v1-generated.png')
im=Image.open(src).convert('RGBA')
# Native brand layer: use original RGBA source without scaling or redrawing.
# Replace generated logo area with a deliberately clean white brand panel.
layer=Image.new('RGBA',im.size,(0,0,0,0))
draw=ImageDraw.Draw(layer)
draw.rounded_rectangle((0,0,230,188),radius=18,fill=(255,255,255,255))
draw.rectangle((0,0,212,170),fill=(255,255,255,255))
logo=Image.open(logo_path).convert('RGBA')
layer.alpha_composite(logo,(36,29))
im=Image.alpha_composite(im,layer).convert('RGB')
im.save(out/'protrain-match-profile-a01-v1.png')
meta={
'asset':'First ProTrain Match profile-to-recommendations static prototype',
'version':'a01-v1',
'tool':'built-in image_gen__imagegen',
'original_generated_image':str(src),
'generated_reference':'protrain-match-profile-a01-v1-generated.png',
'final':'protrain-match-profile-a01-v1.png',
'prompt':'protrain-match-profile-a01-v1-prompt.txt',
'layout_source':'protrain-match-profile-a01-v1-brand-layer.py',
'size':[1122,1402],
'logo':{'source':str(logo_path),'method':'Original 141x127 RGBA image composited at native resolution on a white brand panel, no redraw or scaling','position':[36,29]},
'copy_checks':['Arabic headline, kicker, support and CTA visually match prompt','ProTrain Match present','No CTA arrow','No price, offer, dates or deadline','No invented programs, marks, outcomes or testimonials','Conceptual folder motif, no report UI'],
'limits':['Generated student is synthetic','Illustrative folder is explanatory and does not depict an actual report','No real product screenshot supplied','Output is a review prototype; no publishing performed']
}
(out/'protrain-match-profile-a01-v1-brief.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(str(out/'protrain-match-profile-a01-v1.png'))

