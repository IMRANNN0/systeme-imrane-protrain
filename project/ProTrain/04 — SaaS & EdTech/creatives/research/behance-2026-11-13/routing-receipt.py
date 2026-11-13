import io,json,runpy,sys
from pathlib import Path
root=Path(__file__).parent
payload={'prompt':'[route:sol] Complex Behance visual research and art direction report for ProTrain Match; no static ad production','task_id':'ptm-behance-20261113'}
if len(sys.argv)>1:
    payload={'dispatch_id':sys.argv[1],'status':sys.argv[2],'worker_id':'/root/art_direction_review'}
sys.stdin=io.StringIO(json.dumps(payload))
sys.argv=['imrane-route.py','--session-id','ptm-behance-20261113']
runpy.run_path('{{IMRANE_WORKSPACE_ROOT}}/tools/imrane-route.py',run_name='__main__')
