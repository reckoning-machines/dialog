import sys,os
from pathlib import Path
from arh_client import Connection,Principal
from common import read,write,key
p=Principal(Connection.from_file(sys.argv[1],'Principal'));r=read(sys.argv[2])
d=p.policy_decide(r['transition'],r['check'],r['key']).raise_for_refusal()
a=p.apply(r['transition'],d.sequence,key=key()).raise_for_refusal()
write(Path(sys.argv[3]),{'pid':os.getpid(),'actor':'Principal','separate_from_TC':True,'decision':d.raw,'apply':a.raw,'narrow_credential_enforcement':False})
