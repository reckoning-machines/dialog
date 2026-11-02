"""Retain public evidence/inventory and verify redaction; never read a ledger DB."""
import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import sys
from pathlib import Path
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1];e=root/'evidence'
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
for name in ('probe','profile-check'):
 bundle=root/'runtime'/name/'bundle'
 dest=e/'bundles'/name;dest.mkdir(parents=True,exist_ok=True)
 for p in bundle.glob('*.json'):shutil.copyfile(p,dest/p.name)
 source=dest/'tools';source.mkdir(exist_ok=True)
 for p in (bundle/'tools').glob('*.py'):shutil.copyfile(p,source/p.name)
write(e/'environment.json',{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),
 'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
 'ARH_commit':'93436406c8a1fd2c06e5713b1def09d90104db54','Murmur_authorized_commit':'58aad1a4e17e37b574e08a10a86e6e8c77ead27d',
 'source_package':'Installed from a byte-identical temporary copy of ARH client; build did not write to ARH client source.'})
arh=Path('/Users/jedgore/dev/speedway/client/arh_client');installed=Path(importlib.metadata.distribution('adaptive-research-harness-client').locate_file('arh_client'))
comparison=[]
for p in arh.glob('*.py'):
 target=installed/p.name
 comparison.append({'module':p.name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'installed_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'identical':p.read_bytes()==target.read_bytes()})
assert all(x['identical'] for x in comparison)
write(e/'client-source-comparison.json',comparison)
before=read(e/'before-reopen/state.json');after=read(e/'after-reopen/state.json')
bb=read(e/'before-reopen/budget.json');ab=read(e/'after-reopen/budget.json')
old=read(e/'before-reopen/processes.json')['processes']
def gone(pid):
 try:os.kill(pid,0);return False
 except ProcessLookupError:return True
parity={'same_state':before==after,'same_budget':bb==ab,'same_closure':read(e/'before-reopen/closure.json')==read(e/'after-reopen/closure.json'),
 'same_obligations':read(e/'before-reopen/obligations.json')==read(e/'after-reopen/obligations.json'),
 'old_processes':[{'pid':x['pid'],'gone':gone(x['pid'])} for x in old],
 'scope':'Blocked-startup reconstruction only; not S-15 parallel work or complete S-16'}
assert all(parity[x] for x in ('same_state','same_budget','same_closure','same_obligations'))
assert all(x['gone'] for x in parity['old_processes'])
write(e/'reopen-parity.json',parity)
# Exact secret comparison uses only approved connection/provisioning files, never DB.
secrets=set()
def tokens(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='tokens' and isinstance(v,dict):secrets.update(v.values())
   elif k in ('tc_auth','auth','token') and isinstance(v,str):secrets.add(v)
   else:tokens(v)
 elif isinstance(x,list):
  for v in x:tokens(v)
for run in (root/'runtime').iterdir():
 for p in [run/'state/connection.json',run/'state/fixture.json',*(run/'private').glob('*.json')]:
  if p.is_file():tokens(read(p))
scanned=0
for folder in (root/'source',e):
 for p in folder.rglob('*'):
  if p.is_file() and '__pycache__' not in str(p):
   raw=p.read_bytes();assert not any(s.encode() in raw for s in secrets),str(p);scanned+=1
write(e/'redaction-check.json',{'exact_runtime_secrets_scanned':len(secrets),'files_scanned':scanned,
 'secret_values_or_hashes_retained':False,'matches':0,
 'limitation':'No OS isolation; runtime secret files remain private outside retained evidence.'})
rows=[]
for p in sorted(e.rglob('*')):
 if p.is_file() and p.name!='evidence-manifest.json':
  b=p.read_bytes();rows.append({'path':str(p.relative_to(e)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
write(e/'evidence-manifest.json',rows)
print(json.dumps({'reopen':parity,'redaction_matches':0,'retained_files':len(rows)}))
