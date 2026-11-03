"""Install exact public client source, excluding stale tracked ARH build outputs.

RV-04: direct VCS wheel installation can copy stale client/build/lib modules.
This creates a clean source distribution without modifying ARH or source bytes.
"""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
repo = Path(__file__).resolve().parents[1]
pin = json.loads((repo / "arh-dependency.json").read_text())["commit"]
arh = Path(os.environ.get("DIALOG_ARH_ROOT", "/Users/jedgore/dev/speedway"))
if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=arh, text=True).strip() != pin:
    raise SystemExit("ARH checkout must match pinned commit " + pin)
paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", pin, "client/arh_client", "client/pyproject.toml", "client/README.md"], cwd=arh, text=True).splitlines()
with tempfile.TemporaryDirectory(prefix="dialog-client-source-") as temporary:
    source = Path(temporary)
    hashes = {}
    for path in paths:
        data = subprocess.check_output(["git", "show", pin + ":" + path], cwd=arh)
        destination = source / Path(path).relative_to("client")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        hashes[str(destination.relative_to(source))] = hashlib.sha256(data).hexdigest()
    subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps", "--no-cache-dir", str(source)], check=True)
    code = "import arh_client,json,hashlib;from pathlib import Path;p=Path(arh_client.__file__).parent;print(json.dumps({str(Path('arh_client')/f.name):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.glob('*.py')}))"
    installed = json.loads(subprocess.check_output([sys.executable, "-c", code], text=True))
    expected = {k: v for k, v in hashes.items() if k.startswith("arh_client/") and k.endswith(".py")}
    if installed != expected:
        raise SystemExit("Public client source/installation mismatch")
    report = repo / ".local" / "client-install.json"
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps({"ARH_commit": pin, "source_sha256": hashes, "all_modules_byte_identical": True, "finding": "RV-04"}, indent=2) + "\n")
    print("Installed exact public client bytes from " + pin)
