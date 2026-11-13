"""Inspect real exports: metadata, full decode, edit mapping, review frames, audio."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'
QA = OUT / 'practice-qa'
QA.mkdir(exist_ok=True)
PLAN = json.loads((ROOT / 'public/practice/edit-plan.json').read_text())


def run(args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def inspect(name, frames, sample_frames):
    path = OUT / f'{name}.mp4'
    metadata = json.loads(run(['ffprobe', '-v', 'error', '-count_frames',
                              '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
    assert int(video['nb_read_frames']) == frames, video
    assert (video['width'], video['height'], video['r_frame_rate']) == (1080, 1920, '30/1')
    assert video['codec_name'] == 'h264'
    assert any(s['codec_type'] == 'audio' for s in metadata['streams'])
    run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'])
    expression = '+'.join(f'eq(n,{f})' for f in sample_frames)
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf',
         f'select={expression.replace(",", chr(92)+",")},scale=270:480',
         '-fps_mode', 'vfr', str(QA / f'{name}-%02d.png')])
    sheet = Image.new('RGB', (270 * min(4, len(sample_frames)),
                             510 * ((len(sample_frames) + 3)//4)), '#ddd')
    draw = ImageDraw.Draw(sheet)
    for i, frame in enumerate(sample_frames):
        p = QA / f'{name}-{i+1:02}.png'
        with Image.open(p) as image:
            x, y = (i % 4)*270, (i//4)*510
            sheet.paste(image, (x, y+30))
            draw.text((x+10, y+8), f'Output frame {frame}', fill='black')
    sheet.save(QA / f'{name}-contact.jpg', quality=95)
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'metadata': metadata, 'full_decode': 'passed', 'sample_frames': sample_frames}


def audio_check():
    with wave.open(str(ROOT / 'public/practice/raw-audio.wav'), 'rb') as raw:
        samples = np.frombuffer(raw.readframes(raw.getnframes()), dtype='<i2').astype(float)/32768
    expected = np.concatenate([samples[c['sourceInFrame']*1600:c['sourceOutFrame']*1600]
                               for c in PLAN['clips']])
    decoded = np.frombuffer(run(['ffmpeg', '-v', 'error', '-i', str(OUT/'practice-cut.mp4'),
                                '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']), dtype='<f4')
    assert len(decoded) >= len(expected)-1600
    clips = []
    for c in PLAN['clips']:
        # Ignore codec edges for the waveform comparison, but inspect all output peaks.
        lo, hi = c['outputInFrame']*1600+9600, c['outputOutFrame']*1600-9600
        reference = expected[lo:hi:8]
        trials = [(float(np.corrcoef(reference, decoded[lo+lag:hi+lag:8])[0, 1]), lag)
                  for lag in range(-1920, 1921, 48) if lo+lag >= 0 and hi+lag <= len(decoded)]
        correlation, lag = max(trials)
        assert correlation > .95, (c['id'], correlation, lag)
        clips.append({'id': c['id'], 'waveform_correlation': correlation,
                      'best_alignment_ms': lag/48})
    peak = float(np.max(np.abs(decoded)))
    assert peak < .999, peak
    return {'method': 'Rendered audio compared with retained synthetic source PCM; not ASR',
            'clips': clips, 'peak': peak, 'decoded_samples': len(decoded),
            'expected_samples': len(expected), 'listening_review': 'pending'}


cursor = 0
for c in PLAN['clips']:
    assert c['outputInFrame'] == cursor
    assert c['sourceOutFrame']-c['sourceInFrame'] == c['outputOutFrame']-c['outputInFrame']
    cursor = c['outputOutFrame']
assert cursor == PLAN['outputFrames'] == 350
assert PLAN['rawFrames']-cursor == 120
result = {
    'synthetic_only': True,
    'comparison': inspect('practice-comparison', 540, [0, 30, 89, 90, 180, 269, 270, 330, 419, 420, 480, 539]),
    'cut': inspect('practice-cut', 350, [0, 110, 111, 239, 240, 349]),
    'edit_plan': PLAN,
    'audio': audio_check(),
    'visual_review': 'pending',
    'limits': ['No Darija voice sync or ASR tested', 'No real footage, report, logo or testimony',
               'No mobile player QA or advertising performance measured'],
}
(QA/'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({'status':'technical checks passed', 'frames':[540,350], 'removed_seconds':4,
                  'audio':result['audio'], 'report':str(QA/'verification.json')}, ensure_ascii=True))
