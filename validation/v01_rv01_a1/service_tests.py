"""Separate BC launcher, service process and TC negative-test process."""
import json
import os
import secrets
import subprocess
import sys
import time
import uuid
import urllib.request
from pathlib import Path
from control_service import DENIED
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def tc(endpoint,tc_file,out):
 secret=json.loads(Path(tc_file).read_text())['auth']
 results=[]
 def call(op,rid=None,caller='TC',auth=None):
  body={'op':op,'request_id':rid or str(uuid.uuid4())}
  req=urllib.request.Request(endpoint,data=json.dumps(body).encode(),headers={'X-Caller':caller,'Authorization':'Bearer '+(auth or secret),'Content-Type':'application/json'})
  return json.load(urllib.request.urlopen(req,timeout=10))
 for op in DENIED:
  got=call(op);results.append({'witness':'CS-04','op':op,'expected':'SERVICE_OPERATION_REFUSED','observed':got,'pass':got['code']=='SERVICE_OPERATION_REFUSED' and not got['forwarded']})
 rid=str(uuid.uuid4());call('grant',rid)
 got=call('fence',rid);results.append({'witness':'CS-06-partial','expected':'SERVICE_REQUEST_MISMATCH','observed':got,'pass':got['code']=='SERVICE_REQUEST_MISMATCH' and not got['forwarded']})
 got=call('status',caller='R-T',auth='invalid-designated-researcher-credential')
 results.append({'witness':'CS-04','expected':'SERVICE_CALLER_REFUSED','observed':got,'pass':got['code']=='SERVICE_CALLER_REFUSED' and not got['forwarded']})
 write(out,{'controller_pid':os.getpid(),'results':results,'count':len(results),'passed':sum(x['pass'] for x in results)})
def launch(run,evidence):
 run=Path(run);out=Path(evidence);out.mkdir(parents=True,exist_ok=True);private=run/'private'
 tc_auth=secrets.token_hex(32)
 write(private/'tc.json',{'auth':tc_auth});os.chmod(private/'tc.json',0o600)
 write(private/'service-config.json',{'connection':str(private/'service.json'),'tc_auth':tc_auth});os.chmod(private/'service-config.json',0o600)
 ready=out/'service-ready.json'
 proc=subprocess.Popen([sys.executable,str(Path(__file__).with_name('control_service.py')),str(private/'service-config.json'),str(ready),str(out)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  for _ in range(100):
   if ready.exists():break
   if proc.poll() is not None:raise RuntimeError('Service exited before ready')
   time.sleep(.05)
  endpoint='http://127.0.0.1:'+str(json.loads(ready.read_text())['port'])+'/'
  child=subprocess.run([sys.executable,__file__,'tc',endpoint,str(private/'tc.json'),str(out/'tc-results.json')],capture_output=True,text=True,check=True)
  write(out/'process-boundary.json',{'custodian_launcher_pid':os.getpid(),'service_pid':proc.pid,'controller_separate':True,
   'full_connection_not_supplied_to_TC':True,'TC_arguments':'endpoint, TC-specific-auth-file, output; no Principal credential'})
 finally:
  proc.terminate();proc.wait(timeout=10)
  write(out/'service-termination.json',{'pid':proc.pid,'returncode':proc.returncode,'wait_confirmed':True})
 print((out/'tc-results.json').read_text())
if __name__=='__main__':
 if sys.argv[1]=='tc':tc(*sys.argv[2:])
 else:launch(*sys.argv[1:])
