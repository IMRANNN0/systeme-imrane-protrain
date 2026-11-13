"""Read-only export checks; write fresh, artifact-bound technical evidence per run."""
import argparse
import array
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import uuid


def probe(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-count_frames', '-show_streams',
         '-show_format', '-of', 'json', str(path)],
        check=True, capture_output=True, text=True, encoding='utf-8')
    return json.loads(result.stdout)


def decode(path):
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
                    '-f', 'null', '-'], check=True, capture_output=True)


def audio_peaks(path, stream):
    """Measure actual individual channels; never use a gain-changing downmix."""
    channels = int(stream['channels'])
    result = subprocess.run(
        ['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-map',
         '0:' + str(stream['index']), '-vn', '-c:a', 'pcm_f32le',
         '-f', 'f32le', '-'], check=True, capture_output=True)
    samples = array.array('f')
    samples.frombytes(result.stdout)
    if sys.byteorder != 'little':
        samples.byteswap()
    if not samples or len(samples) % channels:
        raise ValueError('Invalid or empty decoded audio samples')
    if not all(math.isfinite(value) for value in samples):
        raise ValueError('Non-finite decoded audio samples')
    peaks = [max(abs(v) for v in samples[ch::channels]) for ch in range(channels)]
    return {'stream_index': stream['index'], 'channels': channels,
            'sample_rate': stream.get('sample_rate'),
            'samples_per_channel': len(samples) // channels,
            'per_channel_sample_peak': peaks,
            'samples_at_or_above_full_scale': sum(abs(v) >= 1 for v in samples),
            'method': 'Decoded float PCM, original channel layout; sample peaks, not true peaks'}


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def positive_float(value):
    number = float(value)
    if not 0 < number < float('inf'):
        raise argparse.ArgumentTypeError('Must be finite and positive')
    return number


def nonnegative_float(value):
    number = float(value)
    if not 0 <= number < float('inf'):
        raise argparse.ArgumentTypeError('Must be finite and nonnegative')
    return number


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('Must be positive')
    return number


def fps_value(value):
    try:
        result = Fraction(value)
        if result <= 0:
            raise ValueError()
        return str(result)
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError('Use positive FPS, e.g. 30 or 30000/1001')


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('artifact', type=Path)
    cli.add_argument('--output-root', type=Path,
                     default=Path(__file__).resolve().parents[1] / 'runs')
    cli.add_argument('--expected-width', type=positive_int, required=True)
    cli.add_argument('--expected-height', type=positive_int, required=True)
    cli.add_argument('--expected-fps', type=fps_value, required=True)
    expected = cli.add_mutually_exclusive_group()
    expected.add_argument('--expected-frames', type=positive_int)
    expected.add_argument('--expected-duration', type=positive_float)
    cli.add_argument('--max-duration', type=positive_float)
    cli.add_argument('--duration-tolerance', type=nonnegative_float, default=0.05)
    cli.add_argument('--voice', type=Path)
    cli.add_argument('--voice-start', type=nonnegative_float, default=0)
    cli.add_argument('--voice-tail', type=nonnegative_float, default=0,
                     help='Required hold after complete voice, in seconds')
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex
    run_dir = args.output_root.resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    path = args.artifact.resolve()
    report = {'schema_version': 1, 'run_id': run_id,
              'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'artifact': {'path': str(path)}, 'technical_status': 'failed',
              'errors': [], 'review': {'visual': 'pending', 'listening': 'pending',
              'creative': 'pending', 'owner': 'pending', 'platform': 'unknown'},
              'limits': ['Technical evidence only; no subjective review or approval is performed.',
                         'Voice fit checks duration, not placement correctness, intelligibility, or transcript.',
                         'Sample peaks are not loudness or intersample true-peak measurements.'],
              'expectations': {k: str(v) if isinstance(v, Path) else v
                               for k, v in vars(args).items() if k != 'output_root'}}
    errors = report['errors']
    try:
        report['artifact'].update(sha256=sha256(path), size_bytes=path.stat().st_size)
        metadata = probe(path)
        report['probe'] = metadata
        video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
        fps = Fraction(video['avg_frame_rate'])
        frames = int(video['nb_read_frames'])
        duration = float(video['duration']) if video.get('duration') else float(Fraction(frames) / fps)
        container_duration = float(metadata['format']['duration'])
        report['video'] = {'duration_seconds': duration, 'decoded_frames': frames,
                           'fps': str(fps), 'container_duration_seconds': container_duration,
                           'color': {key: video.get(key) for key in
                                     ('pix_fmt', 'color_range', 'color_space', 'color_transfer', 'color_primaries')},
                           'color_policy': 'Recorded as probed; no Rec.709 compliance claim'}
        for key, expected in [('width', args.expected_width), ('height', args.expected_height)]:
            if int(video[key]) != expected:
                errors.append(f'{key}: expected {expected}, got {video[key]}')
        if fps != Fraction(args.expected_fps):
            errors.append(f'FPS: expected {args.expected_fps}, got {fps}')
        if args.expected_frames is not None and frames != args.expected_frames:
            errors.append(f'Frames: expected {args.expected_frames}, got {frames}')
        if args.expected_duration is not None and abs(duration - args.expected_duration) > args.duration_tolerance:
            errors.append(f'Video duration: expected {args.expected_duration}, got {duration}')
        if args.max_duration is not None and max(duration, container_duration) > args.max_duration + args.duration_tolerance:
            errors.append(f'Maximum duration {args.max_duration} exceeded')
        decode(path)
        report['full_decode'] = 'passed'
        report['audio'] = [audio_peaks(path, stream) for stream in metadata['streams']
                           if stream['codec_type'] == 'audio']
        for audio in report['audio']:
            if audio['samples_at_or_above_full_scale']:
                errors.append(f"Audio stream {audio['stream_index']}: samples reach/exceed full scale")
        if args.voice:
            voice_path = args.voice.resolve()
            voice_hash = sha256(voice_path)
            voice_meta = probe(voice_path)
            if not any(s['codec_type'] == 'audio' for s in voice_meta['streams']):
                raise ValueError('Voice file has no audio stream')
            voice_duration = float(voice_meta['format']['duration'])
            required = args.voice_start + voice_duration + args.voice_tail
            report['voice'] = {'path': str(voice_path), 'sha256': voice_hash,
                               'duration_seconds': voice_duration, 'required_video_seconds': required,
                               'available_video_seconds': duration, 'remaining_seconds': duration - required}
            if required > duration + 0.001:
                errors.append('Complete narration plus start/tail does not fit video')
            if not report['audio']:
                errors.append('Narration supplied but output has no audio stream')
            if sha256(voice_path) != voice_hash:
                errors.append('Voice artifact changed during verification')
        if sha256(path) != report['artifact']['sha256']:
            errors.append('Artifact changed during verification')
        report['technical_status'] = 'failed' if errors else 'passed'
    except (OSError, ValueError, KeyError, StopIteration, ZeroDivisionError, subprocess.SubprocessError) as exc:
        errors.append(f'{type(exc).__name__}: {exc}')
    report_path = run_dir / 'technical-report.json'
    with report_path.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'technical_status': report['technical_status'], 'report': str(report_path)}))
    return 0 if report['technical_status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
