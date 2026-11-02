"""Read-only assertions over exported public evidence, not an execution test."""
import json
from pathlib import Path
from common import read,write

ROOT=Path(__file__).resolve().parent.parent
E=ROOT/'evidence'
def main():
 results=read(E/'results.json')
 race=read(E/'contention/race.json')
 assert [x['status'] for x in race].count('COMMITTED')==1
 assert [x.get('reason') for x in race].count('BUDGET_EXCEEDED')==1
 assert read(E/'contention/final/budgets.json')['G-R']['committed']=='9.00'
 results['S-05']={'status':'PASS','details':{'evidence':'contention/race.json; contention/final/budgets.json'}}
 for name,scenario,charge,spendable in [('parallel-success','S-15A','2.25','7.75'),('parallel-blocked','S-15B','1.75','7.25')]:
  dead=read(E/name/'forced-death.json');assert dead['coordinator_returncode']==-9 and dead['workers_reaped_before_proof']
  before=read(E/name/'before-proof.json');assert before['replacement']['reason']=='WORKER_NOT_QUIESCENT'
  final=read(E/name/'final/budgets.json') if name=='parallel-success' else {'G-R':read(E/name/'fresh-reader.json')['budget']}
  assert final['G-R']['committed']==charge and final['G-R']['spendable']==spendable
  run=next(p for p in (ROOT/'runtime').iterdir() if (p/'ready-R-T.json').exists() and read(p/'ready-R-T.json')['pid']==dead['workers']['R-T']['pid'])
  graph=read(run/'graph-result.json')
  assert ('__interrupt__' in graph) if scenario=='S-15B' else all(graph[k]['status']=='recorded' for k in ('trend','reversal'))
  results[scenario]={'status':'PASS','details':{'evidence':name,'graph_state':graph,'settled':charge,'spendable':spendable}}
 for p in ('compatible','restored'):
  d=read(E/'reopen'/(p+'.json'));assert d['same_budgets'] and d['same_closure']
 assert read(E/'reopen/incompatible.json')['reason']=='ARTIFACT_CHANGED'
 results['S-16']={'status':'PASS','details':{'evidence':'reopen','compatible_and_incompatible':True}}
 assert read(E/'boundary/separation-witness.json')['status']=='PASS'
 assert read(E/'boundary/separation-witness.json')['same_uid_raw_credential_readable']
 assert len(read(E/'cs/role-refusals.json'))==6
 assert all(x['response']['reason']=='UNAUTHORIZED' for x in read(E/'cs/role-refusals.json'))
 assert read(E/'cs/final/budgets.json')['AU-CK-V']['committed']=='4.50'
 assert results['CS-01']['status']==results['S-09']['status']=='FAIL'
 expected={'S-05','S-09','S-15A','S-15B','S-16','S-19','S-20','S-21',*[f'CS-{n:02}' for n in range(1,7)]}
 assert set(results)==expected
 assert sum(x['status']=='PASS' for x in results.values())==12
 write(E/'results.json',results)
 write(E/'export-verification.json',{'kind':'assertions against retained exports, not a new host run','required':14,'passed':12,'failed':2,'G_CONSUMER':'FAIL','LangGraph':'UNSELECTED','boundary':'Cooperative separation observed; same-UID credential access remains possible.'})
 print('14 mandatory dispositions reconciled: 12 PASS, 2 FAIL. G-CONSUMER FAIL.')

if __name__=='__main__':main()
