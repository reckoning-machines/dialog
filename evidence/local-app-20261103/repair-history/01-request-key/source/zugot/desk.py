"""Finite, recoverable Historical Reconstruction coordinated by LangGraph."""
import json,os,subprocess,sys,time,signal
from pathlib import Path
from decimal import Decimal as D
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from arh_client import HostControl,event_ref
from .governance import Governance,read,write
from .store import Store,Refused
from .fixtures import MANDATE,QUESTIONS,manifest,digest
from .book import Book,cash
from .execution import SyntheticExecution
STEPS=['Open desk','Competing research','Independent checks and admission','Shared allocation','Order response lost','Recover original partial fill','Complete opening fill','Scheduled exit begins','Recover exit remainder','Close first research cycle','Parallel research interrupted','Recover both researchers','Evaluate revised strategies','Allocate overlapping requests','Fill shared paper portfolio','Close second research cycle','Opening authority expires','Scheduled final exits']
class ResearchState(TypedDict,total=False):
 T:dict
 R:dict
class StepState(TypedDict,total=False):
 requested:int
 completed:int
class Desk:
 def __init__(self,root):
  self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True);self.s=Store(self.root/'desk.sqlite');self.adapter=SyntheticExecution(self.root/'adapter.sqlite');self.book=Book(self.s,self.adapter);self.g=Governance(self.root);self.error=None
 def start(self):
  self.g.start();self.g.bootstrap();self.book.initialize()
  if self.s.get('step') is None:
   self.s.set('step',0);self.s.set('clock','D1 18:00');self.g.tick(1,18)
   self.s.append('opened','DESK_OPENED',{'mandate':'Z-M1','research_grants':['G-R1','G-R2'],'checker_grants':['G-C1','G-C2'],'historical_reconstruction':True,'future_slot_withheld':True},'scheduler')
  self.g.export();return self
 def checkpoint(self):return int(self.s.get('step',0))
 def parallel(self,cycle):
  for prefix in ('T','R'):self.g.design(prefix+str(cycle))
  def run(prefix):
   def node(state):
    name=prefix+str(cycle);p=self.g.worker(name);rc=p.wait(timeout=45)
    if rc:raise Refused('RESEARCH_WORKER_FAILED',{'actor':prefix,'log':'worker-'+name+'.log'})
    return {prefix:self.g.journal.get('result/'+name)}
   return node
  graph=StateGraph(ResearchState);graph.add_node('trend',run('T'));graph.add_node('reversal',run('R'));graph.add_edge(START,'trend');graph.add_edge(START,'reversal');graph.add_edge('trend',END);graph.add_edge('reversal',END)
  with SqliteSaver.from_conn_string(str(self.root/'research-checkpoints.sqlite')) as saver:graph.compile(checkpointer=saver).invoke({},config={'configurable':{'thread_id':'cycle-'+str(cycle)}})
  for prefix in ('T','R'):
   name=prefix+str(cycle);self.s.append('research/'+name,'RESEARCH_RESULT',dict(name=name,question=QUESTIONS[name],parent=(prefix+'1' if cycle==2 else None),**self.g.journal.get('result/'+name)),'R-'+prefix)
 def evaluate(self,name):
  if self.s.find('admission/'+name):return
  refs=self.g.register(name);result=self.g.journal.get('result/'+name)['result'];design=self.g.journal.get('design/'+name)
  c=self.g.c('Principal');checked=c.get(refs['check']);applied=c.get(refs['applied']);actual_design=c.get(design['record'])
  if checked['kind']!='CHECK' or checked['body']['result']!='PASS' or applied['kind']!='APPLIED':raise Refused('INCOMPLETE_ARH_ADMISSION')
  mf=actual_design['body']['result']['manifest']
  if mf['rows_sha256']!=digest(c.get(design['document'])['body']['document']['rows']):raise Refused('PROVENANCE_MISMATCH')
  if name=='T1':self.s.append('missing-partition/T1','REFUSAL',{'code':'MISSING_PRECOMMITTED_SPLIT','reason':'Arithmetic PASS is insufficient without the original partition. Recovered exact precommitted ARH design; no new split written.','resolved_by':design['record']},'strategy-boundary')
  self.book.opening_permitted()
  self.s.append('candidate/'+name,'STRATEGY',{'id':name,'label':'Trend' if name[0]=='T' else 'Quiet reversal' if name=='R2' else 'Reversal','question':QUESTIONS[name],'parent':name[0]+'1' if name[-1]=='2' else None,'method':'MV-'+name,'instrument':'AAA','requested_quantity':200,'deadline':MANDATE['holding_deadlines'].get(name,'D1 20:00'),'evidence_class':'Historical Reconstruction','forward_observations':0},'research-plan')
  criteria={'independent_arithmetic':True,'predeclared_partition':mf['predeclared'],'exact_input':True,'availability_valid':all(r['feature_available']<=r['decision']<r['outcome_available'] for r in mf['rows']),'base_positive':D(result['base_net'])>0,'stress_positive':D(result['stress_net'])>0,'drawdown_within_2_percent':D(result['drawdown'])<=D('.02'),'unexposed_partition':not any(x['body']['partition']==mf['partition'] for x in self.s.facts('COHORT_EXPOSED'))}
  dossier={'strategy':name,'standard':'ES-M1','result':result,'criteria':criteria,'independent_check':refs,'partition':mf['partition'],'design':design['record'],'researcher': 'R-'+name[0],'reviewer':'AD-CK-D1.0','no_forward_support':True}
  self.s.append('dossier/'+name,'DOSSIER',dossier,'domain-evaluator');self.book.strategy_state(name,'evaluated','evaluated/'+name,'Independent arithmetic and complete dossier assessed')
  failed=[k for k,v in criteria.items() if not v];status='rejected' if failed else 'eligible'
  self.book.strategy_state(name,status,'admission/'+name,'Failed '+', '.join(failed) if failed else 'DA-S admits bounded paper-exploratory use; no alpha qualification')
  self.s.append('exposed/'+name,'COHORT_EXPOSED',{'partition':mf['partition'],'shared_with':['R-T','R-R'],'never_untouched_again':True},'data-intake')
 def research_interrupt(self):
  if self.s.find('parallel-interrupted'):return
  for name in ('T2','R2'):self.g.design(name)
  processes={name:self.g.worker(name,'receipt' if name=='T2' else 'unknown') for name in ('T2','R2')}
  ready={}
  for name,p in processes.items():
   path=self.root/('ready-'+name+'.json')
   for _ in range(600):
    if path.exists():break
    if p.poll() is not None:raise Refused('INTERRUPTION_FIXTURE_FAILED',name)
    time.sleep(.025)
   else:raise Refused('INTERRUPTION_TIMEOUT',name)
   ready[name]=read(path)
  for p in processes.values():p.kill()
  for p in processes.values():p.wait(timeout=10)
  self.s.append('parallel-interrupted','INTERRUPTION',{'workers':ready,'returncodes':{k:p.returncode for k,p in processes.items()},'reason':'Both research workers terminated: trend has durable receipt; reversal claim has no receipt. Maximum liabilities remain authoritative in ARH.','recovery':'Resolve original attempts, settle unknown maximum; require host proof before one replacement.'},'operator')
 def research_recover(self):
  data=self.s.find('parallel-interrupted')['body']
  for name in ('T2','R2'):
   p=self.g.worker(name);rc=p.wait(timeout=45)
   if rc:raise Refused('RESEARCH_RECOVERY_FAILED',name)
  if not self.g.journal.get('result/R2'):
   from .governance import Scoped
   c=self.g.c('R-R');r=Scoped(c,'G-R2');old=self.g.journal.get('uncertain/R2')['attempt']
   if not self.s.find('replacement-refusal'):
    refusal=r.retry(old,'before-proof-R2');
    if refusal.reason!='WORKER_NOT_QUIESCENT':raise Refused('EXPECTED_QUIESCENCE_REFUSAL',refusal.raw)
    self.s.append('replacement-refusal','REFUSAL',{'code':refusal.reason,'upstream':refusal.raw,'reason':'No replacement until original workers cannot act'},'operator')
   for name,worker in data['workers'].items():
    if not self.s.find('proof/'+name):
     proof=HostControl.from_file(self.g.run/'private/Principal.json').quiesce({'pid':worker['pid'],'run':worker['run']})
     self.s.append('proof/'+name,'QUIESCENCE',proof,'trusted-control-service')
   p=self.g.worker('R2','replace');rc=p.wait(timeout=45)
   if rc:raise Refused('REPLACEMENT_FAILED','worker-R2.log')
  for name in ('T2','R2'):
   self.s.append('research/'+name,'RESEARCH_RESULT',dict(name=name,question=QUESTIONS[name],parent=name[0]+'1',**self.g.journal.get('result/'+name)),'R-'+name[0])
  self.s.append('research-recovered','RECOVERY',{'reason':'Trend receipt reused; reversal UNKNOWN 1.00 retained; one new 0.50 replacement after host proof','charged':'2.25','pending':'0.00'},'operator')
 def do_step(self,n):
  if self.s.find('step/'+str(n)):self.s.set('step',n);return
  if n!=self.checkpoint()+1:raise Refused('OUT_OF_ORDER_STEP')
  self.g.c('Principal').state() # Graph state is never authorization.
  if n in (1,2,3,10,11,12,13):self.book.opening_permitted()
  if n==1:self.parallel(1)
  elif n==2:
   self.evaluate('T1');self.evaluate('R1')
  elif n==3:self.book.allocate('AL-1',{'T1':200,'R1':200},'D1')
  elif n==4:self.book.send('AL-1/T1/BUY',80,True)
  elif n==5:self.book.reconcile('AL-1/T1/BUY')
  elif n==6:self.book.finish_order('AL-1/T1/BUY')
  elif n==7:
   self.s.set('clock','D1 20:00');self.g.tick(1,20);self.book.retire('T1','D1',79)
  elif n==8:
   self.book.finish_order('EXIT/T1/SELL');self.book.retire('T1','D1')
  elif n in (9,15):
   cycle=1 if n==9 else 2;state=self.book.state();feedback={'fees':state['fees'],'paper_pnl':state['pnl'],'book_revision':self.s.revision(),'source':'ZUGOT accepted fills; execution costs are not alpha'}
   for actor in ('R-T','R-R'):
    ref=self.g.selection(actor,cycle,feedback);self.s.append('selection/'+actor+str(cycle),'SELECTION',{'actor':actor,'cycle':cycle,'next_question':QUESTIONS[actor[-1]+'2'] if cycle==1 else 'No third research slot authorized; monitor current holdings','reference':ref,'parent_results':[x['body']['record'] for x in self.s.facts('RESEARCH_RESULT') if x['body']['name'].endswith(str(cycle))]},'research-plan')
   if self.g.c('Principal').obligations()['pending_attempts']:raise Refused('UNRESOLVED_RESEARCH_LIABILITY')
   self.s.append('closed/'+str(cycle),'CYCLE_CLOSED',{'cycle':cycle,'local_dispatch_stopped':True,'research_expiry':'D'+str(cycle)+' 23:00','no_fence_or_refill':True},'scheduler')
  elif n==10:
   self.s.set('clock','D2 18:00');self.g.tick(2,18);self.s.set('opening-nav/D2',self.book.state()['nav']);self.research_interrupt()
  elif n==11:self.research_recover()
  elif n==12:
   self.evaluate('T2');self.evaluate('R2')
  elif n==13:self.book.allocate('AL-2',{'T2':200,'R2':200},'D2')
  elif n==14:
   for name in ('T2','R2'):self.book.send('AL-2/'+name+'/BUY');self.book.finish_order('AL-2/'+name+'/BUY')
  elif n==16:
   self.s.set('clock','D2 21:00');self.g.tick(2,21);self.s.set('opening_expired',True)
   self.s.append('opening-expired','AUTHORITY_EXPIRED',{'opening':True,'exit_only_preserved':True,'reason':'Research schedules do not define holding periods'},'scheduler')
  elif n==17:
   self.s.set('clock','D3 20:00');self.g.tick(3,20)
   for name in ('T2','R2'):self.book.retire(name,'D3')
  else:raise Refused('NO_AUTHORIZED_SLOT')
  self.g.export();self.s.append('step/'+str(n),'STEP',{'step':n,'label':STEPS[n],'virtual_time':self.s.get('clock'),'authority':'Z-M1 / DA-1'},'scheduler');self.s.set('step',n)
 def advance(self,expected=None):
  if expected is not None and expected!=self.s.revision():raise Refused('STALE_REVISION')
  n=self.checkpoint()+1
  if n>=len(STEPS):raise Refused('DEMO_COMPLETE')
  graph=StateGraph(StepState)
  def execute(state):self.do_step(state['requested']);return {'completed':state['requested']}
  graph.add_node('authorized_step',execute);graph.add_edge(START,'authorized_step');graph.add_edge('authorized_step',END)
  with SqliteSaver.from_conn_string(str(self.root/'desk-checkpoints.sqlite')) as saver:graph.compile(checkpointer=saver).invoke({'requested':n},config={'configurable':{'thread_id':'desk'}})
  self.error=None;return self.snapshot()
 def snapshot(self,refresh=False):
  if refresh:
   try:self.g.export();self.error=None
   except Exception as ex:self.error=str(ex)
  public=self.g.journal.get('public-export',{});now=time.time();asof=public.get('observed_at',0)
  return {'name':'ZUGOT','step':self.checkpoint(),'stage':STEPS[self.checkpoint()],'next':STEPS[self.checkpoint()+1] if self.checkpoint()+1<len(STEPS) else None,'clock':self.s.get('clock'),'revision':self.s.revision(),'book':self.book.state(),'strategies':self.book.strategies(),'research':[x['body'] for x in self.s.facts('RESEARCH_RESULT')],'dossiers':[x['body'] for x in self.s.facts('DOSSIER')],'selections':[x['body'] for x in self.s.facts('SELECTION')],'allocations':[x['body'] for x in self.s.facts('ALLOCATION')],'exits':[x['body'] for x in self.s.facts('EXIT')],'changes':self.s.facts()[-24:],'budgets':public.get('budgets',{}),'obligations':public.get('obligations',{}),'mandate':self.book.mandate,'arh':{'run':public.get('run'),'pin':public.get('pin'),'E':public.get('closure',{}).get('E'),'N':public.get('closure',{}).get('N'),'asof':asof,'stale':now-asof>30,'unavailable':self.error is not None},'paused':self.s.get('paused',False),'opening_expired':self.s.get('opening_expired',False),'error':self.error,'decisions':[{'code':'DESK_BLOCKED','reason':self.error,'action':'Recover authoritative source; no permission bypass'}] if self.error else []}
