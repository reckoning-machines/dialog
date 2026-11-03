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
 body=public_evaluate(snapshot,transition_id,actor,grant,attempt,profile,recompute=recompute)
 proposal=next(x for x in snapshot['transitions'] if x['kind']=='PROPOSED' and x['transition_id']==transition_id)
 if proposal['body']['class']=='HYPOTHESIS':
  refs=(proposal['body']['content'].get('motivation_closure') or {}).get('refs',[])
  evidence={(e['seq'],e['sha256']) for e in snapshot['evidence']}
  if any((r.get('sequence'),r.get('sha256')) not in evidence for r in refs):
   # Actual unavailable immutable input: the scientific check cannot be calculated.
   # This reports uncertainty, never manufactures a passing criterion.
   body['criteria']['recomputation'].update(status='NOT DETERMINABLE',reason='Exact proposed formation input is absent/mismatched in the authoritative snapshot; arithmetic cannot be independently determined.')
   body['result']='STOP'
 return body
