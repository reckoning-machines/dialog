"""Public ARH consumer. Credentials stay in actor-specific local files.

The bootstrap custodian alone provisions controls. Runtime Principal ingress is
limited to P-1/Apply and host control; it is cooperative, not a scoped token.
"""
import copy,json,os,signal,subprocess,sys,time,uuid
from pathlib import Path
from decimal import Decimal as D
from arh_client import Connection,Principal,Observer,HostControl,Researcher,Execution,ReceiptStore,event_ref,digest,invocation,historical_document
from .store import Store,Refused
from .fixtures import cohort,manifest,QUESTIONS,calculate
ARH=Path(os.environ.get('ZUGOT_ARH_ROOT','/Users/jedgore/dev/speedway'))
PIN='76234ff1816d95432a87de69b3337db5401349d4'
CHECKER='AD-CK-D1.0'
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.new')
 fd=os.open(tmp,os.O_CREAT|os.O_WRONLY|os.O_TRUNC,0o600)
 with os.fdopen(fd,'w') as f:json.dump(v,f,sort_keys=True,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
class Scoped(Researcher):
 def __init__(self,c,grant):super().__init__(c);self.selected=grant
 def grant(self):return self.c.state()['grants'][self.selected]
class Governance:
 def __init__(self,root):self.root=Path(root);self.run=self.root/'arh';self.setup=self.root/'setup';self.journal=Store(self.root/'governance-journal.sqlite');self.proc=None
 def c(self,actor):return Connection.from_file(self.run/'private'/(actor+'.json'),actor)
 def call(self,c,key,op,payload):return self.journal.call(c,key,op,payload)
 def prepare(self):
  if (self.setup/'v01.json').exists():return
  import shutil
  shutil.copytree(Path(__file__).parent/'spec',self.setup,ignore=shutil.ignore_patterns('__pycache__'))
  s=read(self.setup/'setup.json');a=read(self.setup/'designs_and_methods.json');e=read(self.setup/'experiment.json')
  g=next(x['content'] for x in s['grants'] if x['content']['class']=='Checker');g['research_budget_units']=g['per_lineage_cap_units']='8.00'
  ck=copy.deepcopy(next(x for x in a['designs'] if x['content']['method_class']=='CHECKER'))
  ck['content'].update(AgentDesignVersionId=CHECKER,AgentDesignLineageId='AD-CK-D1');ck['content_sha256']=digest(ck['content']);a['designs'].append(ck)
  for day in (1,2):
   gc=copy.deepcopy(g);gc.update(AuthorizationId='G-C'+str(day),grantee=[CHECKER],research_budget_units='2.00',per_lineage_cap_units='2.00',expiry=f'2026-10-{28+day}T23:00:00.000Z',forbidden_subjects=['AD-CK-D1 lineage and every successor','G-C1 and G-C2'])
   s['grants'].append({'content':gc})
  for item in s['grants']:
   g=item['content']
   if g['AuthorizationId'] in ('G-BR','G-R'):
    day=1 if g['AuthorizationId']=='G-BR' else 2;g.update(AuthorizationId='G-R'+str(day),expiry=f'2026-10-{28+day}T23:00:00.000Z')
  for name,value in [('setup.json',s),('designs_and_methods.json',a),('experiment.json',e)]:write(self.setup/name,value)
 def start(self):
  actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ARH,text=True).strip()
  if actual!=PIN:raise Refused('DEPENDENCY_PIN_MISMATCH',actual)
  self.prepare();self.run.mkdir(parents=True,exist_ok=True)
  try:
   c=Connection.from_file(self.run/'state/connection.json','Principal');c.state()
  except Exception:
   log=open(self.root/'arh-host.log','ab');self.proc=subprocess.Popen([sys.executable,'-m','adaptive_research_harness.local_host','--setup',str(self.setup),'--run',str(self.run)],cwd=ARH,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log,start_new_session=True);log.close()
   for _ in range(600):
    if self.proc.poll() is not None:raise Refused('ARH_START_FAILED','Inspect local arh-host.log')
    try:c=Connection.from_file(self.run/'state/connection.json','Principal');c.state();break
    except Exception:time.sleep(.05)
   else:raise Refused('ARH_UNAVAILABLE')
  raw=read(self.run/'state/connection.json');private=self.run/'private';private.mkdir(exist_ok=True,mode=0o700)
  for actor in raw['tokens']:
   view={k:v for k,v in raw.items() if k!='tokens'};view['tokens']={actor:raw['tokens'][actor]};write(private/(actor+'.json'),view)
  return self
 def bootstrap(self):
  c=self.c('Principal');p=c.profile();designs={x['content']['AgentDesignVersionId']:x['content'] for x in p['artifacts']['designs']};grants={x['content']['AuthorizationId']:x['content'] for x in p['setup']['grants']}
  if c.state()['N'] is None:self.call(c,'boot/genesis','genesis',{'constitution_sha256':p['setup']['constitution']['sha256'],'design':designs['AD-CK-V1.0'],'grant':grants['AU-CK-V']})
  def control(cls,subject,content):
   tr='BOOT-'+subject
   if any(x['kind']=='APPLIED' and x['transition_id']==tr for x in c.history('T')):return
   key='boot/'+subject
   stored=self.journal.get(key+'/payload')
   if stored is None:
    stored={'transition_id':tr,'base':c.state()['N'],'class':cls,'subject':subject,'content':content,'grant':None,'budget':'0.00','funding_ref':None,'delta':{'O':0,'S':0,'A':0}};self.journal.set(key+'/payload',stored)
   self.call(c,key+'/propose','propose',stored)
   ck=self.check_process(tr,'AU-CK-V','AD-CK-V1.0','0.25')
   if ck['result']!='PASS':raise Refused('BOOTSTRAP_CHECK_FAILED',ck)
   dec=self.call(c,key+'/decision','decide',{'transition_id':tr,'check':ck['check']['sequence'],'decision':'ADMITTED','reason':'Owner-authorized local synthetic startup'})
   self.call(c,key+'/apply','apply',{'transition_id':tr,'decision':dec.sequence})
  g=grants['AU-OBS-V'];control('AUTHORIZATION','AU-OBS-V',{'action':'GRANT','grant':g,'predecessor':None})
  if not self.journal.get('formation'):
   HostControl.from_file(self.run/'private/Principal.json').tick(1000)
   self.journal.set('formation',self.observe('DEV',[{'row_id':'DEV','return_bp':30,'quiet':True,'instrument':'AAA'}]))
  control('LIMITS','initial_limits',p['setup']['initial_limits'])
  for actor in ('R-T','R-R',CHECKER):control('AGENT_DESIGN',actor,designs[actor])
  for name in ('G-R1','G-R2','G-C1','G-C2'):control('AUTHORIZATION',name,{'action':'GRANT','grant':grants[name],'predecessor':None})
  for name,statement in read(self.setup/'v01.json')['themes'].items():
   theme=copy.deepcopy(p['setup']['theme']['content']);theme.update(ThemeId=name,statement=statement,motivation_closure={'N':c.state()['N'],'refs':[self.journal.get('formation')]});control('THEME',name,theme)
  self.export()
 def observe(self,name,rows):
  old=self.journal.get('observation/'+name)
  if old:return old
  raw=json.dumps(rows,sort_keys=True).encode();doc=historical_document(raw,name+'.json','ZUGOT deterministic synthetic fixture');doc.update({'class':'synthetic','synthetic':True})
  c=self.c('Observation function')
  # Recover a committed exact source document before invoking the convenience importer again.
  existing=[e for e in c.history('E') if e['kind']=='OBSERVATION' and e['body'].get('document',{}).get('file',{}).get('sha256')==doc['file']['sha256']]
  ref=event_ref(existing[0]) if existing else event_ref(c.get(Observer(c).observe('SRC-V-DATA',doc,'2026-10-28').ref))
  self.journal.set('observation/'+name,ref);return ref
 def design(self,name):
  old=self.journal.get('design/'+name)
  if old:return old
  ref=self.observe(name,cohort(name));actor='R-'+name[0];r=Scoped(self.c(actor),'G-R'+name[-1]);mf=manifest(name)
  body=r.record_body(None,QUESTIONS[name],{'manifest':mf,'expectation':'Net > 0 under base and doubled cost; drawdown <= 2%; no forward standing.'},None,[ref],kind='EXPERIMENT DESIGN',parameters={'theme':'TH-V-'+name[0]},tool={'id':'CALC-V','planned':True})
  # The body is persisted because a new public closure is not the old command payload.
  saved=self.journal.get('design-body/'+name) or body;self.journal.set('design-body/'+name,saved)
  out=self.call(r.c,'design/'+name,'research-commit',saved);v={'record':out.ref.as_dict(),'document':ref,'manifest':mf};self.journal.set('design/'+name,v);return v
 def worker(self,name,mode='normal'):
  log=open(self.root/('worker-'+name+'.log'),'ab')
  p=subprocess.Popen([sys.executable,'-m','zugot.worker','research',str(self.root),name,mode],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log);log.close();return p
 def check_process(self,tr,grant,actor=CHECKER,amount='0.50'):
  p=subprocess.run([sys.executable,'-m','zugot.worker','check',str(self.root),tr,grant,actor,amount],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  if p.returncode:raise Refused('CHECKER_WORKER_FAILED',p.stderr[-2500:])
  return self.journal.get('check-result/'+tr)
 def register(self,name):
  c=self.c('R-'+name[0]);r=Scoped(c,'G-R'+name[-1]);tr='P-'+name;prefix='hyp/'+name
  if self.journal.get(prefix+'/done'):return self.journal.get(prefix+'/done')
  research=self.journal.get('result/'+name);record=c.get(research['record']);docref=self.journal.get('design/'+name)['document'];profile=c.profile()
  saved=self.journal.get(prefix+'/payload')
  if saved is None:
   content=copy.deepcopy(profile['artifacts']['hypothesis_template']['content']);content.update(HypothesisId='H-'+name,HypothesisLineageId='HL-'+name,predecessor=None,motivated_by=['TH-V-'+name[0]],motivation_closure={'N':c.state()['N'],'refs':[docref,event_ref(record)]},resolution_period={'start':'2026-10-31T00:00:00.000Z','end':'2026-11-01T00:00:00.000Z'},initial_method={'id':'METHOD-H'+str(['T1','R1','T2','R2'].index(name)+1),'sha256':profile['artifacts']['methods']['METHOD-H'+str(['T1','R1','T2','R2'].index(name)+1)]['content_sha256']},selection_basis=copy.deepcopy(profile['setup']['theme']['content']['selection_basis']))
   content['resolution_set']=[{'SourceId':'SRC-V-DATA','period':content['resolution_period'],'print':'FIRST_RELEASE'}]
   saved={'transition_id':tr,'base':c.state()['N'],'class':'HYPOTHESIS','subject':'H-'+name,'content':content,'budget':'0.25','grant':'G-R'+name[-1],'funding_ref':r.next_evidence_sequence(),'delta':{'O':0,'S':0,'A':0}};self.journal.set(prefix+'/payload',saved)
  self.call(c,prefix+'/propose','propose',saved)
  fund=self.call(c,prefix+'/fund','reserve',{'grant':'G-R'+name[-1],'amount':'0.25','purpose':{'kind':'Transition','id':tr},'expected_sequence':saved['funding_ref']})
  checked=self.check_process(tr,'G-C'+name[-1])
  if checked['result']!='PASS':raise Refused('INDEPENDENT_CHECK_NOT_PASS',checked)
  # Trusted service entry: only current P-1 plus Apply; no discretionary decision.
  p=self.c('Principal');dec=self.call(p,prefix+'/policy','policy-decide',{'transition_id':tr,'check':checked['check']['sequence']})
  applied=self.call(p,prefix+'/apply','apply',{'transition_id':tr,'decision':dec.sequence})
  result={'run':p.info['run_id'],'research':research['record'],'check':checked['check'],'decision':dec.ref.as_dict(),'applied':applied.ref.as_dict(),'funding':fund.ref.as_dict(),'arithmetic':checked['result']}
  self.journal.set(prefix+'/done',result);return result
 def selection(self,actor,cycle,feedback):
  name=actor[-1]+str(cycle);r=Scoped(self.c(actor),'G-R'+str(cycle));key='selection/'+name
  old=self.journal.get(key)
  if old:return old
  refs=[self.journal.get('result/'+x+str(cycle))['record'] for x in ('T','R')]
  refs=[event_ref(r.c.get(x)) for x in refs]
  result={'next_question':QUESTIONS.get(actor[-1]+'2','No third slot authorized'),'shared_history':refs,'paper_feedback':feedback,'rejected_variant':'Repeat V1 as untouched evidence','reason':'Reversal failed costs; trend needs volatility robustness. Retained executions and fees are operational feedback, not alpha.','future_slot_authorized':cycle==1}
  body=self.journal.get(key+'/body') or r.record_body(None,'Choose subsequent investigation from shared evidence',result,None,refs,kind='SELECTION',parameters={'theme':'TH-V-'+actor[-1]},tool={'id':'CALC-V','planned':True});self.journal.set(key+'/body',body)
  out=self.call(r.c,key,'research-commit',body);self.journal.set(key,out.ref.as_dict());return out.ref.as_dict()
 def tick(self,day,hour):
  from datetime import datetime,timezone
  target=int(datetime(2026,10,28+day,hour,tzinfo=timezone.utc).timestamp()*1000);c=self.c('Principal');now=c.clock()['t']
  if target>now:HostControl.from_file(self.run/'private/Principal.json').tick(target-now)
 def export(self):
  c=self.c('Principal');v={'closure':c.closure(),'state':c.state(),'budgets':{g:c.budget(g) for g in ('AU-CK-V','G-R1','G-R2','G-C1','G-C2') if g in c.state()['grants']},'obligations':c.obligations(),'observed_at':time.time(),'run':c.info['run_id'],'pin':PIN}
  self.journal.set('public-export',v);return v
 def stop(self):
  try:HostControl.from_file(self.run/'private/Principal.json').stop()
  except Exception:pass
  if self.proc:self.proc.wait(timeout=15)
