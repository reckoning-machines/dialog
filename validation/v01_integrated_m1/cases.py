import copy,json,os,time,uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from arh_client import Connection,Principal,Observer,HostControl,Execution,ReceiptStore,event_ref,digest,HarnessError
from arh_client.operations import OperationStore
from common import *
from startup import check

def clients(run):
 meta=read(Path(run)/'bundle/v01.json') if (Path(run)/'bundle/v01.json').exists() else read(Path(__file__).parent/'v01.json')
 return (conn(run,'service','Principal'),conn(run,'checker',meta['checker']),conn(run,'trend','R-T'),conn(run,'reversal','R-R'))
def fence_bootstrap(run):
 p,ck,t,r=clients(run);return Principal(p).fence('G-BR','Bootstrap reservations complete; measured work uses explicit G-R.',key()).raise_for_refusal()
def snapshot(run,out):
 p,ck,t,r=clients(run)
 write(Path(out)/'closure.json',p.closure());write(Path(out)/'state.json',p.state());write(Path(out)/'obligations.json',p.obligations())
 write(Path(out)/'budgets.json',{g:p.budget(g) for g in ('G-BR','G-R','AU-CK-V')})
def prefix(c,name,actual='0.50'):
 r=ScopedResearcher(c);doc=r.documents('SRC-V-DATA')[0];ref=event_ref(doc);theme='TH-V-T' if c.actor=='R-T' else 'TH-V-R'
 res=c.call_or_raise('reserve',{'grant':'G-R','amount':'1.00','purpose':{'kind':'Theme','id':theme}},key())
 att=r.attempt(res.sequence,'research','CALC-V',[ref],{'fixture':'V01'},'1.00',key()).raise_for_refusal()
 ex=Execution(r,att.sequence,att.input_hash,'CALC-V','1.00')
 result={'sum_bp':sum(x['return_bp'] for x in doc['body']['document']['rows']),'n':len(doc['body']['document']['rows'])}
 exout=ex.run(lambda claim:(result,actual),ReceiptStore(Path(c.info['state']).parent/'prefix-receipts'/c.actor))
 rr=r.research_commit(r.record_body(att.sequence,name,result,None,[ref],parameters={'fixture':'V01'}),key()).raise_for_refusal()
 ex.settle(exout['receipt'],key()).raise_for_refusal();r.close(res.sequence,key()).raise_for_refusal()
 return rr.ref
def hypothesis(c,label,method=1,bad=False,missing=False):
 r=ScopedResearcher(c);p=c.profile();root='TH-V-T' if c.actor=='R-T' else 'TH-V-R'
 docs=r.documents('SRC-V-DATA');doc=docs[0];ref=event_ref(doc)
 # Real unmetered evidence/selection fixture cites committed bytes, not a manufactured Check.
 records=[e for e in c.history('E') if e['kind']=='RESEARCH_RECORD' and e['actor']==c.actor and e['body'].get('kind')=='plain' and e['body'].get('attempt')]
 if not records:raise RuntimeError('A hypothesis needs a completed metered Research result')
 rec=records[-1];doc=c.get(rec['body']['reproducibility']['input_refs'][0]);ref=event_ref(doc);content=copy.deepcopy(p['artifacts']['hypothesis_template']['content'])
 content.update(HypothesisId='H-'+label,HypothesisLineageId='HL-'+label,predecessor=None,motivated_by=[root],
 motivation_closure={'N':c.state()['N'],'refs':[ref,event_ref(rec)]},
 resolution_period={'start':'2026-10-30T00:00:00.000Z','end':'2026-10-31T00:00:00.000Z'},
 initial_method={'id':f'METHOD-H{method}','sha256':p['artifacts']['methods'][f'METHOD-H{method}']['content_sha256']},
 selection_basis=copy.deepcopy(p['setup']['theme']['content']['selection_basis']))
 content['resolution_set']=[{'SourceId':'SRC-V-DATA','period':content['resolution_period'],'print':'FIRST_RELEASE'}]
 if bad:content['tolerance']='1'  # Real proposed criterion failure, independently evaluated.
 if missing:content['motivation_closure']['refs'][0]=dict(ref,sha256='0'*64)
 future=r.next_evidence_sequence();tr='P-'+label
 pr=r.propose('HYPOTHESIS',content['HypothesisId'],content,'0.25',future,key(),transition_id=tr).raise_for_refusal()
 funding=c.call_or_raise('reserve',{'grant':'G-R','amount':'0.25','purpose':{'kind':'Transition','id':tr},'expected_sequence':future},key())
 return tr,funding,content
def run_smoke(run,out):
 p,ck,t,r=clients(run);fence_bootstrap(run)
 record=work(run,'R-T','first-actual','0.75')
 tr,funding,content=hypothesis(t,'smoke',1)
 body,cr=check(ck,tr)
 write(Path(out)/'hypothesis-check.json',body)
 assert body['result']=='PASS',[(k,v['status']) for k,v in body['criteria'].items() if v['status']!='MET']
 d=Principal(p).policy_decide(tr,cr.sequence,key()).raise_for_refusal()
 a=Principal(p).apply(tr,d.sequence,key=key()).raise_for_refusal()
 write(Path(out)/'policy.json',d.raw);write(Path(out)/'apply.json',a.raw);snapshot(run,out)
 return {'record':record,'check':body['result'],'applied':a.raw}
if __name__=='__main__':
 import sys
 write(Path(sys.argv[2])/'smoke-result.json',run_smoke(sys.argv[1],sys.argv[2]))
