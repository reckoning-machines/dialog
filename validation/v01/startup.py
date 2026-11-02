"""External BC startup via public Connection commands and public evaluator wrapper."""
import copy
import json
import os
import sys
import uuid
from pathlib import Path
from arh_client import Connection, Principal, Observer, HostControl, digest, event_ref, invocation, historical_document
from evaluator import evaluate

def key():return str(uuid.uuid4())
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def check(c,tr,amount='0.25'):
 profile=c.profile();s=c.state()
 grant=next(k for k,g in s['grants'].items() if g['class']=='Checker' and c.actor in g['grantee'])
 tool=next(x['id'] for x in s['grants'][grant]['tools'] if x['id'].endswith('-HALF')== (amount=='0.50'))
 step='check-half' if amount=='0.50' else 'check-transition'
 prop=next(e for e in c.history('T') if e['kind']=='PROPOSED' and e['transition_id']==tr)
 r=c.call_or_raise('reserve',{'grant':grant,'amount':amount,'purpose':{'kind':'Check','id':tr}},key())
 data=invocation(profile,tool,step,[event_ref(prop,'T')],{'transition_id':tr})
 a=c.call_or_raise('attempt',{'reservation':r.sequence,'step':step,'input':data,'dispatch_index':0,'maximum':amount,'tier':1},key())
 permission=c.query('tool-run',{'attempt':a.sequence})
 if permission.get('status')!='PERMISSION_CONSUMED':raise RuntimeError('No fresh permission')
 body=evaluate(c.closure(),tr,c.actor,grant,a.sequence,profile)
 receipt={'attempt':a.sequence,'input_hash':digest(data),'tool_id':tool,'actual':amount,'synthetic':True,'result':body,'error':None}
 c.query('tool-finish',{'attempt':a.sequence,'receipt':receipt})
 committed=c.call_or_raise('check-commit',body,key())
 c.call_or_raise('settle',{'attempt':a.sequence,'actual':amount,'unit':'simulated_research_units','provenance':{'kind':'TOOL_RECEIPT','receipt':receipt}},key())
 c.call_or_raise('close',{'reservation':r.sequence},key())
 return body,committed
def main():
 run=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 raw=json.loads((run/'state/connection.json').read_text());meta=json.loads((Path(__file__).parent/'v01.json').read_text())
 private=run/'private';private.mkdir(mode=0o700,exist_ok=True)
 for label,actor in [('service','Principal'),('checker',meta['checker']),('trend','R-T'),('reversal','R-R'),('observer','Observation function')]:
  view={k:v for k,v in raw.items() if k!='tokens'};view['tokens']={actor:raw['tokens'][actor]}
  write(private/(label+'.json'),view);os.chmod(private/(label+'.json'),0o600)
 p=Principal(Connection.from_file(private/'service.json','Principal'));c=p.c
 ck=Connection.from_file(private/'checker.json',meta['checker'])
 profile=c.profile();write(out/'profile.json',profile)
 designs={d['content']['AgentDesignVersionId']:d['content'] for d in profile['artifacts']['designs']}
 grants={g['content']['AuthorizationId']:g['content'] for g in profile['setup']['grants']}
 gen=profile['experiment']['genesis']
 
 if c.state()['N'] is None:p.genesis(designs[gen['design']],grants[gen['grant']],key()).raise_for_refusal()
 seq=0;log=[]
 def control(cls,subject,content):
  nonlocal seq
  seq+=1;tr=f'BOOT-{seq}'
  if any(x['kind']=='APPLIED' and x['transition_id']==tr for x in c.history('T')):
   log.append({'transition':tr,'subject':subject,'status':'RECOVERED_APPLIED'});return True
  pr=p.propose_control(cls,subject,content,tr,key()).raise_for_refusal()
  body,cr=check(ck,tr)
  write(out/(tr+'-check.json'),body)
  log.append({'transition':tr,'class':cls,'subject':subject,'result':body['result']})
  if body['result']!='PASS':
   write(out/'blocked.json',{'transition':tr,'subject':subject,'criteria':{k:v for k,v in body['criteria'].items() if v['status']!='MET'},
    'standing':'STOPPED_DEPENDENT_STARTUP','no_profile_or_upstream_change':True})
   return False
  decision=p.decide(tr,cr.sequence,key=key()).raise_for_refusal()
  p.apply(tr,decision.sequence,key=key()).raise_for_refusal()
  return True
 try:
  obs=next(g for g in grants.values() if g['class']=='Observation')
  if not control('AUTHORIZATION',obs['AuthorizationId'],{'action':'GRANT','grant':obs,'predecessor':None}):return
  HostControl.from_file(private/'service.json').tick(1000)
  observer=Observer(Connection.from_file(private/'observer.json','Observation function'))
  raw_data=json.dumps({'rows':profile['artifacts']['formation_cohort']['content']['rows']},sort_keys=True).encode()
  (out/'formation-input.json').write_bytes(raw_data)
  doc=historical_document(raw_data,'formation-input.json','V-01 synthetic generator')
  doc.update({'class':'synthetic','synthetic':True})
  formation=observer.observe('SRC-V-DATA',doc,'2026-10-28').raise_for_refusal()
  if not control('LIMITS','initial_limits',profile['setup']['initial_limits']):return
  for ident in ('R-T','R-R'):
   if not control('AGENT_DESIGN',ident,designs[ident]):return
  for ident in ('G-BR','G-R'):
   if not control('AUTHORIZATION',ident,{'action':'GRANT','grant':grants[ident],'predecessor':None}):return
  for ident,statement in meta['themes'].items():
   theme=copy.deepcopy(profile['setup']['theme']['content'])
   theme.update(ThemeId=ident,statement=statement,motivation_closure={'N':c.state()['N'],'refs':[formation.ref.as_dict()]})
   if not control('THEME',ident,theme):return
 finally:
  write(out/'startup-controls.json',log);write(out/'state.json',c.state());write(out/'closure.json',c.closure())
  write(out/'budget.json',c.budget(gen['grant']));write(out/'obligations.json',c.obligations())
  print(json.dumps({'controls':log,'budget':c.budget(gen['grant'])['committed'],'evidence':str(out)}))
if __name__=='__main__':main()
