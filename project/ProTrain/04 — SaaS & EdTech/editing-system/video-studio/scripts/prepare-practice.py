"""Prepare synthetic local media and an exact frame-based edit manifest."""

import json
import math
import struct
import subprocess
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'public' / 'practice'
FPS = 30
RATE = 48000
SAMPLES_PER_FRAME = RATE // FPS
SENTENCES = [
    'My average is only one part of my profile.',
    'Before choosing, I compare the published requirements.',
    'Then I check what each option really asks for.',
]


def write_wave(path, pcm):
    with wave.open(str(path), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm)


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    raw = bytearray(RATE * 2)
    source_frame = FPS
    output_frame = 0
    clips = []

    for index, text in enumerate(SENTENCES, start=1):
        normalized = MEDIA / f'take-{index}-48k.wav'
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(MEDIA / f'take-{index}.wav'),
            '-ar', str(RATE), '-ac', '1', '-c:a', 'pcm_s16le', str(normalized),
        ], check=True)
        with wave.open(str(normalized), 'rb') as speech:
            assert speech.getnchannels() == 1 and speech.getsampwidth() == 2
            sample_count = speech.getnframes()
            pcm = speech.readframes(sample_count)

        frame_count = math.ceil(sample_count / SAMPLES_PER_FRAME)
        padded_samples = frame_count * SAMPLES_PER_FRAME
        raw.extend(pcm)
        raw.extend(bytes((padded_samples - sample_count) * 2))
        clips.append({
            'id': f'take-{index}',
            'text': text,
            'sourceInFrame': source_frame,
            'sourceOutFrame': source_frame + frame_count,
            'outputInFrame': output_frame,
            'outputOutFrame': output_frame + frame_count,
        })
        source_frame += frame_count + FPS
        output_frame += frame_count
        raw.extend(bytes(RATE * 2))

    write_wave(MEDIA / 'raw-audio.wav', raw)
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-f', 'lavfi', '-i', f'testsrc2=size=960x540:rate={FPS}',
        '-i', str(MEDIA / 'raw-audio.wav'),
        '-vf', "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='SOURCE FRAME %{n}':x=32:y=32:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.8",
        '-frames:v', str(source_frame), '-c:v', 'libx264', '-crf', '22',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(MEDIA / 'raw-practice.mp4'),
    ], check=True)

    sound = bytearray()
    for sample in range(18 * RATE):
        time = sample / RATE
        value = 0.0
        for onset, frequency in [(0.25, 392), (3.1, 523), (9.1, 659), (14.1, 440)]:
            elapsed = time - onset
            if 0 <= elapsed < 0.6:
                value += 0.12 * math.exp(-elapsed * 9) * math.sin(2 * math.pi * frequency * elapsed)
        sound.extend(struct.pack('<h', round(value * 32767)))
    write_wave(MEDIA / 'comparison-sound.wav', sound)

    manifest = {
        'synthetic': True,
        'voice': 'Microsoft Zira Desktop, en-US, locally synthesized',
        'transcription': 'Known fixture text, not ASR output',
        'fps': FPS,
        'source': 'practice/raw-practice.mp4',
        'rawFrames': source_frame,
        'outputFrames': output_frame,
        'removedFrames': source_frame - output_frame,
        'clips': clips,
    }
    (MEDIA / 'edit-plan.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
