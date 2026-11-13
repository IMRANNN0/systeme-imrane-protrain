"""Exercise spending/script guards without reading credentials or making API calls."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('pilot_voice',Path(__file__).resolve().parents[1]/'scripts/generate_pilot_voice.py')
voice=importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class VoiceAuthorization(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.pilot=Path(temporary.name)
        script='Title\n'+'\n'.join('«نص تجريبي»' for _ in range(5))
        self.script=self.pilot/'script.txt';self.script.write_text(script,encoding='utf-8')
        self.plan={'script':{'path':'script.txt','sha256':hashlib.sha256(self.script.read_bytes()).hexdigest()},
            'approvals':{'storyboard':{'status':'approved'},'paid_services':{'status':'approved','provider_scopes':{'Gemini_TTS':{'max_requests':2}}}}}

    def call(self):
        (self.pilot/'production-plan.json').write_text(json.dumps(self.plan),encoding='utf-8')
        with patch('sys.argv',['generate_pilot_voice.py',str(self.pilot)]),patch.object(voice.urllib.request,'urlopen') as request:
            with self.assertRaises(RuntimeError) as raised:voice.main()
            request.assert_not_called()
            return str(raised.exception)

    def test_unapproved_storyboard_blocks_provider(self):
        self.plan['approvals']['storyboard']['status']='pending'
        self.assertIn('approval',self.call())

    def test_unapproved_service_blocks_provider(self):
        self.plan['approvals']['paid_services']['status']='pending'
        self.assertIn('approval',self.call())

    def test_changed_script_blocks_provider(self):
        self.script.write_text('Changed marketing words',encoding='utf-8')
        self.assertIn('differs',self.call())

    def test_exhausted_request_limit_blocks_provider(self):
        record={'provider':'Gemini_TTS','event':'request_started'}
        (self.pilot/'provider-runs.jsonl').write_text('\n'.join(json.dumps(record) for _ in range(2)),encoding='utf-8')
        self.assertIn('limit reached',self.call())


if __name__=='__main__':unittest.main()
