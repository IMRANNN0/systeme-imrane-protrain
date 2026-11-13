"""Original local cue track. No speech, stock music or external media."""
import math
import random
import struct
import wave
from pathlib import Path

rate = 48000
samples = [0.0] * (18 * rate)
for at, frequency in [(0,392),(2.5,523.25),(3.2,659.25),(7.5,392),(9.2,523.25),(10.15,587.33),(11.1,659.25),(13.5,440)]:
    for i in range(int(.38*rate)):
        t=i/rate
        envelope=min(1,t/.008)*math.exp(-10*t)
        value=.1*envelope*(math.sin(2*math.pi*frequency*t)+.2*math.sin(2*math.pi*frequency*2*t))
        samples[round(at*rate)+i]+=value
random.seed(21)
for at in [2.30,7.30,13.30]:
    previous=0.0
    for i in range(int(.2*rate)):
        previous=.82*previous+.18*random.uniform(-1,1)
        samples[round(at*rate)+i]+=.1*previous*math.sin(math.pi*i/(.2*rate))**2
path=Path(__file__).resolve().parents[1]/'public/practice/comparison-v2-sound.wav'
with wave.open(str(path),'wb') as out:
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(rate)
    out.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,s))*32767)) for s in samples))
print('Prepared original 18-second V2 cue track')
