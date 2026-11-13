"""Inspect the actual nine-second craft export, not just its source."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
video=root/'out/craft-study.mp4'
qa=root/'out/craft-qa'
qa.mkdir(exist_ok=True)
def run(args):
    return subprocess.run(args,check=True,capture_output=True).stdout
metadata=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',270)
assert stream['codec_name']=='h264'
run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
frames=[0,41,47,59,66,78,90,107,108,143,144,180,269]
expression='+'.join(f'eq(n,{n})' for n in frames).replace(',',r'\,')
run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select={expression},scale=360:640','-fps_mode','vfr',str(qa/'frame-%02d.png')])
sheet=Image.new('RGB',(1440,670*((len(frames)+3)//4)),'#ddd')
draw=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
    with Image.open(qa/f'frame-{i+1:02}.png') as image:
        x,y=i%4*360,i//4*670
        sheet.paste(image,(x,y+30));draw.text((x+10,y+8),f'Frame {f}',fill='black')
sheet.save(qa/'contact.jpg',quality=95)
overview=Image.new('RGB',(1080,640))
for col,n in enumerate([1,9,12]):
    with Image.open(qa/f'frame-{n:02}.png') as image:overview.paste(image,(col*360,0))
overview.save(qa/'overview.jpg',quality=95)
with wave.open(str(root/'public/craft/paper-action.wav'),'rb') as wav:
    expected=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)/32768
decoded=np.frombuffer(run(['ffmpeg','-v','error','-i',str(video),'-vn','-ac','1','-ar','48000','-f','f32le','-']),dtype='<f4')
length=min(len(expected),len(decoded))
correlation=float(np.corrcoef(expected[:length],decoded[:length])[0,1])
peak=float(np.max(np.abs(decoded)))
assert correlation>.98,correlation
assert peak<.999,peak
report={'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'metadata':metadata,'full_decode':'passed',
        'frames':frames,'audio':{'source':'Original locally synthesized paper-action fixture, no voice','correlation':correlation,'peak':peak,'listening':'pending'},
        'visual_review':'pending','independent_review':'pending','scope':'Unapproved style study, not a finished client advertisement'}
(qa/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'technical_checks':'passed','frames':270,'duration':stream.get('duration'),'audio_correlation':correlation,'audio_peak':peak}))
