"""ES-M1 paper-exploratory assessment; arithmetic correctness is one criterion."""
from decimal import Decimal as D

def assess(result,manifest,arithmetic_pass,already_exposed=False):
 criteria={'independent_arithmetic':bool(arithmetic_pass),'predeclared_partition':bool(manifest and manifest.get('predeclared')),'availability_valid':bool(manifest and all(r['feature_available']<=r['decision']<r['outcome_available'] for r in manifest['rows'])),'base_positive':D(result['base_net'])>0,'stress_positive':D(result['stress_net'])>0,'drawdown_within_2_percent':D(result['drawdown'])<=D('.02'),'unexposed_partition':not already_exposed}
 return {'criteria':criteria,'eligible':all(criteria.values()),'failed':[k for k,v in criteria.items() if not v]}
