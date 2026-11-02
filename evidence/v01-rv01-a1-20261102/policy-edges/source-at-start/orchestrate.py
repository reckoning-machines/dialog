"""Authorized RV-01-A1 consumer witness runner; no core imports or ledger access."""
import copy,hashlib,json,os,signal,subprocess,sys,time,uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from common import *
from cases import *
from startup import check
from arh_client import historical_document

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'source';OUT=ROOT/'evidence';HOSTS=[];RESULTS=read(OUT/'results.json') if (OUT/'results.json').exists() else {}
ARH=Path('/Users/jedgore/dev/speedway')
PY=sys.executable

def waitfile(p,timeout=30):
 end=time.monotonic()+timeout
 while not Path(p).exists():
  if time.monotonic()>end:raise TimeoutError(str(p))
  time.sleep(.03)
 return read(p)
def outcome(name,passed,details):
 RESULTS[name]={'status':'PASS' if passed else 'FAIL','details':details};write(OUT/'results.json',RESULTS)
 print(name,RESULTS[name]['status'],flush=True)
def start(name):
 
 if (OUT/name).exists():(OUT/name).rename(OUT/(name+'-prior-'+uuid.uuid4().hex[:8]))
 run=ROOT/'runtime'/(name+'-'+uuid.uuid4().hex[:8]);run.mkdir(parents=True,exist_ok=True)
 logfile=open(run/'host-stdout.log','ab')
 proc=subprocess.Popen([PY,'-m','adaptive_research_harness.local_host','--setup',str(SOURCE),'--run',str(run)],cwd=ARH,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=logfile,stderr=logfile)
 HOSTS.append((run,proc,logfile));waitfile(run/'state/connection.json')
 boot=subprocess.run([PY,str(SOURCE/'startup.py'),str(run),str(OUT/name/'startup')],capture_output=True,text=True)
 write(OUT/name/'startup-process.json',{'returncode':boot.returncode,'stdout':boot.stdout,'stderr':boot.stderr})
 if boot.returncode or (OUT/name/'startup/blocked.json').exists():raise RuntimeError('startup failed '+name)
 write(OUT/name/'source-hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob('*') if p.is_file()})
 return run

def prepare(run,name):
 p,ck,t,r=clients(run)
 # Pre-dispatch conservative planning includes pending + retained, before any work.
 preflight={'per_lineage_ceiling':'10.00','bootstrap_max_each':'2.00 reservation /1.00 attempt',
 'measured_peak_each':'5.75' if name=='cs' else '5.50' if name=='contention' else '2.00',
 'maximum_bootstrap_plus_measured_usage':'7.75' if name=='cs' else '7.50' if name=='contention' else '4.00',
 'fits':True,'measured_shared_pool':'10.00','checker_cap':'12.00','prior_run_charges_not_reused':True,
 'authoritative_initial':{g:p.budget(g) for g in ('G-BR','G-R','AU-CK-V')}}
 assert all(x['committed']=='0.00' for g,x in preflight['authoritative_initial'].items() if g!='AU-CK-V')
 write(OUT/name/'preflight.json',preflight)
 # Add a genuine negative cohort before the reversal result; not a fabricated Check.
 obs=Observer(conn(run,'observer','Observation function'))
 raw=json.dumps([{'row_id':'AAA-QUIET','return_bp':-20,'quiet':True,'instrument':'AAA'}, {'row_id':'BBB-QUIET','return_bp':-10,'quiet':True,'instrument':'BBB'}]).encode()
 doc=historical_document(raw,'negative-cohort.json','deterministic V-01 synthetic cohort');doc.update({'class':'synthetic','synthetic':True})
 obs.observe('SRC-V-DATA',doc,'2026-10-28').raise_for_refusal()
 a=work(run,'R-T','bootstrap-trend',actual='0.75',grant='G-BR')
 b=work(run,'R-R','bootstrap-reversal',actual='1.00',grant='G-BR')
 for c,own,other in ((t,a,b),(r,b,a)):
  rr=ScopedResearcher(c);rr.grant_id='G-BR'
  result={'analysis':own['record'],'shared_failure_reference':other['record'],'chosen':'own','candidates':[],
  'rejections':[{'id':'unrestricted-repeat','reason':'Shared observed synthetic cost/failure history; do not claim a reused cohort untouched','reconsider_when':'new_documents'}],
  'next_question':'Volatility robustness' if c.actor=='R-T' else 'Quiet-regime reversal',
  'reason':'Retained both researcher variants; no inherited scientific support'}
  body=rr.record_body(None,'Select next investigation from shared history',result,None,[event_ref(c.get(own['record'])),event_ref(c.get(other['record']))],kind='SELECTION',parameters={'theme':'TH-V-T' if c.actor=='R-T' else 'TH-V-R'},tool={'id':'CALC-V','planned':True})
  rr.research_commit(body,key()).raise_for_refusal()
 fence_bootstrap(run)
 records=t.history('E');selections=[e for e in records if e['kind']=='RESEARCH_RECORD' and e['body'].get('kind')=='SELECTION']
 assert len(selections)==2 and all(e['body']['result'].get('shared_failure_reference') for e in selections)
 write(OUT/name/'shared-history.json',selections)
 snapshot(run,OUT/name/'ready')

def contention():
 name='contention';run=start(name);prepare(run,name);p,ck,t,r=clients(run)
 for i in range(9):prefix(t,'trend-prefix-'+str(i));prefix(r,'reversal-prefix-'+str(i))
 assert t.budget('G-R')['committed']=='9.00'
 def reserve(c):return c.call('reserve',{'grant':'G-R','amount':'1.00','purpose':{'kind':'Theme','id':'TH-V-T' if c.actor=='R-T' else 'TH-V-R'}},key())
 import threading
 barrier=threading.Barrier(2)
 def race(c):barrier.wait();return reserve(c)
 with ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(race,[t,r]))
 write(OUT/name/'race.json',[x.raw for x in res]);b=t.budget('G-R')
 outcome('S-05',sum(x.ok for x in res)==1 and sorted(x.reason for x in res if not x.ok)==['BUDGET_EXCEEDED'] and b['spendable']=='0.00',{'budget':b,'receipts':[x.raw for x in res]})
 winner=next((c,x) for c,x in zip((t,r),res) if x.ok)
 winner[0].call_or_raise('close',{'reservation':winner[1].sequence},key());snapshot(run,OUT/name/'final')

