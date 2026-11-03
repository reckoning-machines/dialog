"""One coordinator graph with two simultaneously running designated-identity processes."""
import os,subprocess,sys,time
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from common import write,work,read

class State(TypedDict,total=False):
 trend:dict
 reversal:dict

def coordinate(run,blocking):
 run=Path(run)
 def node(actor):
  def execute(state):
   marker='receipt' if actor=='R-T' else 'unknown'
   args=[sys.executable,__file__,'worker',str(run),actor,marker if blocking else 'none']
   child=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=open(run/(actor+'-stderr.log'),'ab'))
   write(run/('worker-'+actor+'.json'),{'pid':child.pid})
   child.wait()
   if child.returncode:
    write(run/('reaped-'+actor+'.json'),{'pid':child.pid,'returncode':child.returncode,'coordinator_pid':os.getpid()})
    while True:time.sleep(.1)
   result=read(run/('result-'+actor+'.json'))
   if result['status']=='uncertain':
    from langgraph.types import interrupt
    interrupt({'actor':actor,'operation':actor+'-parallel','requires':'authoritative quiescence/replacement','status':'blocked'})
   return {'trend' if actor=='R-T' else 'reversal':result}
  return execute
 graph=StateGraph(State);graph.add_node('trend',node('R-T'));graph.add_node('reversal',node('R-R'))
 graph.add_edge(START,'trend');graph.add_edge(START,'reversal');graph.add_edge('trend',END);graph.add_edge('reversal',END)
 with SqliteSaver.from_conn_string(str(run/'graph-checkpoints.sqlite')) as saver:
  app=graph.compile(checkpointer=saver)
  config={'configurable':{'thread_id':'parallel-V01'}}
  value={} if blocking else None
  if not blocking and any(task.interrupts for task in app.get_state(config).tasks):
   from langgraph.types import Command
   value=Command(resume=True)
  result=app.invoke(value,config=config)
  import json
  write(run/'graph-result.json',json.loads(json.dumps(result,default=str)))
if __name__=='__main__':
 mode,run=sys.argv[1:3]
 if mode=='worker':
  actor,block=sys.argv[3:5];write(Path(run)/('result-'+actor+'.json'),work(run,actor,actor+'-parallel',actual='0.75' if actor=='R-T' else '1.00',block=None if block=='none' else block))
 else:coordinate(run,mode=='block')
