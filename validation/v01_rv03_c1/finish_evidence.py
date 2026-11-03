"""Retain public exports, consumer journals/checkpoints and integrity metadata.

Reads connection/provisioning files only for redaction. Never reads ARH ledgers.
"""
import hashlib,importlib.metadata,json,os,platform,re,shutil,subprocess,sys
from decimal import Decimal as D
from pathlib import Path
from common import read,write

ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'evidence';S=ROOT/'source'
ARH=Path('/Users/jedgore/dev/speedway');REPO=Path('/Users/jedgore/dev/murmuration')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def money(n):return f'{n:.2f}'
def cmd(*parts):return subprocess.check_output(parts,text=True).strip()

def export():
 rows=[]
 for run in sorted((ROOT/'runtime').iterdir()):
  final=E/'reconciled'/run.name/'after'
  assert final.exists(),run.name
  budgets=read(final/'budgets.json');closure=read(final/'closure.json');obligations=read(final/'obligations.json')
  pending=obligations['pending_attempts'];assert not pending,(run.name,pending)
  assert all(not b['overspent'] for b in budgets.values())
  assert D(budgets['G-BR']['reserved'])<=10 and D(budgets['G-R']['reserved'])<=10 and D(budgets['AU-CK-V']['reserved'])<=12
  attempts={e['seq']:e for e in closure['evidence'] if e['kind']=='ATTEMPT'}
  settled={actor:D(0) for actor in ('R-T','R-R')}
  for e in closure['evidence']:
   if e['kind']=='SETTLEMENT':
    a=attempts[e['body']['attempt']]
    if a['body']['grant'] in ('G-BR','G-R'):settled[a['actor']]+=D(e['body']['actual'])
  row={'run':run.name,'checker_settled':budgets['AU-CK-V']['committed'],'bootstrap_research_settled':budgets['G-BR']['committed'],
   'measured_research_settled':budgets['G-R']['committed'],'measured_usage':budgets['G-R']['reserved'],
   'measured_unsettled_allowance':money(D(budgets['G-R']['reserved'])-D(budgets['G-R']['committed'])),
   'measured_spendable':budgets['G-R']['spendable'],'research_settled_by_actor_across_grants':{k:money(v) for k,v in settled.items()},
   'pending_attempts':pending,'decided_unapplied':obligations['decided_unapplied'],
   'export':'reconciled/'+run.name+'/after'}
  rows.append(row)
  dest=E/'bundles'/run.name;dest.mkdir(parents=True,exist_ok=True)
  for p in (run/'bundle').glob('*.json'):shutil.copyfile(p,dest/p.name)
  for p in (run/'bundle/tools').glob('*.py'):
   (dest/'tools').mkdir(exist_ok=True);shutil.copyfile(p,dest/'tools'/p.name)
  consumer=E/'consumer-state'/run.name
  for name in ('journal','prefix-receipts'):
   for p in (run/name).rglob('*.json'):
    target=consumer/name/p.relative_to(run/name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
  for name in ('graph-checkpoints.sqlite','graph-result.json','ready-R-T.json','ready-R-R.json','reaped-R-T.json','reaped-R-R.json','result-R-T.json','result-R-R.json'):
   if (run/name).is_file():
    consumer.mkdir(parents=True,exist_ok=True);shutil.copyfile(run/name,consumer/name)
 totals={k:money(sum((D(r[k]) for r in rows),D(0))) for k in ('checker_settled','bootstrap_research_settled','measured_research_settled','measured_unsettled_allowance')}
 write(E/'accounting.json',{'unit':'simulated_research_units','runs':rows,'successor_totals':totals,
  'prior_RV01_A1':{'settled':'112.75','checker_settled':'47.50','bootstrap_research_settled':'31.50','measured_research_settled':'33.75','retained_allowances':'5.25','not_reused':True},
  'predecessor_at_ccf31b4':{'checker_settled':'1.25','research_settled':'0.00','not_reused':True},
  'notice':'Independent disposable run ceilings are not a single replenishable pool. Unsettled allowance includes deliberately blocked recovery and retained funding, not unpaid charges. Public budget.reserved means usage including settled charges.'})
 env={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
 'ARH_commit':cmd('git','-C',str(ARH),'rev-parse','HEAD'),'ARH_tracked_diff':cmd('git','-C',str(ARH),'diff','--stat'),
 'Murmur_parent_commit':cmd('git','-C',str(REPO),'rev-parse','HEAD'),'phase':'RV-03-C1 synthetic consumer validation'}
 assert env['ARH_commit']==read(S/'dependency-pin.json')['ARH_commit'] and env['ARH_tracked_diff']==''
 write(E/'environment.json',env)
 package=importlib.metadata.distribution('adaptive-research-harness-client');installed=Path(package.locate_file('arh_client'))
 compare=[{'module':p.name,'source_sha256':sha(p),'installed_sha256':sha(installed/p.name),'identical':p.read_bytes()==(installed/p.name).read_bytes()} for p in (ARH/'client/arh_client').glob('*.py')]
 assert all(x['identical'] for x in compare);write(E/'client-source-comparison.json',compare)
 baseline=[]
 for line in (REPO/'docs/baseline-manifest.md').read_text().splitlines():
  m=re.match(r'\| \[([^]]+)\]\([^)]*\) \| (\d+) \| ([0-9a-f]{64}) \|',line)
  if m:
   path,n,h=m.groups();p=REPO/path;assert p.stat().st_size==int(n) and sha(p)==h
   baseline.append({'path':path,'bytes':int(n),'sha256':h,'matches':True})
 assert len(baseline)==14;write(E/'B-02-integrity.json',baseline)
 write(E/'ARH-source-pins.json',{str(p.relative_to(ARH)):sha(p) for p in (ARH/'adaptive_research_harness/rules.py',ARH/'adaptive_research_harness/experiment.py',ARH/'client/arh_client/checking.py')})
 print(json.dumps({'runs':len(rows),'totals':totals,'baseline_files':len(baseline)}))

def redact_and_manifest():
 secrets=set();secretfiles=[]
 def tokens(v):
  if isinstance(v,dict):
   for k,x in v.items():
    if k=='tokens' and isinstance(x,dict):secrets.update(s for s in x.values() if isinstance(s,str))
    elif k in ('tc_auth','token','auth') and isinstance(x,str):secrets.add(x)
    else:tokens(x)
  elif isinstance(v,list):
   for x in v:tokens(x)
 for run in (ROOT/'runtime').iterdir():
  for p in [run/'state/connection.json',run/'state/fixture.json',*(run/'private').glob('*.json')]:
   if p.is_file():tokens(read(p));secretfiles.append(p)
 assert secrets,'No redaction secrets found; refuse to pretend scan ran.'
 scanned=0
 for directory in (S,E):
  for p in directory.rglob('*'):
   if p.is_file() and '__pycache__' not in p.parts:
    b=p.read_bytes();assert not any(x.encode() in b for x in secrets),p;scanned+=1
 # Ensure all retained known worker/coordinator/core/service process IDs are gone.
 pids=set()
 def collect(v):
  if isinstance(v,dict):
   for k,x in v.items():
    if k in ('pid','service_pid','coordinator_pid','worker_pid','new_pid','old_pid','tc_pid','bc_pid','bootstrap_pid') and isinstance(x,int):pids.add(x)
    else:collect(x)
  elif isinstance(v,list):
   for x in v:collect(x)
 for p in E.rglob('*.json'):
  if p.name not in ('source-manifest.json','evidence-manifest.json'):
   try:collect(read(p))
   except (ValueError,UnicodeDecodeError):pass
 status=[]
 for pid in sorted(pids):
  try:os.kill(pid,0);gone=False
  except ProcessLookupError:gone=True
  if not gone:
   state=subprocess.run(['ps','-p',str(pid),'-o','stat='],capture_output=True,text=True).stdout.strip()
   # A reaped/exited historical PID can be reused. Retain the ambiguity, no kill.
   status.append({'pid':pid,'gone':False,'current_stat':state,'identity_unestablished':True})
  else:status.append({'pid':pid,'gone':True})
 write(E/'process-disposition.json',{'retained_known_processes':status,'notice':'A currently allocated historical PID is not presumed to be the original process. Forced-death witnesses retain wait returncodes and host proofs.'})
 write(E/'redaction-check.json',{'exact_secret_values_compared':len(secrets),'files_scanned':scanned,'matches':0,'token_values_or_token_hashes_retained':False,'scheme':'No HTTP headers, secret config or connection files exported. Byte comparison against currently available provisioned secrets includes consumer checkpoints. Earlier rotated secrets are not retained; separate structural and token-format audit covers every retained file.','runtime_credentials_deleted':True})
 for p in secretfiles:p.unlink()
 source_rows=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(S.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='source-manifest.json']
 write(S/'source-manifest.json',source_rows)
 rows=[{'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(E.rglob('*')) if p.is_file() and p.name!='evidence-manifest.json']
 write(E/'evidence-manifest.json',rows)
 print(json.dumps({'redaction_matches':0,'source_files':len(source_rows),'evidence_files':len(rows),'credential_files_deleted':len(secretfiles),'ambiguous_live_pids':sum(not x['gone'] for x in status)}))

if __name__=='__main__':
 if sys.argv[1]=='export':export()
 elif sys.argv[1]=='finalize':redact_and_manifest()
