from pathlib import Path
import hashlib,json,shutil
root=Path('/private/tmp/murmur-rv01.bV2lvE');s=root/'source';e=root/'evidence'
def h(b):return hashlib.sha256(b).hexdigest()
corpus={h(p.read_bytes()):p.read_bytes() for d in (s,e/'repairs',*e.glob('*/source-at-start')) for p in d.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
text=(s/'orchestrate.py').read_text()
block=" for source in SOURCE.glob('*'):\n  if source.is_file():\n   target=OUT/name/'source-at-start'/source.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)\n"
old=text.replace(',uuid,shutil\n',',uuid\n').replace(block,'')
for variant in (old,old.replace("RESULTS=read(OUT/'results.json') if (OUT/'results.json').exists() else {}","RESULTS={}")):
 corpus[h(variant.encode())]=variant.encode()
coverage=[]
for name in ('contention','parallel-success','parallel-blocked','reopen','cs','policy-edges','boundary'):
 hashes=json.loads((e/name/'source-hashes.json').read_text());unresolved=[];resolved=[]
 for filename,digest in hashes.items():
  if digest in corpus:
   dest=e/name/'source-at-start'/filename;dest.parent.mkdir(exist_ok=True);dest.write_bytes(corpus[digest]);assert h(dest.read_bytes())==digest;resolved.append(filename)
  else:unresolved.append(filename)
 assert not any(p.endswith(('.py','.json')) for p in unresolved),(name,unresolved)
 coverage.append({'witness_family':name,'verified_source_files':resolved,'unresolved_nonexecuted_metadata':unresolved,'method':'Original start snapshot, or reconstruction from retained bytes whose SHA-256 exactly matches pre-run hash; not a new pre-run capture.'})
(e/'source-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print([(x['witness_family'],len(x['verified_source_files']),x['unresolved_nonexecuted_metadata']) for x in coverage])
