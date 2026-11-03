"""Read-only Dialog source, evidence and archived B-02 audit."""
from pathlib import Path
import json,hashlib,re
repo=Path(__file__).resolve().parents[2]
e=repo/'evidence/dialog-n1-20261103'
for row in json.loads((e/'manifest.json').read_text()):
    p=repo/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],p
    if p.suffix not in ('.png','.sqlite'):
        assert not re.search(rb'(?<![0-9a-f])[0-9a-f]{48}(?![0-9a-f])',b),p
for p in (e/'tested-source').rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:
        assert p.read_bytes()==(repo/p.relative_to(e/'tested-source')).read_bytes(),p
for row in json.loads((repo/'evidence/v01-integrated-m1-20261102/B-02-integrity.json').read_text()):
    p=repo/'docs/history/B-02'/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],p
print('Dialog tested source/evidence integrity and all 14 archived B-02 hashes pass.')
