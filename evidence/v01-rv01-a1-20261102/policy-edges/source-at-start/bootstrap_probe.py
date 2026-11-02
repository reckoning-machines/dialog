"""BC process: public profile/genesis/startup probe, redacted evidence only."""
import json
import os
import sys
import uuid
from pathlib import Path
from arh_client import Connection, Principal, Checker, Researcher, HostControl, HarnessError, event_ref, invocation
from evaluator import recompute

def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def key():return str(uuid.uuid4())
def main():
 run=Path(sys.argv[1]);out=Path(sys.argv[2]);conn=run/'state/connection.json'
 raw=json.loads(conn.read_text());out.mkdir(parents=True,exist_ok=True)
 private=run/'private';private.mkdir(mode=0o700,exist_ok=True)
 for label,actor in [('service','Principal'),('trend','R-T'),('reversal','R-R')]:
  view={k:v for k,v in raw.items() if k!='tokens'};view['tokens']={actor:raw['tokens'][actor]}
  p=private/(label+'.json');write(p,view);os.chmod(p,0o600)
 config=json.loads((Path(__file__).parent/'v01.json').read_text())
 ck_id=config['checker']
 view={k:v for k,v in raw.items() if k!='tokens'};view['tokens']={ck_id:raw['tokens'][ck_id]}
 write(private/'checker.json',view);os.chmod(private/'checker.json',0o600)
 p=Principal(Connection.from_file(private/'service.json','Principal'))
 c=p.c;profile=c.profile()
 write(out/'profile.json',profile)
 write(out/'provisioning.json',{'custodian_pid':os.getpid(),'service_actor_upstream':'Principal','test_controller_receives_principal':False,
 'views':{'service':['Principal'],'trend':['R-T'],'reversal':['R-R'],'checker':[ck_id]},
 'permissions':{n:oct((private/(n+'.json')).stat().st_mode&0o777) for n in ('service','trend','reversal','checker')},
 'assurance':'Cooperative same-user workflow; not OS isolation. Full host credential file remains privileged runtime material.'})
 designs={d['content']['AgentDesignVersionId']:d['content'] for d in profile['artifacts']['designs']}
 grants={g['content']['AuthorizationId']:g['content'] for g in profile['setup']['grants']}
 genesis=profile['experiment']['genesis']
 g=p.genesis(designs[genesis['design']],grants[genesis['grant']],key());write(out/'genesis.json',g.raw)
 tr='V01-BOOT-OBS'
 obs=next(g for g in grants.values() if g['class']=='Observation')
 proposal=p.propose_control('AUTHORIZATION',obs['AuthorizationId'],{'action':'GRANT','grant':obs,'predecessor':None},tr,key())
 write(out/'first-control-proposal.json',proposal.raw);proposal.raise_for_refusal()
 ck=Connection.from_file(private/'checker.json',ck_id)
 try:
  checked=Checker(ck,recompute=recompute).check(tr)
  helper={'status':'COMPLETED','result':checked.result,'check':checked.check.raw if checked.check else None}
 except HarnessError as exc:
  helper={'status':'BLOCKED','code':exc.code,'detail':str(exc),
   'boundary':'Public Checker.check -> checker_context; two matching declared check steps, no step selection argument',
   'no_private_evaluator_fallback':True}
 write(out/'public-checker-startup.json',helper)
 # Independent public-command probe: 0.25 cannot execute a 0.50 step.
 r=ck.call('reserve',{'grant':genesis['grant'],'amount':'0.25','purpose':{'kind':'Check','id':tr}},key()).raise_for_refusal()
 pe=c.get(proposal.ref);tool=config['check_tools']['0.50']
 data=invocation(profile,tool,'check-half',[event_ref(pe,'T')],{'transition_id':tr})
 a=ck.call('attempt',{'reservation':r.sequence,'step':'check-half','input':data,'dispatch_index':0,'maximum':'0.25','tier':1},key())
 write(out/'core-tariff-probe.json',a.raw)
 close=ck.call('close',{'reservation':r.sequence},key());write(out/'probe-reservation-close.json',close.raw)
 write(out/'budget.json',ck.budget(genesis['grant']))
 write(out/'state.json',c.state());write(out/'obligations.json',c.obligations())
 write(out/'closure.json',c.closure())
 print(json.dumps({'startup':helper['status'],'code':helper.get('code'),'tariff':a.raw.get('reason'),
 'checker_budget':ck.budget(genesis['grant'])['committed'],'evidence':str(out)}))
if __name__=='__main__':main()
