"""BC-only provisioning process. Exits before the independent TC starts requests."""
import json,os,secrets,subprocess,sys,time
from pathlib import Path
from common import write,read,key
from orchestrate import start,prepare,OUT,SOURCE,waitfile
from cases import clients,hypothesis,snapshot
from startup import check
from arh_client import HostControl,Connection

def bootstrap():
 run=start('boundary');prepare(run,'boundary');p,ck,t,r=clients(run)
 tr,f,content=hypothesis(t,'BOUNDARY',1);body,cr=check(ck,tr);assert body['result']=='PASS'
 snapshot(run,OUT/'boundary/provisioned')
 # Service receives only its Principal view. TC receives only its own caller key.
 tc_key=secrets.token_hex(32)
 cfg=run/'private/boundary-cs.json';write(cfg,{'connection':str(run/'private/service.json'),'tc_auth':tc_key});os.chmod(cfg,0o600)
 service=subprocess.Popen([sys.executable,str(SOURCE/'control_service.py'),str(cfg),str(run/'boundary-ready.json'),str(OUT/'boundary/service')],stdout=subprocess.DEVNULL,stderr=open(run/'boundary-service.log','ab'))
 ready=waitfile(run/'boundary-ready.json')
 tc=run/'private/tc-only.json';write(tc,{'endpoint':'http://127.0.0.1:'+str(ready['port'])+'/','caller':'TC','tc_auth':tc_key});os.chmod(tc,0o600)
 write(OUT/'boundary/handles.json',{'run_name':run.name,'bootstrap_pid':os.getpid(),'service_pid':service.pid,'transition':tr,'check':cr.ref.as_dict(),'funding':f.ref.as_dict(),'tc_only_file':str(tc),
 'identity_boundary':'cooperative same-user process separation; no OS isolation',
 'mode_0600':{label:oct((run/'private'/(label+'.json')).stat().st_mode & 0o777) for label in ('service','checker','trend','reversal')},
 'raw_principal_file_readable_by_same_uid':os.access(run/'private/service.json',os.R_OK)})
 print(json.dumps({'bootstrap_complete':True,'run_name':run.name}),flush=True)

def finish():
 h=read(OUT/'boundary/handles.json');run=ROOT_RUN=SOURCE.parent/'runtime'/h['run_name']
 snapshot(run,OUT/'boundary/final')
 status=HostControl.from_file(run/'private/service.json').status()
 write(OUT/'boundary/stopped-host.json',{'status_before':status,'stop':HostControl.from_file(run/'private/service.json').stop(),'custodian_pid':os.getpid()})

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='finish':finish()
 else:bootstrap()
