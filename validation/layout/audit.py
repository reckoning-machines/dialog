"""Read-only integrity audit for the application plus its visual-only successor."""
from pathlib import Path
import hashlib,json,re
repo=Path(__file__).resolve().parents[2]
baseline=repo/'evidence/dialog-app-20261103'
surface=repo/'evidence/layout-20261103'
for manifest in (baseline/'manifest.json',surface/'manifest.json'):
    for row in json.loads(manifest.read_text()):
        p=repo/row['path'];b=p.read_bytes()
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],p
        if p.suffix not in ('.png','.sqlite'):
            assert not re.search(rb'(?<![0-9a-f])[0-9a-f]{48}(?![0-9a-f])',b),p
meta=json.loads((surface/'surface.json').read_text())
for p in (baseline/'tested-source').rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.md':continue
    actual=repo/p.relative_to(baseline/'tested-source')
    if actual==repo/'src/dialog/workspace.html':
        assert hashlib.sha256(actual.read_bytes()).hexdigest()==meta['workspace_sha256']
        assert actual.read_text().split('<script>')[1]==p.read_text().split('<script>')[1]
    else:assert actual.read_bytes()==p.read_bytes(),actual
for row in json.loads((repo/'evidence/v01-integrated-m1-20261102/B-02-integrity.json').read_text()):
    p=repo/'docs/history/B-02'/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],p
print('Application source, verified layout, historical evidence and B-02 archive pass; action JavaScript is unchanged.')
