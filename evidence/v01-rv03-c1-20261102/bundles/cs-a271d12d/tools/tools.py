"""Deterministic synthetic tool; no provider and no core imports."""
def calculate(document, parameters, claim=None):
 return {'sum_bp':sum(row['return_bp'] for row in document['rows']), 'n':len(document['rows'])}
def researcher(*args,**kwargs):
 raise RuntimeError('Use the explicit consumer runner with its designated identity.')
