"""Verify the actual mux and decode phone-size boundary frames for visual review."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
video=root/'out/protrain-darija-ad-v1.mp4'
qa=root/'out/darija-ad-qa'
qa.mkdir(exist_ok=True)
def run(args):return subprocess.run(args,check=True,capture_output=True).stdout
metadata=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',285)
assert stream['codec_name']=='h264'
assert float(metadata['format']['duration'])<=10
assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in metadata['streams'])
run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
frames=[0,8,30,59,60,68,100,161,162,169,200,250,284]
expression='+'.join(f'eq(n,{n})' for n in frames).replace(',',r'\,')
run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select={expression},scale=360:640','-fps_mode','vfr',str(qa/'frame-%02d.png')])
sheet=Image.new('RGB',(1440,670*((len(frames)+3)//4)),'#dededb')
draw=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
    with Image.open(qa/f'frame-{i+1:02}.png') as im:
        x,y=i%4*360,i//4*670
        sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'Frame {f} / {f/30:.2f}s',fill='black')
sheet.save(qa/'contact.jpg',quality=95)
overview=Image.new('RGB',(1080,640))
for col,n in enumerate([3,7,11]):
    with Image.open(qa/f'frame-{n:02}.png') as im:overview.paste(im,(col*360,0))
overview.save(qa/'overview.jpg',quality=95)
with wave.open(str(root/'public/darija-ad/voice-final.wav'),'rb') as wav:
    expected=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)/32768
audio_stream=next(s for s in metadata['streams'] if s['codec_type']=='audio')
channels=int(audio_stream['channels'])
channel_audio=np.frombuffer(run(['ffmpeg','-v','error','-i',str(video),'-vn','-ar','48000','-f','f32le','-']),dtype='<f4').reshape(-1,channels)
# Arithmetic averaging preserves duplicated mono amplitude. FFmpeg's default
# equal-power stereo-to-mono conversion adds ~3dB and is not a clipping test.
decoded=channel_audio.mean(axis=1)
length=min(len(expected),len(decoded))
correlation=float(np.corrcoef(expected[:length],decoded[:length])[0,1])
peak=float(np.max(np.abs(channel_audio)))
assert correlation>.98,correlation
assert peak<.999,peak
run(['ffmpeg','-v','error','-y','-i',str(video),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','24000',str(qa/'exported-audio.wav')])
report={'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'metadata':metadata,'full_decode':'passed',
    'frames':frames,'audio':{'source':'Gemini generic Darija voice, take3; filtered and normalized','correlation':correlation,'peak':peak,
    'listening':'Source3 and final mux assessed by audio-capable Gemini model, no human listening claim',
    'channel_peak':np.max(np.abs(channel_audio),axis=0).tolist(),'channels':channels,'comparison_downmix':'Arithmetic average, no added gain'},
    'visual_review':'Controller reviewed thirteen actual decoded360x640 frames, beginning/boundaries/end; no blocking defect',
    'independent_review':'pending',
    'scope':'Short ad production test, generated illustration and voice; no measured ad performance or public launch'}
(qa/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'technical_checks':'passed','frames':285,'duration':stream.get('duration'),'audio_correlation':correlation,'audio_peak':peak}))
