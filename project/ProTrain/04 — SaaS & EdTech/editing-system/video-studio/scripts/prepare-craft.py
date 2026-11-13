"""Original vector paper artwork and a synthetic paper-action sound fixture."""
import math
import random
import struct
import wave
from pathlib import Path

assets=Path(__file__).resolve().parents[1]/'public/craft'
assets.mkdir(parents=True,exist_ok=True)

def svg(width,height,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{body}</svg>'

grain='''<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".62" numOctaves="3" stitchTiles="stitch" seed="21"/><feColorMatrix type="saturate" values="0"/></filter></defs>'''
desk=grain+'''<rect width="1080" height="1920" fill="#DDD9CC"/>
<path d="M0 180Q290 130 570 168T1080 130M0 1680Q290 1650 640 1690T1080 1660" fill="none" stroke="#BDB8A6" stroke-width="2" opacity=".35"/>
<path d="M0 0H280L0 270Z" fill="#CAC5B4" opacity=".35"/>
<rect width="1080" height="1920" filter="url(#grain)" opacity=".045"/>
<g transform="translate(1030 1420) rotate(17)"><path d="M0 0H22V400L11 435 0 400Z" fill="#263238"/><path d="M0 400H22L11 435Z" fill="#B68A5B"/><path d="m7 423 4 12 4-12Z" fill="#263238"/><path d="M4 0H9V398H4Z" fill="#7C8277"/></g>'''
(assets/'desk.svg').write_text(svg(1080,1920,desk),encoding='utf-8')
for name,accent in [('science','#37697B'),('economics','#AC552F')]:
    rules=''.join(f'<path d="M53 {y}H407" stroke="#A5A89B" stroke-width="1" opacity=".31"/>' for y in range(79,810,44))
    holes=''.join(f'<ellipse cx="24" cy="{y}" rx="6" ry="8" fill="#BBB3A1"/>' for y in range(90,780,77))
    body=grain+f'''<path d="M3 8 433 2 439 832 420 850 7 845Z" fill="#FAF6E9" stroke="#CDC5B3" stroke-width="2"/>
<path d="M37 9V838" stroke="{accent}" stroke-width="4" opacity=".66"/>{rules}{holes}
<path d="m369 3 64-1 2 68Z" fill="#E3DCCB"/><path d="m369 3 64 67" stroke="#B8AE98" stroke-width="2"/>
<rect x="5" y="8" width="430" height="830" filter="url(#grain)" opacity=".035"/>
<path d="m78 710 70-5 20 9 60-10M78 753l123-9 52 7 76-6" fill="none" stroke="{accent}" stroke-width="3" opacity=".22"/>'''
    (assets/f'{name}-paper.svg').write_text(svg(440,850,body),encoding='utf-8')
band=grain+'''<path d="m8 14 914-8-5 578-43 8-56-6-52 10-74-8-68 8-68-6-75 7-73-5-61 5-81-6-66 5-65-8-64 4Z" fill="#EBAE55" stroke="#CE9040" stroke-width="2"/>
<path d="M27 46Q421 36 895 43M34 556Q431 548 891 561" stroke="#CB8935" stroke-width="2" opacity=".32"/>
<path d="M464 18Q449 275 466 585" fill="none" stroke="#B87C32" stroke-width="3" opacity=".20"/>
<rect x="10" y="12" width="900" height="575" filter="url(#grain)" opacity=".055"/>'''
(assets/'grade-band.svg').write_text(svg(930,600,band),encoding='utf-8')

rate=48000
sound=[0.0]*(9*rate)
random.seed(32)
# Three uneven frictions are one paper-lift action, not a soundtrack of repeated whooshes.
for at,duration,level in [(1.4,.15,.045),(1.61,.37,.14),(2.06,.55,.10),(2.75,.22,.065),(3.56,.13,.10)]:
    previous=0.0
    for i in range(round(duration*rate)):
        t=i/rate
        noise=random.uniform(-1,1)
        high=noise-previous
        previous=.75*previous+.25*noise
        envelope=math.sin(math.pi*t/duration)**2
        sound[round(at*rate)+i]+=level*high*envelope
for i in range(round(.13*rate)):
    t=i/rate
    sound[round(3.56*rate)+i]+=.09*math.sin(2*math.pi*110*t)*math.exp(-40*t)*min(1,t/.005)
with wave.open(str(assets/'paper-action.wav'),'wb') as out:
    out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate)
    out.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,s))*32767)) for s in sound))
# Keep the generated friction out of the ultrasonic/high hiss band before AAC encoding.
import subprocess
subprocess.run(['ffmpeg','-v','error','-y','-i',str(assets/'paper-action.wav'),'-af','lowpass=f=8000:p=2',str(assets/'paper-action-filtered.wav')],check=True)
(assets/'paper-action-filtered.wav').replace(assets/'paper-action.wav')
print('Prepared original paper SVGs and9-second synthetic action sound')
