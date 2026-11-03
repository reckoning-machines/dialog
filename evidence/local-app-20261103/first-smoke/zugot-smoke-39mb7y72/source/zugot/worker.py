"""Designated research/Checker process; no Principal connection is loaded."""
import os,sys,time
from arh_client import Execution,ReceiptStore,event_ref,invocation,digest
from .governance import Governance,Scoped,write
from .fixtures import calculate,QUESTIONS
from .store import Refused

def research(g,name,mode):
 actor='R-'+name[0];c=g.c(actor);r=Scoped(c,'G-R'+name[-1]);prefix='research/'+name
 if g.journal.get('result/'+name):return
 design=g.journal.get('design/'+name);refs=[design['document'],event_ref(c.get(design['record']))]
 res=g.call(c,prefix+'/reserve','reserve',{'grant':r.selected,'amount':'2.00','purpose':{'kind':'Theme','id':'TH-V-'+name[0]}})
 inp=invocation(c.profile(),'CALC-V','research',refs,{'fixture':'V01'})
 att=g.call(c,prefix+'/attempt','attempt',{'reservation':res.sequence,'step':'research','input':inp,'dispatch_index':0,'maximum':'1.00','tier':1})
 previous=att.sequence;ex=Execution.from_record(r,previous);receipts=ReceiptStore(g.root/'receipts'/actor)
 def ready(boundary):
  write(g.root/('ready-'+name+'.json'),{'pid':os.getpid(),'attempt':previous,'boundary':boundary,'run':c.info['run_id']})
  while True:time.sleep(.1)
 actual='0.75' if name[0]=='T' else '1.00'
 def compute(claim):
  if mode=='unknown':ready('claimed-no-receipt')
  return calculate(c.get(design['document'])['body']['document']['rows']),actual
 def hook(point):
  if mode=='receipt' and point=='after_receipt':ready('durable-receipt')
 result=ex.run(compute,receipts,hook=hook)
 if result['status']=='uncertain':
  g.call(c,prefix+'/unknown','settle',{'attempt':previous,'actual':'1.00','unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}})
  g.journal.set('uncertain/'+name,{'attempt':previous,'reservation':res.sequence,'charged':'1.00','status':'UNKNOWN'})
  if mode!='replace':return
  a=c.get(att.ref)['body'];payload={k:a[k] for k in ('reservation','step','input','maximum','tier')};payload['dispatch_index']=1
  retry=g.call(c,prefix+'/replacement','attempt',payload);att=retry;ex=Execution.from_record(r,retry.sequence)
  result=ex.run(lambda claim:(calculate(c.get(design['document'])['body']['document']['rows']),'0.50'),ReceiptStore(g.root/'replacement-receipts'/actor))
  if result['status']=='uncertain':raise Refused('REPLACEMENT_UNCERTAIN','Only one replacement is authorized')
 receipt=result['receipt'];suffix='/replacement' if att.sequence!=previous else ''
 body=g.journal.get(prefix+suffix+'/body') or r.record_body(att.sequence,QUESTIONS[name],receipt['result'],None,refs,parameters={'fixture':'V01'},extra={'design':design['record']})
 g.journal.set(prefix+suffix+'/body',body)
 rec=g.call(c,prefix+suffix+'/record','research-commit',body)
 g.call(c,prefix+suffix+'/settle','settle',{'attempt':att.sequence,'actual':receipt['actual'],'unit':'simulated_research_units','provenance':{'kind':'TOOL_RECEIPT','receipt':receipt}})
 g.call(c,prefix+'/close','close',{'reservation':res.sequence})
 g.journal.set('result/'+name,{'record':rec.ref.as_dict(),'attempt':att.ref.as_dict(),'result':receipt['result'],'recovered':mode not in ('normal','receipt','unknown'),'original_attempt':previous,'replacement':att.sequence!=previous,'researcher':actor})

def check(g,tr,grant,actor,amount):
 if g.journal.get('check-result/'+tr):return
 c=g.c(actor);prefix='check/'+tr;r=Scoped(c,grant);p=c.profile();prop=next(e for e in c.history('T') if e['kind']=='PROPOSED' and e['transition_id']==tr)
 tool='CHECK-V-1'+('-HALF' if amount=='0.50' else '');step='check-half' if amount=='0.50' else 'check-transition'
 reserve=g.call(c,prefix+'/reserve','reserve',{'grant':grant,'amount':amount,'purpose':{'kind':'Check','id':tr}})
 inp=invocation(p,tool,step,[event_ref(prop,'T')],{'transition_id':tr})
 att=g.call(c,prefix+'/attempt','attempt',{'reservation':reserve.sequence,'step':step,'input':inp,'dispatch_index':0,'maximum':amount,'tier':1})
 ex=Execution.from_record(r,att.sequence)
 from .spec.evaluator import evaluate
 execution=ex.run(lambda claim:(evaluate(c.closure(),tr,actor,grant,att.sequence,p),amount),ReceiptStore(g.root/'checker-receipts'/actor))
 if execution['status']=='uncertain':
  g.call(c,prefix+'/unknown','settle',{'attempt':att.sequence,'actual':amount,'unit':'simulated_research_units','provenance':{'kind':'UNKNOWN'}})
  raise Refused('CHECK_RESULT_UNCERTAIN','No permission to fabricate a check or execute again')
 receipt=execution['receipt'];out=g.call(c,prefix+'/commit','check-commit',receipt['result'])
 g.call(c,prefix+'/settle','settle',{'attempt':att.sequence,'actual':amount,'unit':'simulated_research_units','provenance':{'kind':'TOOL_RECEIPT','receipt':receipt}})
 g.call(c,prefix+'/close','close',{'reservation':reserve.sequence})
 g.journal.set('check-result/'+tr,{'check':out.ref.as_dict(),'result':receipt['result']['result'],'criteria':receipt['result']['criteria'],'actor':actor,'grant':grant,'actual':amount,'worker_pid':os.getpid()})
if __name__=='__main__':
 g=Governance(sys.argv[2])
 if sys.argv[1]=='research':research(g,sys.argv[3],sys.argv[4])
 elif sys.argv[1]=='check':check(g,*sys.argv[3:7])
