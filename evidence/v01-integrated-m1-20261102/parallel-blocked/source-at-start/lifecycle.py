"""BC public lifecycle snapshots. Contains no private ledger access."""
import json
import os
import sys
from pathlib import Path
from arh_client import Connection,HostControl
run=Path(sys.argv[1]);out=Path(sys.argv[2]);action=sys.argv[3]
out.mkdir(parents=True,exist_ok=True)
connection=run/'state/connection.json'
c=Connection.from_file(connection,'Principal');ctl=HostControl.from_file(connection)
def write(n,v):(out/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
write('state.json',c.state());write('closure.json',c.closure());write('obligations.json',c.obligations())
grant=next(k for k,g in c.state()['grants'].items() if g['class']=='Checker')
write('budget.json',c.budget(grant));write('processes.json',ctl.status())
write('reader.json',{'pid':os.getpid(),'action':action,'actor':'Principal','runtime_only_credential':True})
if action=='stop':write('stop-response.json',ctl.stop())
print(json.dumps({'action':action,'head':c.state()['N'] if action!='stop' else 'retained-before-stop','out':str(out)}))
