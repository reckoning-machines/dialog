"""Reopen disposable runs through public APIs, reconcile a known receipt, export.

No ledger files are opened. Historical failures remain in their original exports.
"""
import os,subprocess,sys,time
from pathlib import Path
from common import read,write,key
from cases import clients,snapshot
from arh_client import Connection,HostControl,Principal

ROOT=Path(__file__).resolve().parent.parent

def reconcile(run):
 out=ROOT/'evidence'/'reconciled'/run.name
 log=open(run/'reconcile-host.log','ab')
 proc=subprocess.Popen([sys.executable,'-m','adaptive_research_harness.local_host','--setup',str(ROOT/'source'),'--run',str(run)],cwd='/Users/jedgore/dev/speedway',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log)
 try:
  end=time.monotonic()+30
  while True:
   if proc.poll() is not None:raise RuntimeError('reopen failed '+run.name)
   try:
    p=Connection.from_file(run/'state/connection.json','Principal');p.state();break
   except Exception:
    if time.monotonic()>end:raise TimeoutError(run.name)
    time.sleep(.05)
  # Host reopen changes socket/control endpoints; refresh each narrow actor view.
  raw=read(run/'state/connection.json')
  for label in ('service','checker','trend','reversal','observer'):
   path=run/'private'/(label+'.json');old=read(path)
   actors=list(old['tokens']);view={k:v for k,v in raw.items() if k!='tokens'}
   view['tokens']={actor:raw['tokens'][actor] for actor in actors};write(path,view);os.chmod(path,0o600)
  snapshot(run,out/'before')
  changes=[]
  pending=p.obligations()['pending_attempts']
  for number in pending:
   assert run.name=='cs-d2b93351' and number==50,(run.name,number)
   att=next(e for e in p.history('E') if e['seq']==number)
   claim=next(x for x in Principal(p).dispatch_status()['claims'] if x['attempt']==number)
   receipt=claim['receipt'];assert receipt['actual']=='0.50'
   ck=clients(run)[1];assert ck.actor==att['actor']
   result=ck.call_or_raise('settle',{'attempt':number,'actual':receipt['actual'],'unit':'simulated_research_units','provenance':{'kind':'TOOL_RECEIPT','receipt':receipt}},key())
   close=ck.call_or_raise('close',{'reservation':att['body']['reservation']},key())
   changes.append({'attempt':number,'settlement':result.raw,'closed':close.raw,'receipt':receipt,'reason':'Preserved failed Check commit; known charged receipt reconciled, never refunded or converted into a Check.'})
  write(out/'changes.json',changes)
  snapshot(run,out/'after')
  write(out/'host-status.json',HostControl.from_file(run/'state/connection.json').status())
  print(run.name,'exported',len(changes),'reconciliations',flush=True)
 finally:
  if proc.poll() is None:
   try:HostControl.from_file(run/'state/connection.json').stop()
   except Exception:proc.terminate()
  proc.wait(timeout=15);log.close()

if __name__=='__main__':
 for run in sorted((ROOT/'runtime').iterdir()):
  if run.is_dir() and not (ROOT/'evidence/reconciled'/run.name/'after/budgets.json').exists():reconcile(run)
