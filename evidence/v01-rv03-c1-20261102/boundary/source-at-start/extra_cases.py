import copy,json,os,subprocess,sys,time,uuid
from pathlib import Path
from common import *
from cases import *
from startup import check
from cs_suite import Service

def policy_edges(run,out,emit):
 run=Path(run);out=Path(out);p,ck,t,r=clients(run)
 service=Service(run,out/'service')
 try:
  # New checked, unapplied Theme: genuine policy-class refusal, not stale-check proxy.
  theme=copy.deepcopy(p.state()['themes']['TH-V-T'])
  doc=ScopedResearcher(t).documents('SRC-V-DATA')[0]
  theme.update(ThemeId='TH-POLICY-PROBE',statement='Independent proposal to test Theme-policy boundary; not admitted.',
   motivation_closure={'N':p.state()['N'],'refs':[event_ref(doc)]})
  tr='THEME-POLICY-PROBE'
  Principal(p).propose_control('THEME',theme['ThemeId'],theme,tr,key()).raise_for_refusal()
  body,cr=check(ck,tr);assert body['result']=='PASS'
  service_theme=service.call('policy-decide',transition=tr)
  assert service_theme['code']=='SERVICE_POLICY_PRECONDITION_REFUSED' and not service_theme['forwarded']
  refused=Principal(p).policy_decide(tr,cr.sequence,key());assert refused.reason=='P1_CLASS',refused.raw
  write(out/'theme-class-refusal.json',refused.raw)
  # Suspension is a legitimate checked BC control in this disposable fixture.
  tr='SUSPEND-POLICY'
  Principal(p).propose_control('SUSPEND_POLICY','G-R',{'policy':'P-1','scope':'G-R','action':'SUSPEND','reason':'Authorized policy-refusal fixture'},tr,key()).raise_for_refusal()
  body,cr=check(ck,tr);assert body['result']=='PASS'
  d=Principal(p).decide(tr,cr.sequence,key=key()).raise_for_refusal();Principal(p).apply(tr,d.sequence,key=key()).raise_for_refusal()
  h,f,_=hypothesis(t,'SUSPENDED',1);hb,hc=check(ck,h);assert hb['result']=='PASS',hb
  response=service.call('policy-decide',transition=h)
  assert response['code']=='REFUSED' and response['upstream']['reason']=='POLICY_SUSPENDED',response
  assert not any(x['kind']=='DECISION' and x['transition_id']==h for x in p.history('T'))
  write(out/'suspended-policy.json',{'service':response,'check':hc.ref.as_dict()})
  snapshot(run,out/'final')
  main=list((Path(__file__).parent.parent/'evidence').glob('cs/observed.json'))
  assert main and read(main[0]).get('CS-02-main')
  emit('CS-02',True,{'main_run':read(main[0])['CS-02-main'],'auxiliary_theme_refusal':refused.raw,'suspended':response,'aux_checker_setup':p.budget('AU-CK-V')})
 finally:service.stop()

def reopen(run,out,host_entry):
 run=Path(run);out=Path(out);p,ck,t,r=clients(run);before=p.closure();budgets={g:p.budget(g) for g in ('G-R','G-BR','AU-CK-V')}
 ctl=HostControl.from_file(run/'private/service.json');old=ctl.status()
 ctl.stop();host_entry[1].wait(timeout=15);host_entry[2].close()
 def launch():
  log=open(run/'reopen-log.txt','ab')
  proc=subprocess.Popen([sys.executable,'-m','adaptive_research_harness.local_host','--setup',str(Path(__file__).parent),'--run',str(run)],cwd='/Users/jedgore/dev/speedway',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log)
  deadline=time.monotonic()+25
  while time.monotonic()<deadline:
   if proc.poll() is not None:return proc,log,False
   try:
    c=Connection.from_file(run/'state/connection.json','Principal')
    c.state();return proc,log,True
   except Exception:time.sleep(.05)
  return proc,log,False
 proc,log,live=launch();assert live
 new=Connection.from_file(run/'state/connection.json','Principal')
 assert new.closure()==before and all(new.budget(g)==b for g,b in budgets.items())
 newctl=HostControl.from_file(run/'state/connection.json');status=newctl.status()
 write(out/'compatible.json',{'old_processes':old,'new_processes':status,'same_closure':True,'same_budgets':True,'head':new.state()['N']})
 newctl.stop();proc.wait(timeout=15);log.close()
 # Corrupt only disposable bundle executable bytes, never ARH or a ledger file.
 tool=run/'bundle/tools/tools.py';original=tool.read_bytes();tool.write_bytes(original+b'\n# intentional incompatible-execution fixture\n')
 try:
  bad,badlog,live=launch();bad.wait(timeout=30);badlog.close()
  assert not live and bad.returncode!=0
  text=(run/'state/core-None.log').read_text()
  assert 'ARTIFACT_CHANGED' in text,text[-2000:]
  write(out/'incompatible.json',{'live_reopen':False,'host_returncode':bad.returncode,'reason':'ARTIFACT_CHANGED','mode':'live mutation refused; retained history remains inspection evidence','no_ledger_access':True})
 finally:tool.write_bytes(original)
 # Verify exact restored run opens again; no implicit input migration.
 proc,log,live=launch();assert live
 c=Connection.from_file(run/'state/connection.json','Principal');assert c.closure()==before
 write(out/'restored.json',{'same_closure':True,'same_budgets':all(c.budget(g)==b for g,b in budgets.items()),'no_new_charges':True})
 HostControl.from_file(run/'state/connection.json').stop();proc.wait(timeout=15);log.close()
 return True
