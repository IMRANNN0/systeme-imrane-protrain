"""Small authorized speech task. Read existing provider key in memory; never log it."""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

root=Path(__file__).resolve().parents[1]
assets=root/'public/darija-ad'
assets.mkdir(exist_ok=True)
script='كتوجد لكامبوس فرانس؟ بروترين ماتش كيقترح عليك تكوينات على حساب ملفك. عمّر ملفك دابا.'
style='A natural young adult Moroccan woman speaking authentic contemporary Moroccan Darija, Casablanca accent. Friendly, confident, lightly energetic social ad voice, conversational not a newsreader. Do not switch to Modern Standard Arabic, Egyptian or Gulf Arabic. Pronounce Campus France naturally as Moroccan students do and ProTrain Match as بروترين ماتش. Speak clearly at a brisk but unhurried pace, about eight seconds total for this short script. Brief natural pauses at sentence boundaries. Read only the supplied text; no introductions, music, sound effects or added words.'

def key():
    for line in Path('{{IMRANE_WORKSPACE_ROOT}}/secrets/graphify.env').read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('GEMINI_API_KEY='):
            return line.split('=',1)[1].strip().strip('\"\'')
    raise RuntimeError('Authorized provider credential unavailable')

def request(path,payload,timeout=120):
    req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/'+path,
        headers={'x-goog-api-key':key(),'Content-Type':'application/json'},data=json.dumps(payload,ensure_ascii=False).encode('utf-8'))
    try:
        return json.load(urllib.request.urlopen(req,timeout=timeout))
    except urllib.error.HTTPError as error:
        try:
            message=json.loads(error.read()).get('error',{}).get('message','')
            message=message.replace(key(),'[redacted]')[:400]
        except Exception:
            message=''
        raise RuntimeError('Provider returned HTTP '+str(error.code)+' '+message) from None
    except TimeoutError:
        raise RuntimeError('Provider request timed out') from None

def find_audio(value):
    if isinstance(value,dict):
        if value.get('type')=='audio' and value.get('data'):return value
        for item in value.values():
            found=find_audio(item)
            if found:return found
    elif isinstance(value,list):
        for item in value:
            found=find_audio(item)
            if found:return found
    return None

mode=sys.argv[1] if len(sys.argv)>1 else 'generate'
take='take'+mode[-1] if mode[-1:].isdigit() else 'take1'
if mode.startswith('generate'):
    if take=='take2':
        style+=' Revision: The first take rushed the product name. Clearly separate and enunciate بروترين ماتش (Pro-train Match), with a brief natural pause after the opening question and after the brand name. Give the brand about one second, keeping the remaining sentence conversational. Do not compress or swallow the product syllables. Target seven to eight seconds, no more than nine. Keep Darija consonants natural.'
    if take=='take3':
        script=script.replace('بروترين ماتش','ProTrain Match')
        style='Authentic Moroccan Darija woman voice, Casablanca. Warm, confident and conversational, not a fast announcer. Read the Arabic colloquially and the written product name ProTrain Match with clear natural French-English articulation (Pro Train Match), not brotrayn. Separate the opening question, brand introduction and final invitation with short natural pauses. Slow, clear product name. Aim for eight seconds, below nine seconds. No music or extra words.'
    payload={'model':'gemini-3.8-flash-tts','input':[{'type':'user_input','content':[{'type':'text','text':script,
        'annotations':[{'type':'speech_metadata','style':style}]}]}],
        'response_format':{'type':'audio'},'generation_config':{'speech_config':[{'voice':'Kore'}]}}
    result=request('interactions',payload)
    audio=find_audio(result)
    if not audio:raise RuntimeError('No audio block returned; no response contents logged')
    data=base64.b64decode(audio['data'])
    if data[:4]!=b'RIFF':raise RuntimeError('Expected complete WAV; no file written')
    (assets/('voice-'+take+'.wav')).write_bytes(data)
    (assets/'script.txt').write_text(script+'\n',encoding='utf-8')
    (assets/('voice-generation-'+take+'.json')).write_text(json.dumps({'provider':'Gemini API','model':payload['model'],'voice':'Kore',
        'script':script,'style':style,'output':'voice-'+take+'.wav','bytes':len(data),'mode':'synthetic generic voice, not a clone'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'audio_saved':True,'bytes':len(data),'file':'public/darija-ad/voice-'+take+'.wav'}))