def parallel(blocked):
 name='parallel-blocked' if blocked else 'parallel-success';run=start(name);prepare(run,name)
 coordinator=subprocess.Popen([PY,str(SOURCE/'graph_worker.py'),'block',str(run)],stdout=open(run/'coordinator.log','ab'),stderr=subprocess.STDOUT)
 ready={a:waitfile(run/('ready-'+a+'.json')) for a in ('R-T','R-R')}
 for a,x in ready.items():os.kill(x['pid'],signal.SIGKILL)
 for a in ready:waitfile(run/('reaped-'+a+'.json'))
 coordinator.kill();coordinator.wait(timeout=10)
 write(OUT/name/'forced-death.json',{'coordinator_pid':coordinator.pid,'coordinator_returncode':coordinator.returncode,'workers':ready,'workers_reaped_before_proof':True})
 t=work(run,'R-T','R-T-parallel',actual='0.75');r=work(run,'R-R','R-R-parallel',actual='1.00')
 no_proof=replacement(run,'R-R','R-R-parallel')
 assert no_proof['reason']=='WORKER_NOT_QUIESCENT',no_proof
 write(OUT/name/'before-proof.json',{'trend':t,'reversal':r,'replacement':no_proof});snapshot(run,OUT/name/'before-proof-snapshot')
 if blocked:
  # Fresh process sees same blocked attempt; do not turn absence of a receipt into permission.
  subprocess.run([PY,str(SOURCE/'state_reader.py'),str(run),str(OUT/name/'fresh-reader.json')],check=True)
  subprocess.run([PY,str(SOURCE/'graph_worker.py'),'resume',str(run)],check=True)
  graph_state=read(run/'graph-result.json');assert '__interrupt__' in graph_state
  b=clients(run)[0].budget('G-R');outcome('S-15B',b['committed']=='1.75' and b['spendable']=='7.25',{'budget':b,'replacement':no_proof})
 else:
  ctl=HostControl.from_file(run/'private/service.json');proofs=[]
  for x in ready.values():proofs.append(ctl.quiesce({'pid':x['pid'],'run':ctl.info['run_id']}))
  yes=replacement(run,'R-R','R-R-parallel');assert yes['status']=='recorded'
  b=clients(run)[0].budget('G-R')
  # Replay the original trend journal, never claim it anew.
  again=work(run,'R-T','R-T-parallel',actual='0.75');assert again['attempt']==t['attempt']
  subprocess.run([PY,str(SOURCE/'graph_worker.py'),'resume',str(run)],check=True)
  graph_state=read(run/'graph-result.json');assert graph_state['trend']['status']=='recorded' and graph_state['reversal']['status']=='recorded'
  assert clients(run)[0].budget('G-R')==b
  write(OUT/name/'proof-and-replacement.json',{'proofs':proofs,'replacement':yes,'replayed_trend':again})
  snapshot(run,OUT/name/'final')
  outcome('S-15A',b['committed']=='2.25' and b['spendable']=='7.75',{'budget':b,'replacement':yes})
 return run

if __name__=='__main__':
 try:
  if sys.argv[1]=='contention':contention()
  elif sys.argv[1]=='parallel-success':parallel(False)
  elif sys.argv[1]=='parallel-blocked':parallel(True)
  elif sys.argv[1]=='cs':
   from cs_suite import cs_scope
   run=start('cs');prepare(run,'cs');cs_scope(run,OUT/'cs',outcome)
  elif sys.argv[1]=='policy-edges':
   from extra_cases import policy_edges
   run=start('policy-edges');prepare(run,'policy-edges');policy_edges(run,OUT/'policy-edges',outcome)
  elif sys.argv[1]=='reopen':
   from extra_cases import reopen
   run=start('reopen');prepare(run,'reopen');outcome('S-16',reopen(run,OUT/'reopen',HOSTS[-1]),{'evidence':'reopen','compatible_and_incompatible':True})
 except Exception as exc:
  import traceback
  write(OUT/('failure-'+uuid.uuid4().hex[:8]+'.json'),{'exception':type(exc).__name__,'traceback':traceback.format_exc()})
  raise
 finally:
  for run,proc,log in HOSTS:
   try:snapshot(run,OUT/('retained-'+run.name))
   except Exception:pass
   try:
    if proc.poll() is None:HostControl.from_file(run/'private/service.json').stop()
   except Exception:
    if proc.poll() is None:proc.terminate()
   proc.wait(timeout=15);log.close()
