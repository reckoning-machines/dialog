"""Experiment recomputation only; generic criteria belong to public Checker."""
def recompute(context):
 for record in context.get("records", []):
  result=record["body"].get("result") or {}
  if "sum_bp" in result:
   docs=context.get("documents", [])
   return bool(docs) and result["sum_bp"]==sum(row["return_bp"] for row in docs[-1]["body"]["document"]["rows"])
 return False
def evaluate(*args, **kwargs):
 raise RuntimeError("Use public arh_client.Checker with the recompute callback; no private generic evaluator imported.")
