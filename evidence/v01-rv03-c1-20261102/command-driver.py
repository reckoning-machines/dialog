import os,subprocess,json,time,sys
from pathlib import Path
r=Path(__file__).resolve().parent;e=r/'evidence';s=r/'source';py='/private/tmp/murmur-v01.1dUJI5/venv/bin/python'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');commands=json.loads((e/'commands.json').read_text()) if (e/'commands.json').exists() else []
steps=[['orchestrate.py',m] for m in ['contention','parallel-success','parallel-blocked','cs','policy-edges']]+[['boundary_test.py'],['orchestrate.py','reopen']]
if len(sys.argv)>1:steps=[sys.argv[1:]]
for parts in steps:
 command=[py,str(s/parts[0]),*parts[1:]];name=str(len(commands)+1).zfill(2)+'-'+ '-'.join(parts).replace('.py','');start=time.time()
 print('START',name,flush=True)
 with (e/(name+'.stdout.log')).open('wb') as out,(e/(name+'.stderr.log')).open('wb') as err:
  p=subprocess.run(command,cwd=s,env=env,stdout=out,stderr=err)
 commands.append({'argv':command,'cwd':str(s),'env_overrides':{'PYTHONDONTWRITEBYTECODE':'1'},'started_unix':start,'elapsed_seconds':round(time.time()-start,3),'returncode':p.returncode,'stdout':name+'.stdout.log','stderr':name+'.stderr.log'})
 (e/'commands.json').write_text(json.dumps(commands,indent=2,sort_keys=True)+'\n')
 print('END',name,'rc',p.returncode,'seconds',round(time.time()-start,2),flush=True)
 print((e/(name+'.stdout.log')).read_text(),flush=True)
 if p.returncode:
  print((e/(name+'.stderr.log')).read_text(),flush=True);sys.exit(p.returncode)
