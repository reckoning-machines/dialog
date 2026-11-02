"""Supported public evaluation wrapper; no private generic criteria imports."""
from arh_client.analysis import evaluator
def recompute(inputs,spec,result):
 return result.get('sum_bp')==sum(row['return_bp'] for row in inputs.rows)
evaluate=evaluator(recompute)
