import sys,os
from pathlib import Path
from cases import clients
from common import write
p,ck,t,r=clients(sys.argv[1])
write(Path(sys.argv[2]),{'pid':os.getpid(),'state':p.state(),'budget':p.budget('G-R'),'obligations':p.obligations(),'history':p.closure()})
