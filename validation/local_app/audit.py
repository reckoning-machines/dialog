"""Read-only local-app evidence/source integrity verification."""
import hashlib,json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[2]
evidence=repo/'evidence/local-app-20261103'
for row in json.loads((evidence/'manifest.json').read_text()):
    p=repo/row['path'];data=p.read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],p
    if p.suffix not in ('.png','.sqlite'):
        assert not re.search(rb'(?<![0-9a-f])[0-9a-f]{48}(?![0-9a-f])',data),p
for source in (evidence/'tested-source').rglob('*'):
    if source.is_file() and '__pycache__' not in source.parts:
        actual=repo/source.relative_to(evidence/'tested-source')
        assert actual.read_bytes()==source.read_bytes(),actual
print('App source matches retained tested bytes; all retained hashes/byte counts and token-format checks pass.')
