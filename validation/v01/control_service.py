"""CS-V1: cooperative owner service, explicitly not an ARH credential sandbox."""
import hashlib
import hmac
import json
import os
import sys
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from arh_client import Connection, Principal, HostControl

DENIED=('decide','grant','limits','standard','fence','tick','token-export','scope-extension')
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def serve(config_file, ready, evidence):
 cfg=json.loads(Path(config_file).read_text())
 conn=Connection.from_file(cfg['connection'],'Principal');principal=Principal(conn)
 control=HostControl.from_file(cfg['connection'])
 out=Path(evidence);out.mkdir(parents=True,exist_ok=True)
 seen={};forwarded=0;events=[]
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal forwarded
   body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
   caller=self.headers.get('X-Caller','');auth=self.headers.get('Authorization','')
   method=body.get('op');request=body.get('request_id')
   fingerprint=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
   forward=False
   if caller!='TC' or not hmac.compare_digest(auth,'Bearer '+cfg['tc_auth']):code='SERVICE_CALLER_REFUSED'
   elif not isinstance(request,str):code='SERVICE_REQUEST_ID_REQUIRED'
   elif request in seen and seen[request]!=fingerprint:code='SERVICE_REQUEST_MISMATCH'
   elif method not in ('policy-decide','apply','inspect','obligations','quiesce','status'):code='SERVICE_OPERATION_REFUSED'
   else:
    # Actual positive calls need currently valid public records; core still decides.
    seen[request]=fingerprint
    if method in ('policy-decide','apply'):
     tr=body.get('transition');events_t=conn.history('T')
     p=next((e for e in events_t if e['kind']=='PROPOSED' and e['transition_id']==tr),None)
     checks=[e for e in events_t if e['kind']=='CHECK' and e['transition_id']==tr]
     if not p or p['body']['class']!='HYPOTHESIS' or not checks or checks[-1]['body']['result']!='PASS' or checks[-1]['body']['base']!=conn.state()['N']:
      code='SERVICE_POLICY_PRECONDITION_REFUSED'
     elif method=='policy-decide':
      forwarded+=1;forward=True;response=principal.policy_decide(tr,checks[-1]['seq'],key=request).raw;code=response.get('status')
     else:
      decisions=[e for e in events_t if e['kind']=='DECISION' and e['transition_id']==tr and e['body'].get('decider','').startswith('P-1')]
      if not decisions:code='SERVICE_POLICY_DECISION_REQUIRED'
      else:
       forwarded+=1;forward=True;response=principal.apply(tr,decisions[-1]['seq'],key=request).raw;code=response.get('status')
    elif method=='quiesce':
     forwarded+=1;forward=True;response=control.quiesce(body.get('generation'));code='HOST_RESPONSE'
    elif method=='status':
     forwarded+=1;forward=True;response=control.status();code='HOST_RESPONSE'
    elif method=='inspect':
     forwarded+=1;forward=True;response=conn.outcome(body.get('original_key'));code=response.get('status')
    else:
     forwarded+=1;forward=True;response=conn.obligations();code='OBSERVED'
   if request and caller=='TC' and hmac.compare_digest(auth,'Bearer '+cfg['tc_auth']):seen.setdefault(request,fingerprint)
   result={'code':code,'forwarded':forward,'request_id':request}
   # No credentials, request payload, connection object or HTTP headers retained.
   events.append({'caller':caller,'operation':method,**result,'service_pid':os.getpid()})
   write(out/'service-events.json',events);write(out/'forwarding-count.json',{'forwarded':forwarded})
   raw=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 server=HTTPServer(('127.0.0.1',0),Handler)
 write(ready,{'port':server.server_port,'service_pid':os.getpid(),'upstream_actor':'Principal'})
 server.serve_forever()
if __name__=='__main__':serve(*sys.argv[1:])
