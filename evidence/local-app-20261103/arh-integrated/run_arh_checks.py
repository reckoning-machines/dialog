import hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ARH=Path('/Users/jedgore/dev/speedway')
PY='/private/tmp/murmur-v01.1dUJI5/venv/bin/python'
name=sys.argv[1];args=sys.argv[2:]
directory=ROOT/'evidence'/name;directory.mkdir(parents=True,exist_ok=True)
command=[PY,*args];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',ARH_LANGGRAPH_PYTHON=PY,ARH_RV03_EVIDENCE=str(directory/'public-host-regressions'))
start=time.monotonic()
with (directory/'output.txt').open('w') as output:
 proc=subprocess.Popen(command,cwd=ARH,env=env,stdout=output,stderr=subprocess.STDOUT)
 rc=proc.wait()
record={'command':command,'cwd':str(ARH),'environment_overrides':{k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','ARH_LANGGRAPH_PYTHON','ARH_RV03_EVIDENCE')},'returncode':rc,'elapsed_seconds':round(time.monotonic()-start,3),'process_pid':proc.pid,'core_rules_sha256':hashlib.sha256((ARH/'adaptive_research_harness/rules.py').read_bytes()).hexdigest()}
(directory/'command.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
print((directory/'output.txt').read_text()[-3500:])
sys.exit(rc)
