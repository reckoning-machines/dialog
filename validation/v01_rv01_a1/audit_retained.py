"""Inspect finalized artifacts without runtime credentials, sockets or ARH DBs."""
import hashlib,json,re,sys
from pathlib import Path

SOURCE=Path(__file__).resolve().parent
EVIDENCE=(SOURCE.parent/'evidence') if SOURCE.name=='source' else (SOURCE.parents[1]/'evidence/v01-rv01-a1-20261102')
def main():
 sensitive={'tokens','tc_auth','auth','token','Authorization','api_key','secret'}
 def visit(v):
  if isinstance(v,dict):
   for k,x in v.items():
    assert not (k in sensitive and x),'Credential field present'
    visit(x)
  elif isinstance(v,list):
   for x in v:visit(x)
 count=0
 for folder,manifest in ((SOURCE,'source-manifest.json'),(EVIDENCE,'evidence-manifest.json')):
  rows=[]
  for p in sorted(folder.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts or p==folder/manifest:continue
   b=p.read_bytes()
   assert not re.search(rb'(?<![0-9a-f])[0-9a-f]{48}(?![0-9a-f])',b),'Host token format present'
   if p.suffix=='.json':visit(json.loads(b))
   rows.append({'path':str(p.relative_to(folder)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
  target=folder/manifest
  if '--refresh' in sys.argv:target.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
  assert json.loads(target.read_text())==rows,'Manifest mismatch '+str(target)
  count+=len(rows)
 print(f'{count} source/evidence file hashes and byte counts verified; structural credential/token-format audit passed.')

if __name__=='__main__':main()
