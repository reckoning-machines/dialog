"""Actual public CS/scope witnesses, without manufactured passing checks."""
import copy,json,os,secrets,subprocess,sys,time,urllib.request
from pathlib import Path
from common import *
from cases import *
from startup import check
from arh_client import historical_document

class Service:
 def __init__(self,run,out):
  self.run=Path(run);self.out=Path(out);self.out.mkdir(parents=True,exist_ok=True);self.tc_auth=secrets.token_hex(32)
  self.config=self.run/'private/cs-config.json'
  write(self.config,{'connection':str(self.run/'private/service.json'),'tc_auth':self.tc_auth});os.chmod(self.config,0o600);self.start()
 def start(self):
  ready=self.run/'cs-ready.json'
  if ready.exists():ready.unlink()
  self.proc=subprocess.Popen([sys.executable,str(Path(__file__).with_name('control_service.py')),str(self.config),str(ready),str(self.out)],stdout=subprocess.DEVNULL,stderr=open(self.out/'stderr.log','ab'))
  for _ in range(200):
   if ready.exists():break
   if self.proc.poll() is not None:raise RuntimeError('CS startup failed')
   time.sleep(.025)
  self.endpoint='http://127.0.0.1:'+str(read(ready)['port'])+'/'
 def call(self,op,rid=None,caller='TC',auth=None,**body):
  body.update(op=op,request_id=rid or key())
  req=urllib.request.Request(self.endpoint,data=json.dumps(body).encode(),headers={'X-Caller':caller,'Authorization':'Bearer '+(auth or self.tc_auth),'Content-Type':'application/json'})
  return json.load(urllib.request.urlopen(req,timeout=20))
 def stop(self):self.proc.terminate();self.proc.wait(timeout=10)
 def restart(self):
  old=self.proc.pid;self.stop();self.start();write(self.out/'restart.json',{'old_pid':old,'old_terminated':True,'new_pid':self.proc.pid})

