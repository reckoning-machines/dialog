"""Explicit public client work lifecycle, journal and fixed profile budget selection."""
import json,os,uuid
from pathlib import Path
from arh_client import Connection,Researcher,Execution,ReceiptStore,Outcome,event_ref,digest
from arh_client.operations import OperationStore

def key():return str(uuid.uuid4())
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 tmp=p.with_suffix(p.suffix+'.new')
 with open(tmp,'w') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
def read(p):return json.loads(Path(p).read_text())
class ScopedResearcher(Researcher):
 def grant(self):
  # Explicit application selection, not authorization: every request is core checked.
  return self.c.state()['grants'].get(getattr(self,'grant_id','G-R'))
def conn(run,label,actor):
 return Connection.from_file(Path(run)/'private'/(label+'.json'),actor)
def budget(c):return c.budget('G-R')
def work(run,actor,operation,actual='0.75',block=None,grant='G-R'):
 run=Path(run);c=conn(run,'trend' if actor=='R-T' else 'reversal',actor)
 r=ScopedResearcher(c);r.grant_id=grant;store=OperationStore(run/'journal'/actor/'operations')
 receipt_store=ReceiptStore(run/'journal'/actor/'receipts')
 entry=store.begin(operation,'call',actual=actual)
 if entry.get('replacement'):
  c.get(entry['replacement']['record'])
  return entry['replacement']
 def stage(name,fn):
  e=store.get(operation);k=e['keys'][name]
  if name in e['stages']:return Outcome.from_reply(e['stages'][name])
  prior=c.outcome(k)
  out=Outcome.from_reply(prior) if prior.get('status') in ('COMMITTED','REFUSED') else fn(k)
  store.stage(operation,name,out.raw);return out
 docs=r.documents('SRC-V-DATA');doc=docs[-1] if actor=='R-R' else docs[0];ref=event_ref(doc)
 theme='TH-V-T' if actor=='R-T' else 'TH-V-R'
 res=stage('reserve',lambda k:c.call('reserve',{'grant':grant,'amount':'2.00','purpose':{'kind':'Theme','id':theme}},k)).raise_for_refusal()
 att=stage('attempt',lambda k:r.attempt(res.sequence,'research','CALC-V',[ref],{'fixture':'V01'},'1.00',k)).raise_for_refusal()
 ex=Execution(r,att.sequence,att.raw.get('input_hash') or c.get(att.ref)['body']['input_hash'],'CALC-V','1.00')
 def call(claim):
  if block=='unknown':
   write(run/('ready-'+actor+'.json'),{'pid':os.getpid(),'attempt':att.sequence,'boundary':'claimed-no-receipt'})
   import time
   while True:time.sleep(.1)
  return {'sum_bp':sum(x['return_bp'] for x in doc['body']['document']['rows']),'n':len(doc['body']['document']['rows'])},actual
 def hook(point):
  if block=='receipt' and point=='after_receipt':
   write(run/('ready-'+actor+'.json'),{'pid':os.getpid(),'attempt':att.sequence,'boundary':'durable-local-receipt'})
   import time
   while True:time.sleep(.1)
 execution=ex.run(call,receipt_store,hook=hook)
 if execution['status']=='uncertain':
  stage('settle',lambda k:ex.settle_unknown(k)).raise_for_refusal()
  store.update(operation,status='uncertain')
  return {'status':'uncertain','attempt':att.sequence,'reservation':res.sequence}
 receipt=execution['receipt']
 body=r.record_body(att.sequence,operation,receipt['result'],None,[ref],parameters={'fixture':'V01'})
 rec=stage('record',lambda k:r.research_commit(body,k)).raise_for_refusal()
 stage('settle',lambda k:ex.settle(receipt,k)).raise_for_refusal()
 stage('close',lambda k:r.close(res.sequence,k)).raise_for_refusal()
 store.update(operation,status='recorded')
 return {'status':'recorded','attempt':att.sequence,'reservation':res.sequence,'record':rec.ref.as_dict(),'execution':execution['status']}
def replacement(run,actor,operation):
 run=Path(run);c=conn(run,'trend' if actor=='R-T' else 'reversal',actor);r=ScopedResearcher(c)
 entry=OperationStore(run/'journal'/actor/'operations').get(operation)
 previous=Outcome.from_reply(entry['stages']['attempt']).sequence
 att=r.retry(previous,key())
 if not att.ok:return {'status':'refused','reason':att.reason,'raw':att.raw}
 ex=Execution.from_record(r,att.sequence);docs=r.documents('SRC-V-DATA');ref=event_ref(docs[0])
 result={'sum_bp':sum(x['return_bp'] for x in docs[0]['body']['document']['rows']),'n':len(docs[0]['body']['document']['rows'])}
 runout=ex.run(lambda claim:(result,'0.50'),ReceiptStore(run/'journal'/actor/'replacement-receipts'))
 rec=r.research_commit(r.record_body(att.sequence,operation+' replacement',result,None,[ref],parameters={'fixture':'V01'}),key()).raise_for_refusal()
 ex.settle(runout['receipt'],key()).raise_for_refusal()
 reservation=c.get(att.ref)['body']['reservation'];r.close(reservation,key()).raise_for_refusal()
 result={'status':'recorded','attempt':att.sequence,'record':rec.ref.as_dict()}
 OperationStore(run/'journal'/actor/'operations').update(operation,replacement=result,status='recorded')
 return result