elif mode=='export-review':
    source=root/'out/protrain-darija-ad-v1.mp4'
    data=base64.b64encode(source.read_bytes()).decode('ascii')
    instruction='Inspect this actual short vertical advertisement with its audio, critically. Target: Moroccan students preparing Campus France choices. This is a generated-photo narrated motion ad, not a talking customer testimonial; no lip sync expected. Return JSON only: actual_spoken_transcript, observed_scene_timing, arabic_text_readability_and_shaping, text_overflow_or_unintended_wrap, visual_hierarchy, motion_and_cut_pacing, voice_dialect_and_pronunciation, voice_intelligibility_noise_and_distortion, speech_to_visual_sync, ending_CTA_reading_time, concrete_defects (with approximate timestamps, severity, reason and specific fix), acceptable_as_short_production_test (boolean), limits_of_your_review. Assess what is actually visible/audible, do not assume unseen product UI. Do not manufacture defects or praise; distinguish optional taste from a blocker. Watch for clipped Arabic, crowded photo faces, rapid/unclear brand pronunciation and high frequency voice noise. No claims about measured ad performance. No speaker identity inference.'
    model=sys.argv[2] if len(sys.argv)>2 else 'gemini-3.1-flash-lite'
    result=request('interactions',{'model':model,'store':False,'input':[{'type':'text','text':instruction},
        {'type':'video','mime_type':'video/mp4','data':data}]},timeout=60)
    text=result.get('output_text','') or ''.join(part.get('text','') for step in result.get('steps',[]) if step.get('type')=='model_output' for part in step.get('content',[]) if part.get('type')=='text')
    text=text.strip().removeprefix('```json').removeprefix('```').removesuffix('```').strip()
    report=json.loads(text)
    report['review_method']=model+' multimodal analysis of actual exported MP4, including audio; not a human playback verdict'
    report['source_file']=str(source)
    target=root/'out/darija-ad-qa/export-review.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
elif mode.startswith('review'):
    data=base64.b64encode((assets/('voice-'+take+'.wav')).read_bytes()).decode('ascii')
    instruction='Listen to the supplied short audio, without assuming its intended script. Evaluate it as Moroccan Darija advertising speech. Return JSON only with actual_transcript_arabic, utterances (start_seconds,end_seconds,text), dialect_observations, mispronunciations_or_unnatural_words, added_or_missing_or_unintelligible_words, pace_assessment, audible_noise_or_clipping, usable_for_short_ad (boolean), and concrete_changes_needed. Identify uncertainty explicitly; do not call it perfect. Times are approximate auditory estimates, not forced alignment. Evaluate regional accent and whether it sounds naturally Moroccan rather than MSA, Egyptian or Gulf. No speaker identity inference.'
    model=sys.argv[2] if len(sys.argv)>2 else 'gemini-3.5-flash'
    payload={'model':model,'store':False,'input':[{'type':'text','text':instruction},
        {'type':'audio','mime_type':'audio/wav','data':data}]}
    result=request('interactions',payload,timeout=60)
    text=result.get('output_text','')
    if not text:
        text=''.join(part.get('text','') for step in result.get('steps',[]) if step.get('type')=='model_output' for part in step.get('content',[]) if part.get('type')=='text')
    if not text:
        raise RuntimeError('No review text returned; response keys '+','.join(result.keys()))
    text=text.strip().removeprefix('```json').removeprefix('```').removesuffix('```').strip()
    report=json.loads(text)
    report['review_method']=model+' audio-capable model assessed actual WAV; not a human listening verdict'
    (assets/('voice-review-'+take+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
else:
    raise RuntimeError('Unknown mode')
