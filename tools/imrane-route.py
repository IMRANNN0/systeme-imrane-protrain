"""Choose the authorized native worker; emit metadata, never execute hidden agents."""
import argparse,hashlib,json,sys,tomllib
import os
import re
from pathlib import Path
from uuid import uuid4
W=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(W/'tools/systeme-imrane/scripts'))
from common import read_json,resolve_project,runtime_dir,write_json,now
from routing import recommend

class BindingPolicyError(ValueError):
    """The local automatic policy rejected the requested worker binding."""

def prepare_host_config(text,instruction):
    """Pure preflight: keep existing settings and reject instruction/cap conflicts."""
    data=tomllib.loads(text)
    if data.get('features',{}).get('hooks') is not True:
        raise ValueError('Hooks are not enabled; preserve configuration for review')
    if data.get('developer_instructions'):
        if data['developer_instructions']!=instruction:
            raise ValueError('Existing developer instructions preserved; review merge')
    else:text='developer_instructions = '+json.dumps(instruction,ensure_ascii=False)+'\n\n'+text
    agents=data.get('agents')
    if agents is None:
        text+='\n[agents]\nmax_concurrent_threads_per_session = 1\n'
    elif agents.get('max_concurrent_threads_per_session')!=1:
        raise ValueError('Existing agents settings preserved; review worker cap')
    assert tomllib.loads(text)['agents']['max_concurrent_threads_per_session']==1
    return text

def receipt_path(workspace, project_id, dispatch_id):
    if not isinstance(dispatch_id, str) or not re.fullmatch(r"[0-9a-f]{32}", dispatch_id):
        raise ValueError("Invalid dispatch id")
    path = runtime_dir(workspace, project_id) / "routing" / "receipts" / f"{dispatch_id}.json"
    if path.resolve() != path:
        raise ValueError("Linked receipt path refused")
    return path


def route(workspace,cwd,prompt,session_id,task_id=None):
    workspace=Path(workspace).resolve()
    project=resolve_project(workspace,cwd)
    if project is None:raise ValueError('No scope resolved inside workspace')
    automatic=read_json(workspace/'.codex/automatic-routing.json',{})
    if not automatic.get('enabled') or automatic.get('host')!='codex':raise ValueError('Automatic Codex routing is not enabled')
    policy=read_json(workspace/'.codex/model-routing-policy.json')
    session=hashlib.sha256(session_id.encode()).hexdigest()[:20]
    # Separate controller dispatch state from lifecycle hook state.
    path=runtime_dir(workspace,project['id'])/'routing'/(session+'.json')
    previous=read_json(path,{})
    if task_id is not None and (not isinstance(task_id, str) or not task_id.strip() or len(task_id) > 160):
        raise ValueError("Task id must be a nonempty string of up to 160 characters")
    task_hash = hashlib.sha256(task_id.encode()).hexdigest()[:20] if task_id else None
    if previous.get("task_hash") != task_hash:
        previous = {}
    result=recommend(prompt,previous,policy)
    binding=policy['routes'][result['route']]
    model=binding.get('codex_model')
    if model not in ('gpt-6-luna','gpt-6.1-sol'):
        raise BindingPolicyError('Automatic Codex workers must use GPT-6 Luna or GPT-6.1 Sol')
    effort=result['reasoning']
    if effort not in ('low','medium','high'):
        raise BindingPolicyError('Automatic Codex worker effort exceeds the high cap; review the policy and regenerate the roles')
    dispatch_id = uuid4().hex
    decision={**result,'at':now(),'project_id':project['id'],'model':model,'reasoning_effort':effort,'agent':binding['agent'],'execution':'native_subagent','dispatch_status':'planned','dispatch_id':dispatch_id,'task_hash':task_hash,'max_workers':1,'nested_delegation':False,'active_controller_model_changed':False}
    receipt = {key: decision[key] for key in
               ("at", "project_id", "dispatch_id", "dispatch_status", "agent", "model", "reasoning_effort")}
    write_json(receipt_path(workspace, project["id"], dispatch_id),
               {**receipt, "session_hash": session}, private=True)
    write_json(path,decision,private=True)
    return decision


def record_receipt(workspace, cwd, session_id, dispatch_id, status, worker_id=None):
    project = resolve_project(workspace, cwd)
    if project is None:
        raise ValueError("No scope resolved inside workspace")
    path = receipt_path(workspace, project["id"], dispatch_id)
    if not path.is_file():
        raise ValueError("No plan for this dispatch in the selected scope")
    if status not in ("started", "finished", "failed"):
        raise ValueError("Invalid receipt status")
    if worker_id is not None and (not isinstance(worker_id, str) or
                                  not re.fullmatch(r"[A-Za-z0-9._/:-]{1,160}", worker_id)):
        raise ValueError("Invalid native worker id")
    lock = path.with_suffix(".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        receipt = read_json(path)
        if receipt["session_hash"] != hashlib.sha256(session_id.encode()).hexdigest()[:20]:
            raise ValueError("Dispatch belongs to another session")
        previous = receipt["dispatch_status"]
        recorded = receipt.get("worker_id")
        if status == previous and recorded == worker_id:
            return receipt
        if (previous, status) not in {
            ("planned", "started"), ("planned", "failed"), ("started", "finished"), ("started", "failed")
        }:
            raise ValueError("Invalid dispatch status transition")
        if status == "started" and not worker_id:
            raise ValueError("A started dispatch requires a native worker id")
        if previous == "started" and worker_id != recorded:
            raise ValueError("Native worker id does not match the started dispatch")
        if previous == "planned" and status == "failed" and worker_id is not None:
            raise ValueError("A dispatch that failed to start has no worker id")
        receipt["dispatch_status"] = status
        receipt[f"{status}_at"] = now()
        if worker_id:
            receipt["worker_id"] = worker_id
        write_json(path, receipt, private=True)
        return receipt
    finally:
        lock.unlink()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',default=str(W));p.add_argument('--cwd',default=str(Path.cwd()));p.add_argument('--session-id',required=True)
    args=p.parse_args()
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8-sig")
    raw=sys.stdin.read(1_048_577)
    if len(raw)>1_048_576:raise ValueError('Input exceeds budget')
    payload=json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("JSON stdin requires an object")
    if "dispatch_id" in payload:
        result = record_receipt(Path(args.workspace).resolve(), args.cwd, args.session_id, payload["dispatch_id"],
                                payload.get("status"), payload.get("worker_id"))
    else:
        prompt=payload.get('prompt')
        if not isinstance(prompt,str):raise ValueError('JSON stdin requires a prompt string')
        result = route(args.workspace,args.cwd,prompt,args.session_id,payload.get("task_id"))
    print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':
    try:main()
    except BindingPolicyError as exc:
        print('ROUTING_ERROR: '+str(exc),file=sys.stderr);raise SystemExit(1)
    except Exception as exc:
        print('ROUTING_ERROR: '+type(exc).__name__,file=sys.stderr);raise SystemExit(1)
