"""Experiment arithmetic with ARH's top-level exported criteria evaluator."""
from arh_client import evaluate as public_evaluate

def recompute(context):
 records=context.get('records',[])
 for rec in records:
  result=rec['body'].get('result') or {}
  if 'sum_bp' in result:
   rows=[row for d in context['documents'] for row in d['body']['document'].get('rows',[])]
   return result['sum_bp']==sum(row['return_bp'] for row in rows)
 return False

def evaluate(snapshot,transition_id,actor,grant,attempt,profile):
 return public_evaluate(snapshot,transition_id,actor,grant,attempt,profile,recompute=recompute)
