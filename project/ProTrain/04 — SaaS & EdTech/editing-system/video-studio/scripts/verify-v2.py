"""Verify actual V2 export and generate phone-sized review evidence."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
video=root/'out/practice-comparison-v2.mp4'
qa=root/'out/v2-qa'
qa.mkdir(exist_ok=True)


def run(args):
    return subprocess.run(args,check=True,capture_output=True).stdout


metadata=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',540)
assert stream['codec_name']=='h264'
assert any(s['codec_type']=='audio' for s in metadata['streams'])
run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])

# Before/after each meaningful visual change; exact decoded frames, not a mockup.
frames=[0,74,75,95,120,209,210,224,225,240,255,270,300,330,360,404,405,450,539]
expression='+'.join(f'eq(n,{f})' for f in frames).replace(',',r'\,')
run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select={expression},scale=360:640','-fps_mode','vfr',str(qa/'frame-%02d.png')])
sheet=Image.new('RGB',(1440,670*((len(frames)+3)//4)),'#ddd')
draw=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
    with Image.open(qa/f'frame-{i+1:02d}.png') as image:
        x,y=(i%4)*360,(i//4)*670
        sheet.paste(image,(x,y+30))
        draw.text((x+10,y+8),f'Frame {f}',fill='black')
sheet.save(qa/'contact.jpg',quality=95)

# Four large stable scenes for the handoff, retaining 360px phone-scale text.
hero=Image.new('RGB',(1440,640))
for i,n in enumerate([1,5,13,18]):
    with Image.open(qa/f'frame-{n:02d}.png') as image:
        hero.paste(image,(i*360,0))
hero.save(qa/'overview.jpg',quality=95)

with wave.open(str(root/'public/practice/comparison-v2-sound.wav'),'rb') as wav:
    expected=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)/32768
decoded=np.frombuffer(run(['ffmpeg','-v','error','-i',str(video),'-vn','-ar','48000','-ac','1','-f','f32le','-']),dtype='<f4')
length=min(len(expected),len(decoded))
correlation=float(np.corrcoef(expected[:length],decoded[:length])[0,1])
peak=float(np.max(np.abs(decoded)))
assert correlation>.98,correlation
assert peak<.999,peak
report={'version':'V2','scope':'Synthetic educational practice; not a client ad or measured creative performance',
        'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'metadata':metadata,
        'full_decode':'passed','sample_frames':frames,'phone_scale':'360x640 frame images inspected separately; no physical phone playback claim',
        'audio':{'source':'Original locally generated cue track; no speech','waveform_correlation':correlation,'peak':peak,'listening':'pending'},
        'visual_review':'pending','independent_review':'pending'}
(qa/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'status':'technical checks passed','video_frames':540,'audio_correlation':correlation,'audio_peak':peak,'review_frames':len(frames)},ensure_ascii=True))
