"""Contract tests use probe/decode doubles; no media rendering or provider calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'scripts/check_export.py'
spec = importlib.util.spec_from_file_location('check_export', MODULE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def metadata(duration=9.5, width=1080):
    return {'streams': [{'codec_type': 'video', 'index': 0, 'width': width,
                         'height': 1920, 'avg_frame_rate': '30/1',
                         'nb_read_frames': '285', 'duration': str(duration)},
                        {'codec_type': 'audio', 'index': 1, 'channels': 2}],
            'format': {'duration': str(duration)}}


class ExportContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifact = self.root / 'export.mp4'
        self.artifact.write_bytes(b'original export fixture')
        self.runs = self.root / 'runs'
        self.arguments = [str(self.artifact), '--output-root', str(self.runs),
                          '--expected-width', '1080', '--expected-height', '1920',
                          '--expected-fps', '30', '--expected-frames', '285']

    def run_check(self, meta=None, extra=(), decode_error=None):
        peaks = {'stream_index': 1, 'samples_at_or_above_full_scale': 0,
                 'per_channel_sample_peak': [0.8, 0.8]}
        with patch.object(checker, 'probe', return_value=meta or metadata()), \
             patch.object(checker, 'decode', side_effect=decode_error), \
             patch.object(checker, 'audio_peaks', return_value=peaks):
            return checker.main(self.arguments + list(extra))

    def reports(self):
        return sorted(self.runs.glob('*/technical-report.json'))

    def test_repeated_run_preserves_review_and_history(self):
        self.assertEqual(self.run_check(), 0)
        first = self.reports()[0]
        original = first.read_bytes()
        review = first.parent / 'owner-review.json'
        review.write_text('{"owner":"approved this exact original"}')
        self.assertEqual(self.run_check(), 0)
        self.assertEqual(len(self.reports()), 2)
        self.assertEqual(first.read_bytes(), original)
        self.assertIn('approved this exact original', review.read_text())
        newest = json.loads(self.reports()[-1].read_text())
        self.assertEqual(newest['review']['owner'], 'pending')
        self.assertEqual(newest['review']['listening'], 'pending')

    def test_changed_bytes_get_new_hash_and_do_not_inherit_pass(self):
        self.assertEqual(self.run_check(), 0)
        old = json.loads(self.reports()[0].read_text())
        self.artifact.write_bytes(b'corrupted replacement export')
        self.assertEqual(self.run_check(decode_error=ValueError('cannot decode replacement')), 1)
        new = json.loads(self.reports()[-1].read_text())
        self.assertNotEqual(old['artifact']['sha256'], new['artifact']['sha256'])
        self.assertEqual(new['technical_status'], 'failed')
        self.assertEqual(new['review']['owner'], 'pending')

    def test_invalid_dimensions_fail(self):
        self.assertEqual(self.run_check(metadata(width=720)), 1)

    def test_invalid_duration_fails(self):
        self.assertEqual(self.run_check(extra=['--max-duration', '8']), 1)

    def test_expected_duration_fails(self):
        self.arguments = self.arguments[:-2]
        self.assertEqual(self.run_check(extra=['--expected-duration', '10']), 1)

    def test_complete_narration_and_tail_must_fit(self):
        voice = self.root / 'voice.wav'
        voice.write_bytes(b'voice fixture')
        voice_meta = {'streams': [{'codec_type': 'audio'}], 'format': {'duration': '9.4'}}
        with patch.object(checker, 'probe', side_effect=[metadata(), voice_meta]), \
             patch.object(checker, 'decode'), \
             patch.object(checker, 'audio_peaks', return_value={
                 'stream_index': 1, 'samples_at_or_above_full_scale': 0}):
            self.assertEqual(checker.main(self.arguments + ['--voice', str(voice), '--voice-tail', '0.2']), 1)
        result = json.loads(self.reports()[0].read_text())
        self.assertLess(result['voice']['remaining_seconds'], 0)

    def test_longer_narration_fails(self):
        voice = self.root / 'voice.wav'
        voice.write_bytes(b'long voice fixture')
        with patch.object(checker, 'probe', side_effect=[metadata(), {
                'streams': [{'codec_type': 'audio'}], 'format': {'duration': '10'}}]), \
             patch.object(checker, 'decode'), \
             patch.object(checker, 'audio_peaks', return_value={
                 'stream_index': 1, 'samples_at_or_above_full_scale': 0}):
            self.assertEqual(checker.main(self.arguments + ['--voice', str(voice)]), 1)


if __name__ == '__main__':
    unittest.main()
