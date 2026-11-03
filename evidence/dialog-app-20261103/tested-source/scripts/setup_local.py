"""Create the local environment and install Dialog's pinned dependencies."""
import subprocess,sys
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
if sys.version_info < (3,12):
    raise SystemExit("Python 3.12 or newer is required")
python=repo/".venv/bin/python"
if not python.exists():
    subprocess.run([sys.executable,"-m","venv",str(repo/".venv")],check=True)
subprocess.run([str(python),"-m","pip","install","-r",str(repo/"requirements.lock")],check=True)
subprocess.run([str(python),str(repo/"scripts/install_arh_client.py")],check=True)
print("Dialog is ready. Start it with .venv/bin/python run.py")
