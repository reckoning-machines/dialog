"""Run with the pinned environment: .venv/bin/python run.py."""
import os, sys
from pathlib import Path
source = str(Path(__file__).resolve().parent / "src")
sys.path.insert(0, source)
os.environ["PYTHONPATH"] = source + (os.pathsep + os.environ["PYTHONPATH"] if os.environ.get("PYTHONPATH") else "")
from zugot.__main__ import main
if __name__ == "__main__":
    main()
