#!/usr/bin/env python3
"""Install the private ProTrain kit into a separate workspace, offline (Python 3.11+)."""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'tools/systeme-imrane'
sys.path.insert(0,str(ENGINE/'scripts'))
import imrane
from common import write_json, read_json
from agents import generate

STATE='.imrane/protrain-portable/installed.json'
MEMORIES=('CURRENT.md','DECISIONS.md','CONTEXT_INDEX.md','PROJECT_CONTEXT.md')
BLOCKED={'.git','.venv','venv','node_modules','__pycache__','.cache','.graphify-cache','.imrane','.ashraf','.work','tmp','secrets'}
TOKENS={'{{IMRANE_WORKSPACE_ROOT}}':None,'{{PROTRAIN_PROJECT_ROOT}}':None}

def sha(data):return hashlib.sha256(data).hexdigest()
def linked(p):
    try:s=p.lstat()
    except FileNotFoundError:return False
    return stat.S_ISLNK(s.st_mode) or bool(getattr(s,'st_file_attributes',0)&0x400)
def no_links(p):
    for current in (p,*p.parents):
        if linked(current):raise ValueError('Linked path refused: '+str(current))
def safe(base,relative):
    if not isinstance(relative,str) or not relative or '\\' in relative:raise ValueError('Invalid portable path')
    parts=relative.split('/')
    if any(p in ('','.','..') or re.search(r'[:*?<>|"\x00-\x1f]',p) or p.endswith(('.', ' ')) or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?',p) for p in parts):raise ValueError('Unsafe path: '+relative)
    result=base.joinpath(*parts);no_links(result)
    return result
def files(base):
    no_links(base)
    if not base.is_dir():raise ValueError('Missing directory: '+str(base))
    result={};folded=set()
    for folder,dirs,names in os.walk(base,followlinks=False):
        for name in dirs+names:
            p=Path(folder)/name
            if linked(p):raise ValueError('Linked entry refused: '+str(p))
        for name in names:
            p=Path(folder)/name;rel=p.relative_to(base).as_posix();safe(base,rel)
            if not stat.S_ISREG(p.stat().st_mode):raise ValueError('Non-regular source: '+rel)
            if rel.casefold() in folded:raise ValueError('Case-insensitive collision: '+rel)
            folded.add(rel.casefold());result[rel]=p
    return result
def destination(value):
    raw=Path(value).expanduser().absolute();no_links(raw);target=raw.resolve()
    if target==ROOT or ROOT in target.parents or target in ROOT.parents:raise ValueError('Choose a destination separate from the kit checkout')
    imrane.command_string([sys.executable,target])
    for ancestor in (target,*target.parents):
        registry=ancestor/'.codex/projects.json'
        if not registry.is_file():continue
        for project in read_json(registry,{}).get('projects',[]):
            lane=safe(ancestor,project['path']).resolve()
            if target==lane or lane in target.parents:raise ValueError('Destination is inside a registered business lane')
    return target
def substitute(data,target):
    # Forward slashes are safe in JSON strings and shell-quoted portable pointers.
    if b'{{' not in data:return data
    try:text=data.decode('utf-8')
    except UnicodeError:return data
    if '\x00' in text:return data
    text=text.replace('{{IMRANE_WORKSPACE_ROOT}}',target.as_posix())
    text=text.replace('{{PROTRAIN_PROJECT_ROOT}}',(target/'projects/ProTrain').as_posix())
    return text.encode('utf-8')
def payload():
    entries=files(ROOT/'project/ProTrain')
    for rel in entries:
        parts=Path(rel).parts
        if any(p.casefold() in BLOCKED for p in parts) or rel.endswith(('.pyc','.key')) or Path(rel).name in {'auth.json','graphify.env','settings.local.json'} or Path(rel).name.startswith('.env'):
            raise ValueError('Private/generated payload entry refused: '+rel)
        if parts[0] in {'.agents','.claude'}:raise ValueError('Payload host settings must be generated: '+rel)
        if parts[0]=='.codex' and rel not in {'.codex/memory/'+m for m in MEMORIES}|{'.codex/graphify-scope.json'}:raise ValueError('Payload host config must be generated: '+rel)
    required={'AGENTS.md',*('.codex/memory/'+m for m in MEMORIES)}
    if not required.issubset(entries):raise ValueError('ProTrain payload lacks instructions or four canonical memories')
    return entries
def skill_payload():
    spec=read_json(ROOT/'kit/skills-manifest.json')
    actual=files(ROOT/'kit/skills');expected={f['path']:f for f in spec['files']}
    if set(actual)!=set(expected):raise ValueError('Unmanifested/missing skill files')
    for rel,p in actual.items():
        data=p.read_bytes();entry=expected[rel]
        if sha(data)!=entry['sha256'] or len(data)!=entry['bytes']:raise ValueError('Skill integrity mismatch: '+rel)
    ids={s['id'] for s in spec['skills'] if s['delivery']=='payload'}
    if ids!={r.split('/')[0] for r in actual if r.endswith('/SKILL.md')} or len(ids)+1!=spec['canonical_count']:raise ValueError('Skill census mismatch')
    return spec,actual

def prepare(stage,target):
    with redirect_stdout(io.StringIO()):
        imrane.initialize(stage,apply=True)
        imrane.project_add(argparse.Namespace(workspace=str(stage),id='protrain',path='projects/ProTrain',name='ProTrain',git_init=False,apply=True,set_default=False))
    reg=read_json(stage/'.codex/projects.json');reg['default_project']=None;write_json(stage/'.codex/projects.json',reg)
    policy=read_json(ENGINE/'config/models.json')
    preset=read_json(ENGINE/'config/codex-sol-luna-6.json')
    for route,binding in preset['routes'].items():policy['routes'][route].update(binding)
    write_json(stage/'.codex/model-routing-policy.json',policy)
    automatic=read_json(ENGINE/'config/automatic-routing.json')
    automatic.update(enabled=True,authorized_by='Owner requested isolated portable ProTrain work system, 2026-11-13; host capabilities and access must be checked separately')
    write_json(stage/'.codex/automatic-routing.json',automatic)
    for rel,p in files(ROOT/'kit/governance').items():
        dest=safe(stage,'docs/governance/'+rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
    router=stage/'AGENTS.md'
    router.write_text(router.read_text(encoding='utf-8')+'\n'+(ROOT/'kit/WORKSPACE_RULES.md').read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    (stage/'.codex/memory/CURRENT.md').write_text('# Current governance state\n\nThe isolated ProTrain workspace is installed with one registered business lane at projects/ProTrain and no default project. Six Codex Luna/Sol routes are configured. Automatic one-worker routing is enabled by the owner-requested kit policy; actual models and native worker support remain host/account capabilities. Claude routing stays advisory. No dependencies or indexes were installed. Native hook autoload is unverified.\n\nNext: open projects/ProTrain, read its checkpoint and context index, verify local client trust/hooks and choose the business component.\n',encoding='utf-8')
    # Source project content overlays neutral init scaffolding. Runtime/auth never enters.
    for rel,p in payload().items():
        dest=safe(stage,'projects/ProTrain/'+rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(substitute(p.read_bytes(),target))
    scope={'include':['AGENTS.md',*('.codex/memory/'+m for m in MEMORIES)],'exclude':[]}
    write_json(stage/'projects/ProTrain/.codex/graphify-scope.json',scope)
    spec,skills=skill_payload()
    for rel,p in skills.items():
        for prefix in ('.agents/skills/','.claude/skills/'):
            dest=safe(stage,prefix+rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
    # Rebase generated hook paths to the real destination and active interpreter.
    for prefix in ('','projects/ProTrain/'):
        for rel,text in imrane.host_files(target,prefix).items():
            if rel.endswith('CLAUDE.md') and prefix and 'CLAUDE.md' in payload():continue
            dest=safe(stage,rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf-8',newline='\n')
        config=stage/(prefix+'.codex/config.toml')
        text=config.read_text(encoding='utf-8')
        text='developer_instructions = '+json.dumps('Read AGENTS.md first. Follow the isolated ProTrain workspace routing, permissions and checkpoint rules. Substantive Codex tasks use the one-worker policy when host/model capabilities are available; workers never delegate again.')+'\n\n'+text+'\n[agents]\nmax_concurrent_threads_per_session = 1\n'
        config.write_text(text,encoding='utf-8',newline='\n')
    with redirect_stdout(io.StringIO()):generate(stage,apply=True)
    # Legal files are installed beside the reusable engine and skill library.
    for rel in ['LICENSE.toolkit.txt','NOTICE.toolkit.md','kit/skills-manifest.json','kit/COURSE-NOTICE.md']:
        dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
    for p in (stage/'tools/systeme-imrane/scripts').rglob('__pycache__'):
        # No imports originate in the staging tree; this is a defensive assertion.
        raise ValueError('Unexpected staging cache: '+str(p))
    managed=read_json(stage/'.imrane/managed.json')
    for rel in managed['files']:
        p=safe(stage,rel)
        if p.is_file():managed['files'][rel]=sha(p.read_bytes())
    write_json(stage/'.imrane/managed.json',managed)
    return spec

def check(target):
    no_links(target)
    state=read_json(safe(target,STATE),{})
    if state.get('schema')!=1 or state.get('id')!='protrain-portable':raise ValueError('Not a portable-kit installation')
    missing=[];changed=[]
    for rel,h in state['files'].items():
        p=safe(target,rel)
        if not p.is_file():missing.append(rel)
        elif sha(p.read_bytes())!=h:changed.append(rel)
    reg=read_json(target/'.codex/projects.json',{})
    registry_ok=reg.get('default_project') is None and [(p.get('id'),p.get('path')) for p in reg.get('projects',[])]==[('protrain','projects/ProTrain')]
    views=files(target/'.agents/skills');mirror=files(target/'.claude/skills')
    mirror_ok=set(views)==set(mirror) and all(p.read_bytes()==mirror[r].read_bytes() for r,p in views.items())
    hooks_ok=True
    for prefix in ('','projects/ProTrain/'):
        for name in ('.codex/hooks.json','.claude/settings.json'):
            h=read_json(target/(prefix+name),{}).get('hooks',{})
            hooks_ok=hooks_ok and set(h)==set(imrane.EVENTS)
            for groups in h.values():
                for group in groups:
                    for handler in group['hooks']:
                        hooks_ok=hooks_ok and str(target/'tools/systeme-imrane/scripts/hooks.py') in handler['command'] and str(sys.executable) in handler['command']
    return {'ok':not missing and registry_ok and mirror_ok and hooks_ok,'mode':'check','workspace':str(target),'missing_baseline_files':missing,'changed_since_install':changed,'baseline_matches':not missing and not changed,'registry_ok':registry_ok,'skill_views_equal':mirror_ok,'generated_hooks_match_current_python_and_workspace':hooks_ok,'native_hooks_autoload':'unverified; reload each client and observe actual events','network_index':'not built or refreshed by this installer','note':'Changed working project files are reported, not overwritten. Baseline equality is not expected after authorized work.'}

def install(target,apply):
    if target.exists() and not target.is_dir():raise ValueError('Destination is not a directory')
    state=read_json(safe(target,STATE),{})
    if state and (state.get('schema')!=1 or state.get('id')!='protrain-portable' or not isinstance(state.get('files'),dict)):
        raise ValueError('Invalid existing install state; no files changed')
    if target.exists() and any(target.iterdir()) and not state:raise ValueError('Destination is not empty; no files changed')
    with tempfile.TemporaryDirectory(prefix='protrain-kit-stage-') as tmp:
        stage=Path(tmp)/'workspace';spec=prepare(stage,target)
        desired=files(stage);conflicts=[];creates=[]
        baseline={'schema':1,'id':'protrain-portable','version':'2026.11.13','workspace':target.as_posix(),'python':sys.executable,'files':{rel:sha(p.read_bytes()) for rel,p in desired.items()}}
        if state and state!=baseline:conflicts.append('Installed kit/interpreter/state differs; upgrades are not supported by bootstrap')
        for rel,p in desired.items():
            dest=safe(target,rel)
            if not dest.exists():creates.append(rel)
            elif not dest.is_file() or dest.read_bytes()!=p.read_bytes():conflicts.append(rel)
        result={'ok':not conflicts,'mode':'apply' if apply else 'plan','workspace':str(target),'canonical_skills':spec['canonical_count'],'files':len(desired),'new_files':len(creates),'conflicts':conflicts,'network_calls':False,'dependencies_installed':False,'global_config_changed':False}
        if conflicts or not apply:return result
        # Publishing is exclusive creation. Existing different data never gets replaced.
        target.mkdir(parents=True,exist_ok=True)
        for rel in creates:
            p=safe(target,rel);p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as handle:handle.write(desired[rel].read_bytes())
        statepath=safe(target,STATE);statepath.parent.mkdir(parents=True,exist_ok=True)
        if statepath.exists():
            old=read_json(statepath)
            if old!=baseline:raise ValueError('Existing install state differs; preserved')
        else:
            with statepath.open('x',encoding='utf-8') as handle:json.dump(baseline,handle,indent=2);handle.write('\n')
        result['verification']=check(target)
        result['ok']=result['verification']['ok']
        return result

def main():
    if sys.version_info<(3,11):raise ValueError('Python 3.11 or newer is required')
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('plan','apply','check','doctor'))
    parser.add_argument('--workspace',type=Path)
    args=parser.parse_args()
    if args.action=='doctor':
        from dependencies import inspect_dependencies
        target=destination(args.workspace) if args.workspace else None
        result={'ok':True,'mode':'doctor','python':sys.executable,'python_version':sys.version.split()[0],'bootstrap_runtime':'Python standard library only','optional_capabilities':inspect_dependencies('complete',target),'native_hooks_autoload':'unverified','accounts_and_plugins':'personal setup required; not bundled','network_calls':False}
    else:
        if args.workspace is None:parser.error('--workspace is required')
        target=destination(args.workspace)
        result=check(target) if args.action=='check' else install(target,args.action=='apply')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['ok'] else 1
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=False));raise SystemExit(1)