def cs_scope(run,out,emit):
 run=Path(run);out=Path(out);p,ck,t,r=clients(run);service=Service(run,out/'service');checks=[];observed={}
 def checked(tr,amount):
  b,c=check(ck,tr,amount);checks.append({'transition':tr,'amount':amount,'result':b['result'],'record':c.ref.as_dict()});write(out/('check-'+tr+'.json'),b);write(out/'checks.json',checks);return b,c
 def apply_service(tr):
  d=service.call('policy-decide',transition=tr);assert d['code']=='COMMITTED',d
  a=service.call('apply',transition=tr);assert a['code']=='COMMITTED',a
  return {'decision':d,'applied':a}
 try:
  h1,f1,_=hypothesis(t,'CS1',1)
  try:
   b1,c1=checked(h1,'0.50')
   raise AssertionError('The independently observed check-step rejection unexpectedly changed')
  except HarnessError as exc:
   rejection={'code':exc.code,'detail':str(exc)}
   assert exc.code=='UNFUNDED_CHECK',rejection
  emit('CS-01',False,{'expected':'valid 0.50 Check commit','observed':rejection,'source_constraint':'do_check_commit requires step check-transition; declared check-half is admitted at attempt but not Check commit'})
  candidate=next(x['receipt']['result'] for x in Principal(p).dispatch_status()['claims'] if x.get('receipt') and (x['receipt'].get('result') or {}).get('transition_id')==h1)
  role=[]
  for c in (t,r):
   for op,payload in [('check-commit',candidate),('decide',{'transition_id':h1,'check':1,'decision':'ADMITTED','reason':'Unauthorized researcher test'}),('policy-decide',{'transition_id':h1,'check':1})]:
    got=c.call(op,payload,key());assert not got.ok and got.reason=='UNAUTHORIZED',got.raw;role.append({'actor':c.actor,'operation':op,'response':got.raw})
  write(out/'role-refusals.json',role)
  emit('S-09',False,{'role_refusals_passed':role,'legitimate_0.50_check_blocked':rejection})
  t.call_or_raise('close',{'reservation':f1.sequence},key())
  bad,fb,_=hypothesis(t,'FAIL',2,bad=True);bb,bc=checked(bad,'0.25');assert bb['result']=='FAIL'
  assert service.call('policy-decide',transition=bad)['code']=='SERVICE_POLICY_PRECONDITION_REFUSED'
  failed=Principal(p).policy_decide(bad,bc.sequence,key());assert failed.reason=='CHECK_NOT_PASS'
  stop,fs,_=hypothesis(t,'STOP',3,missing=True);sb,sc=checked(stop,'0.25');assert sb['result']=='STOP'
  assert service.call('policy-decide',transition=stop)['code']=='SERVICE_POLICY_PRECONDITION_REFUSED'
  stale,ft,_=hypothesis(t,'STALE',4);stb,stc=checked(stale,'0.25');assert stb['result']=='PASS'
  raw,fr,_=hypothesis(t,'RAW',5);rb,rc=checked(raw,'0.25');assert rb['result']=='PASS'
  private=run/'private/raw-probe.json';write(private,{'transition':raw,'check':rc.sequence,'key':key()});os.chmod(private,0o600)
  subprocess.run([sys.executable,str(Path(__file__).with_name('raw_probe.py')),str(run/'private/service.json'),str(private),str(out/'raw-probe.json')],check=True)
  raw_result=read(out/'raw-probe.json');assert raw_result['decision']['status']=='COMMITTED'
  emit('CS-05',True,raw_result)
  old=Principal(p).policy_decide(stale,stc.sequence,key());assert old.reason=='STALE_CHECK',old.raw
  assert service.call('policy-decide',transition=stale)['code']=='SERVICE_POLICY_PRECONDITION_REFUSED'
  fresh,frc=checked(stale,'0.25');assert fresh['result']=='PASS'
  t.call_or_raise('close',{'reservation':ft.sequence},key())
  nofund=Principal(p).policy_decide(stale,frc.sequence,key());assert nofund.reason=='RESERVATION_CLOSED',nofund.raw
  for fund in (fb,fs):t.call_or_raise('close',{'reservation':fund.sequence},key())
  observed['CS-02-main']={'fail':bc.ref.as_dict(),'stop':sc.ref.as_dict(),'stale':old.raw,'missing_funding':nofund.raw}
  from control_service import DENIED
  denied=[]
  for op in DENIED:
   x=service.call(op);assert x['code']=='SERVICE_OPERATION_REFUSED' and not x['forwarded'];denied.append(x)
  x=service.call('status',caller='R-T',auth='wrong-caller');assert x['code']=='SERVICE_CALLER_REFUSED';denied.append(x)
  for op in DENIED:
   x=service.call(op,caller='R-T',auth='wrong-caller');assert x['code']=='SERVICE_CALLER_REFUSED' and not x['forwarded'];denied.append(x)
  emit('CS-04',True,{'responses':denied,'assertions':len(denied)})
  rid=key();service.call('grant',rid);assert service.call('fence',rid)['code']=='SERVICE_REQUEST_MISMATCH'
  drift,fd,_=hypothesis(t,'DRIFT',6);db,dc=checked(drift,'0.25');assert db['result']=='PASS'
  roots=p.state()['themes']
  observer=Observer(conn(run,'observer','Observation function'))
  rawbytes=json.dumps([{'row_id':'AAA-V2-quiet','return_bp':30,'quiet':True,'instrument':'AAA'},{'row_id':'BBB-V2-quiet','return_bp':25,'quiet':True,'instrument':'BBB'},{'row_id':'AAA-V2-quiet-2','return_bp':25,'quiet':True,'instrument':'AAA'}]).encode()
  doc=historical_document(rawbytes,'quiet-V2.json','predeclared synthetic V2');doc.update({'class':'synthetic','synthetic':True})
  obs=observer.observe('SRC-V-DATA',doc,'2026-10-28').raise_for_refusal()
  rr=ScopedResearcher(r);ref=event_ref(r.get(obs.ref))
  design=rr.record_body(None,'Does reversal work in quiet regimes?',{'question':'quiet-regime','parent':'bootstrap-reversal','input':ref},None,[ref],kind='EXPERIMENT DESIGN',parameters={'theme':'TH-V-R'},tool={'id':'CALC-V','planned':True})
  designref=rr.research_commit(design,key()).raise_for_refusal()
  rwork=work(run,'R-R','same-root-quiet','0.75');h19,f19,_=hypothesis(r,'S19',7)
  hb,hc=checked(h19,'0.25');assert hb['result']=='PASS',hb
  applied19=apply_service(h19);assert p.state()['themes']==roots
  emit('S-19',True,{'same_roots':True,'design':designref.ref.as_dict(),'work':rwork,'policy':applied19})
  driftref=service.call('policy-decide',transition=drift);assert driftref['code']=='SERVICE_POLICY_PRECONDITION_REFUSED'
  db2,dc2=checked(drift,'0.25');assert db2['result']=='PASS'
  request=key();first=service.call('policy-decide',request,transition=drift);assert first['code']=='COMMITTED'
  service.restart();replay=service.call('policy-decide',request,transition=drift);assert replay==first
  assert service.call('apply',request,transition=drift)['code']=='SERVICE_REQUEST_MISMATCH'
  assert service.call('apply',transition=drift)['code']=='COMMITTED'
  emit('CS-06',True,{'fresh_service':read(out/'service/restart.json'),'stale':driftref,'same_response':replay==first,'decision_count':len([x for x in p.history('T') if x['kind']=='DECISION' and x['transition_id']==drift])})
  content=copy.deepcopy(p.profile()['artifacts']['hypothesis_template']['content']);content.update(HypothesisId='H-OUTSIDE',motivated_by=['TH-CCC'])
  outside=rr.propose('HYPOTHESIS','H-OUTSIDE',content,'0.25',rr.next_evidence_sequence(),key(),transition_id='OUTSIDE')
  assert not outside.ok and outside.reason=='SCOPE_VIOLATION',outside.raw
  outside_service=service.call('policy-decide',transition='OUTSIDE')
  assert outside_service['code']=='SERVICE_POLICY_PRECONDITION_REFUSED' and not outside_service['forwarded']
  emit('S-20',True,{'local':'TB_SCOPE_CHANGE_REQUIRED','upstream':outside.raw,'no_dispatch':True})
  try:r.get({'ledger':'T','sequence':1,'sha256':'0'*64});raise AssertionError('Invalid exact reference accepted')
  except HarnessError as ex:ambiguity={'code':ex.code,'detail':str(ex)}
  emit('S-21',True,{'local':'TB_SCOPE_UNRESOLVED','lookup':ambiguity,'no_rewrite':True})
  worker=subprocess.Popen([sys.executable,str(Path(__file__).with_name('graph_worker.py')),'worker',str(run),'R-R','unknown'],stdout=subprocess.DEVNULL,stderr=open(out/'worker.log','ab'))
  from orchestrate import waitfile
  generation=waitfile(run/'ready-R-R.json');worker.kill();worker.wait(timeout=10)
  unknown=work(run,'R-R','R-R-parallel','1.00');refusal=replacement(run,'R-R','R-R-parallel');assert refusal['reason']=='WORKER_NOT_QUIESCENT'
  proof=service.call('quiesce',generation={'pid':worker.pid,'run':p.info['run_id']});assert proof['code']=='HOST_RESPONSE'
  success=replacement(run,'R-R','R-R-parallel');assert success['status']=='recorded'
  emit('CS-03',True,{'worker_pid':worker.pid,'returncode':worker.returncode,'uncertain':unknown,'before_proof':refusal,'proof':proof,'replacement':success})
  snapshot(run,out/'final');budgets=read(out/'final/budgets.json')
  assert budgets['AU-CK-V']['committed']=='4.50',budgets
  assert budgets['G-R']['committed']=='2.25' and budgets['G-R']['spendable']=='7.00',budgets
  write(out/'checks.json',checks);write(out/'observed.json',observed);return observed
 finally:service.stop()
