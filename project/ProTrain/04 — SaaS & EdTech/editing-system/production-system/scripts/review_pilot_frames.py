"""Decode actual phone-size review frames into a new per-run folder; no verdicts."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import uuid
from PIL import Image,ImageDraw

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('artifact',type=Path)
    cli.add_argument('edit_plan',type=Path)
    cli.add_argument('--output-root',type=Path,default=Path(__file__).resolve().parents[1]/'runs')
    args=cli.parse_args();video=args.artifact.resolve();plan=json.loads(args.edit_plan.read_text(encoding='utf-8'))
    count=plan['durationInFrames'];fps=plan['fps'];frames={0,count-1}
    for scene in plan['scenes']:
        start=round(scene['startSeconds']*fps);end=round(scene['endSeconds']*fps)
        frames.update([start,max(start,end-1),round((start+end-1)/2)])
    for caption in plan['captions']:frames.add(round((caption['startMs']+caption['endMs'])/2000*fps))
    frames=sorted(f for f in frames if 0<=f<count)
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-frames-'+uuid.uuid4().hex[:8]
    target=args.output_root.resolve()/run_id;target.mkdir(parents=True,exist_ok=False)
    expression='+'.join(f'eq(n,{frame})' for frame in frames).replace(',',r'\,')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select={expression},scale=360:640','-fps_mode','vfr',str(target/'frame-%03d.png')],check=True)
    pages=[]
    for offset in range(0,len(frames),12):
        batch=frames[offset:offset+12];rows=(len(batch)+3)//4
        sheet=Image.new('RGB',(1440,rows*670),'#deded9');draw=ImageDraw.Draw(sheet)
        for j,frame in enumerate(batch):
            index=offset+j
            with Image.open(target/f'frame-{index+1:03d}.png') as im:sheet.paste(im,((j%4)*360,(j//4)*670+30))
            draw.text(((j%4)*360+10,(j//4)*670+9),f'f{frame} | {frame/fps:.2f}s',fill='#121812')
        out=target/f'contact-{offset//12+1:02d}.jpg';sheet.save(out,quality=95);pages.append(str(out))
    result={'artifact':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'edit_plan':str(args.edit_plan.resolve()),'frames':frames,'contact_pages':pages,'visual_review':'pending','listening_review':'pending','purpose':'Actual decoded evidence for a separate reviewer; generation of sheets does not certify visual quality'}
    with (target/'frame-evidence.json').open('x',encoding='utf-8') as h:json.dump(result,h,indent=2)
    print(json.dumps({'folder':str(target),'frame_count':len(frames),'contact_pages':pages}))

if __name__=='__main__':main()
