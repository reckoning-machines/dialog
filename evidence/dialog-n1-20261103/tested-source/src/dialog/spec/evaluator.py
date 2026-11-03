"""Independent arithmetic, using ARH's exported full-criteria evaluator."""
from decimal import Decimal
from arh_client import evaluate as public_evaluate

def recompute(context):
 docs=context.get('documents',[])
 rows=[r for d in docs for r in d['body']['document'].get('rows',[])]
 for rec in context.get('records',[]):
  result=rec['body'].get('result') or {}
  if 'sum_bp' not in result:continue
  if result['sum_bp']!=sum(r['return_bp'] for r in rows):return False
  if 'base_net' in result:
   outcomes=[Decimal(r['return_bp'])/10 for r in rows]
   balance=Decimal(1000);peak=balance;drawdown=Decimal(0)
   for x in outcomes:
    balance+=x-10;peak=max(peak,balance);drawdown=max(drawdown,(peak-balance)/peak)
   return Decimal(result['base_net'])==sum(outcomes)-10*len(rows) and Decimal(result['stress_net'])==sum(outcomes)-20*len(rows) and Decimal(result['drawdown'])==drawdown
  return True
 return False

def evaluate(snapshot,transition_id,actor,grant,attempt,profile):
 return public_evaluate(snapshot,transition_id,actor,grant,attempt,profile,recompute=recompute)
