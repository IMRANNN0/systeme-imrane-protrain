"""One explicitly authorized Gemini TTS request. No automatic retries or key logging."""
import argparse
import base64
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import wave


def find_audio(value):
    if isinstance(value,dict):
        if value.get('type')=='audio' and value.get('data'):return value
        for item in value.values():
            found=find_audio(item)
            if found:return found
    if isinstance(value,list):
        for item in value:
            found=find_audio(item)
            if found:return found
    return None


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('pilot',type=Path)
    args=cli.parse_args();pilot=args.pilot.resolve()
    plan=json.loads((pilot/'production-plan.json').read_text(encoding='utf-8'))
    approval=plan['approvals']['paid_services']
    if plan['approvals']['storyboard']['status']!='approved' or approval['status']!='approved':
        raise RuntimeError('Storyboard and bounded service approval are required')
    limit=approval['provider_scopes']['Gemini_TTS']['max_requests']
    script_path=pilot/plan['script']['path'];raw=script_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=plan['script']['sha256']:raise RuntimeError('Script differs from the approved version')
    sections=re.findall('«(.*?)»',raw.decode('utf-8'))
    if len(sections)!=5:raise RuntimeError('Expected the five exact submitted spoken sections')
    spoken='\n\n'.join(sections)
    log=pilot/'provider-runs.jsonl'
    previous=[json.loads(line) for line in log.read_text(encoding='utf-8').splitlines()] if log.exists() else []
    attempts=sum(e.get('provider')=='Gemini_TTS' and e.get('event')=='request_started' for e in previous)
    if attempts>=limit:raise RuntimeError('Approved TTS request limit reached; no call made')
    credential=None
    for line in Path('{{IMRANE_WORKSPACE_ROOT}}/secrets/graphify.env').read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('GEMINI_API_KEY='):credential=line.split('=',1)[1].strip().strip('\"\'')
    if not credential:raise RuntimeError('Existing authorized provider credential unavailable')
    take=f'vo-take{attempts+1:02}'
    assets=pilot/'assets';assets.mkdir(exist_ok=True)
    output=assets/(take+'.wav')
    if output.exists():raise RuntimeError('Output already exists; refusing overwrite')
    style='A natural adult Moroccan woman, authentic contemporary Moroccan Darija with Casablanca pronunciation. Warm, credible and conversational, explaining calmly to a student; no shouting and no formal Arabic newsreader style. Preserve every supplied word exactly, including the Latin brand and academic terms. Pronounce Campus France and Formation naturally as Moroccan students use them; ProTrain Match clearly as Pro Train Match, with a brief pause around its first mention. The words مجاناً refer to filling the profile, not the full report. Read the full script, complete all sentence tails, and do not add an introduction, music or extra words. Give the question, explanation, product value and final invitation natural short pauses. Aim for a clear unhurried educational ad delivery around45to55seconds if natural; do not force a slow robotic cadence or rush to fit a target.'
    payload={'model':'gemini-3.8-flash-tts','store':False,'input':[{'type':'user_input','content':[{'type':'text','text':spoken,'annotations':[{'type':'speech_metadata','style':style}]}]}],
        'response_format':{'type':'audio'},'generation_config':{'speech_config':[{'voice':'Kore'}]}}
    def event(kind,**extra):
        value={'date_utc':datetime.now(timezone.utc).isoformat(),'provider':'Gemini_TTS','take':take,'event':kind,'script_sha256':plan['script']['sha256'],**extra}
        with log.open('a',encoding='utf-8') as handle:handle.write(json.dumps(value,ensure_ascii=False)+'\n')
    event('request_started',model=payload['model'],approval_event=approval['event_id'])
    request=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/interactions',headers={'x-goog-api-key':credential,'Content-Type':'application/json'},data=json.dumps(payload,ensure_ascii=False).encode('utf-8'))
    try:
        with urllib.request.urlopen(request,timeout=120) as response:result=json.load(response)
        block=find_audio(result)
        if not block:raise RuntimeError('Provider returned no audio block')
        audio=base64.b64decode(block['data'])
        if audio[:4]!=b'RIFF':raise RuntimeError('Expected complete WAV output')
        with output.open('xb') as handle:handle.write(audio)
        with wave.open(str(output),'rb') as wav:duration=wav.getnframes()/wav.getframerate()
        metadata={'provider':'Gemini API','model':payload['model'],'voice':'Kore','script_sha256':plan['script']['sha256'],'exact_spoken_text':spoken,'style':style,'output':output.name,'duration_seconds':duration,'status':'generated, awaiting pronunciation and creative review','voice_type':'generic synthetic, not cloned'}
        (assets/(take+'.json')).write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
        event('request_completed',output=str(output),duration_seconds=duration)
        print(json.dumps({'take':take,'duration_seconds':duration,'output':str(output),'review_status':'pending'}))
    except Exception as exc:
        status=exc.code if isinstance(exc,urllib.error.HTTPError) else type(exc).__name__
        event('request_failed',status=status)
        raise RuntimeError('TTS request failed ('+str(status)+'); no automatic retry. Credential and raw response not logged.') from None


if __name__=='__main__':main()
