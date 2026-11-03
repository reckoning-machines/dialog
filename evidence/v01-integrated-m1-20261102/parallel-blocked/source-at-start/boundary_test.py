"""TC: reads its caller credential only; never loads ARH connection/token files."""
import json,os,subprocess,sys,urllib.request,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def main():
 boot=subprocess.run([sys.executable,str(ROOT/'source/boundary_worker.py')],capture_output=True,text=True)
 out=ROOT/'evidence/boundary';write(out/'bootstrap-process.json',{'returncode':boot.returncode,'stdout':boot.stdout,'stderr':boot.stderr})
 assert boot.returncode==0
 h=read(out/'handles.json');cfg=read(h['tc_only_file'])
 assert set(cfg)=={'endpoint','caller','tc_auth'}
 def call(op,**values):
  body={'op':op,'request_id':str(uuid.uuid4()),**values}
  request=urllib.request.Request(cfg['endpoint'],data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-Caller':cfg['caller'],'Authorization':'Bearer '+cfg['tc_auth']})
  return json.load(urllib.request.urlopen(request,timeout=20))
 before=call('status');assert before['code']=='HOST_RESPONSE'
 d=call('policy-decide',transition=h['transition']);assert d['code']=='COMMITTED',d
 a=call('apply',transition=h['transition']);assert a['code']=='COMMITTED',a
 refusals=[]
 for op in ('decide','grant','limits','standard','fence','tick','token-export','scope-extension'):
  x=call(op);assert x['code']=='SERVICE_OPERATION_REFUSED' and not x['forwarded'];refusals.append(x)
 obligations=call('obligations');assert obligations['code']=='OBSERVED'
 write(out/'separation-witness.json',{'status':'PASS','tc_pid':os.getpid(),'bc_pid':h['bootstrap_pid'],'bc_terminated_before_tc_requests':True,
 'tc_inputs_have_no_principal_credential':True,'service_actor':'Principal','credential_scope':'broad; allowlist is application code',
 'same_uid_raw_credential_readable':h['raw_principal_file_readable_by_same_uid'],'os_isolation':False,'policy':d,'apply':a,'refusals':refusals,'obligations':obligations,'status_before':before})
 os.kill(h['service_pid'],15)
 # Host shutdown occurs in a separate custodian, which never passes TC a token.
 subprocess.run([sys.executable,str(ROOT/'source/boundary_worker.py'),'finish'],check=True)
 print('Control-service provisioning/process witness PASS',flush=True)

if __name__=='__main__':main()
