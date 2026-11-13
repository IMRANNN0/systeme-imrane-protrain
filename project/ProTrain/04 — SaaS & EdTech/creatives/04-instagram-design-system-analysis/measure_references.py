"""Read-only image measurement. Writes evidence alongside this script only."""
from pathlib import Path
from PIL import Image
from collections import Counter
import hashlib, json, statistics, math

base=Path('D:/Instagram')
out=Path(__file__).parent
files=sorted(p for p in base.rglob('*') if p.is_file())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p):digest(p) for p in files}
inventory=[]
for p in files:
    row={'path':str(p),'bytes':p.stat().st_size,'sha256_before':before[str(p)]}
    try:
        with Image.open(p) as im: row.update(width=im.width,height=im.height,mode=im.mode,format=im.format)
    except Exception as e: row['image_read_error']=str(e)
    inventory.append(row)

rois={'32':{'green_ribbon':[40,660,150,675],'yellow_ribbon':[55,800,100,835],'white_ribbon':[48,885,65,950],'footer_green':[5,1045,190,1070],'green_text':[110,747,745,839]},
      '29':{'green_ribbon':[45,667,85,702],'yellow_ribbon':[320,807,430,823],'white_ribbon':[47,870,55,938],'footer_green':[5,1045,190,1070],'green_text':[55,730,780,820]}}
samples=[]
for prefix,regions in rois.items():
    p=next(base.glob('imgi_'+prefix+'_*'))
    with Image.open(p) as im:
        im=im.convert('RGB')
        for label,box in regions.items():
            pixels=list(im.crop(box).getdata())
            filt='all pixels'
            if label=='green_text':
                pixels=[v for v in pixels if v[1]>65 and v[1]>v[0]*1.5 and v[1]>v[2]*1.15 and v[0]<70]
                filt='R<70, G>65, G>1.5R, G>1.15B; isolates green glyph interiors imperfectly'
            counts=Counter(pixels)
            median=[statistics.median(v[i] for v in pixels) for i in range(3)]
            samples.append({'file':p.name,'region':label,'roi_xyxy_exclusive':box,'filter':filt,'pixel_count':len(pixels),'channel_median_rgb':median,'top_rgb_counts':[[list(rgb),n] for rgb,n in counts.most_common(4)]})
after={str(p):digest(p) for p in files}
for row in inventory: row.update(sha256_after=after[row['path']],unchanged=after[row['path']]==row['sha256_before'])
data={'scope':'Analysis of existing files only; no reconstruction or creative generation','coordinates':'original decoded pixel coordinates; origin top left, xyxy excludes right/bottom','method':'Pillow RGB decoding; exact per-channel median and exact RGB frequency in specified ROI. Lossy WebP samples are observations, not official brand tokens. Text filter only approximates interiors.','inventory':inventory,'roi_samples':samples,'all_original_files_unchanged':before==after}
(out/'inventory-measurements.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(inventory),'all_unchanged':before==after,'dimensions':[(Path(x['path']).name,x.get('width'),x.get('height')) for x in inventory],'samples':samples},ensure_ascii=False))
