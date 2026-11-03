"""External V-01 setup data. Imports only ARH's supported client."""
import copy
import json
from pathlib import Path
from arh_client.project import Project
from arh_client import digest

THEMES = {
 'TH-V-T': 'Research price-return continuation on synthetic AAA/BBB at the declared toy-trade horizon, including predeclared volatility cohorts DEV/V1/V2, unchanged feature availability, cost and validation rules; stop after the two named research slots.',
 'TH-V-R': 'Research recovery after negative price returns on synthetic AAA/BBB at the same declared horizon, including the predeclared quiet-regime filter and DEV/V1/V2 cohorts, unchanged feature availability, cost and validation rules; stop after the two named research slots.',
}
def read(p): return json.loads(Path(p).read_text())
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def build(directory):
 d=Path(directory);d.mkdir(parents=True,exist_ok=True)
 formation={'class':'synthetic','synthetic':True,'item_id':'v-2026-10-28-charter',
 'period_start':'2026-10-28T00:00:00.000Z','period_end':'2026-10-29T00:00:00.000Z',
 'claimed_publication_time':'2026-10-29T00:00:00.000Z',
 'rows':[{'row_id':'AAA-DEV','return_bp':30,'quiet':True,'instrument':'AAA'},
 {'row_id':'BBB-DEV','return_bp':-10,'quiet':False,'instrument':'BBB'}]}
 project={'experiment_id':'MURMUR-V01','short':'V','question':'Bounded continuation/reversal research on synthetic AAA/BBB.',
 'sources':[{'id':'SRC-V-DATA','prefix':'v-','class':'synthetic','description':'Immutable synthetic AAA/BBB DEV/V1/V2 inputs.'}],
 'analyses':[{'id':'CALC-V','kind':'v01-calculation','module':'tools.py','callable':'calculate',
 'execution':'caller','provider_work':'ends_with_caller','step':'research',
 'parameters':{'fixture':'V01'},'tariff':{'measure':'documents','limit':1,'per_unit':'1.00'},
 'inputs':[{'kind':'OBSERVATION','form':'DOCUMENT','min':1,'max':1},{'kind':'RESEARCH_RECORD','record_kind':'EXPERIMENT DESIGN','min':0,'max':1}],
 'description':'Sum synthetic returns over the exact committed rows; no provider.',
 'cost':'Maximum1.00; caller receipts report fixed fixture actual costs.'}],
 'researcher':{'program':'tools.py','entrypoint':'tools:researcher'},
 'evaluator':{'module':'evaluator.py','entrypoint':'evaluator:evaluate','description':'Public independent full criteria evaluator, with exact sum recomputation.'},
 'budget':'12.00','theme':THEMES['TH-V-T'],'formation':formation}
 Project(d, project).write_setup()
 s=read(d/'setup.json');a=read(d/'designs_and_methods.json');e=read(d/'experiment.json')
 # Adapt inspectable public setup files; never modify ARH or its ledgers.
 research=next(x for x in a['designs'] if x['content']['method_class']=='RESEARCH')
 research['content']['AgentDesignVersionId']='R-T';research['content']['AgentDesignLineageId']='L-T'
 research['content']['scope_profile']='TH-V-T'
 research['content']['instructions']='Research only within declared original Theme and grant; record all revisions; never check or approve.'
 other=copy.deepcopy(research);other['content'].update(AgentDesignVersionId='R-R',AgentDesignLineageId='L-R',scope_profile='TH-V-R')
 other['content']['instructions']='Investigate negative-return reversal and predeclared quiet regimes on AAA/BBB, record failures/revisions, never check or admit.'
 a['designs'].append(other)
 ck=next(x['content'] for x in a['designs'] if x['content']['method_class']=='CHECKER')
 ck_id=ck['AgentDesignVersionId']
 # Two public check steps support the two exact B-02 tariffs; lower-level
 # public Connection/invocation/evaluate, not checker_context's one-step helper.
 check_tool=next(t for t in a['tools'] if t.startswith('CHECK'))
 second=check_tool+'-HALF'
 a['tools'][second]=copy.deepcopy(a['tools'][check_tool])
 a['tools'][second]['content']['cost']='0.50 units per full funded check.'
 a['tools'][second]['content_sha256']=digest(a['tools'][second]['content'])
 ck['tool_specs'][second]=a['tools'][second]['content_sha256']
 e['tools'][second]=dict(e['tools'][check_tool],label='check-half')
 e['steps'].append({'name':'check-half','kind':'check','tools':[second],'maximum':'0.50'})
 gck=next(x['content'] for x in s['grants'] if x['content']['class']=='Checker')
 gck.update(research_budget_units='12.00',per_lineage_cap_units='12.00')
 gck['tools'].append({'id':second,'tier':1,'spec_sha256':a['tools'][second]['content_sha256']})
 gr=next(x['content'] for x in s['grants'] if x['content']['class']=='Research')
 gr.update(AuthorizationId='G-BR',grantee=['R-T','R-R'],research_budget_units='10.00',per_lineage_cap_units='10.00')
 gr['scope_by_grantee']={'R-T':{'themes':['TH-V-T'],'empirical_search_families':[]},
 'R-R':{'themes':['TH-V-R'],'empirical_search_families':[]}}
 gr['may_propose'].insert(0,'Hypothesis registration')
 gr['discovery_scope']['fixed_subgrant_units']='10.00'
 measured=copy.deepcopy(gr);measured['AuthorizationId']='G-R'
 s['grants'].append({'content':measured})
 # All setup/grant control data stays inspectable and is checked at startup.
 s['ordinary_researcher']='R-T'
 s['theme']['content'].update(ThemeId='TH-V-T',statement=THEMES['TH-V-T'])
 s['theme']['content']['selection_basis'].update(
  uncertainty='Robustness within predeclared volatility/quiet cohorts.',
  horizon='Two named research slots',stopping_rule='Both slots complete or authority/budget/required evidence unavailable.',
  cost_estimate_units='10.00',time_estimate_ms='UNESTIMATED',origin='discovery-scope initiative')
 for h in range(1,9):
  method={'version':h,'scoring':'exact binary synthetic positive-return fraction','effective_observations':'one fixed synthetic cohort','predictive_check':f'predeclared fixture calibration grid {h}; zero forward support claimed'}
  a['methods'][f'METHOD-H{h}']={'content':method,'content_sha256':digest(method)}
 rule={'version':1,'algorithm':'Target1 iff the first-release declared synthetic cohort has positive-return fraction at least1/2; missing member unresolved.','input_fields':['return_bp'],'missing_member':'UNRESOLVED'}
 template={'template_id':'V01-H','statement':'In the next declared synthetic AAA/BBB cohort, at least half the returns are positive.',
 'observable':'Binary positive-return fraction on the declared synthetic cohort','falsifier':'A resolved positive-return fraction below1/2 contradicts this prediction; no standing from reconstruction.',
 'horizon':'One declared synthetic cohort','stopping_rule':'Stop at the two approved research slots; no inherited forward standing.',
 'tolerance':'0','resolution_rule':rule,'resolution_rule_sha256':digest(rule),'resolution_source':'SRC-V-DATA','print':'FIRST_RELEASE'}
 a['hypothesis_template']={'content':template,'content_sha256':digest(template)}
 obs=next(g['content'] for g in s['grants'] if g['content']['class']=='Observation')
 declaration=obs['source_declarations'][0]['content'];declaration.update(extraction_rule='Exact fraction of positive return_bp over row_id cohort.',field='positive_return_fraction',unit='exact numerator/denominator')
 obs['source_declarations'][0]['SourceRevision']=digest(declaration)
 for design in a['designs']:design['content_sha256']=digest(design['content'])
 s['theme']['content_sha256']=digest(s['theme']['content'])
 write(d/'project.json',project);write(d/'setup.json',s);write(d/'designs_and_methods.json',a);write(d/'experiment.json',e)
 write(d/'v01.json',{'themes':THEMES,'checker':ck_id,'check_grant':gck['AuthorizationId'],
 'check_tools':{'0.25':check_tool,'0.50':second},'researchers':['R-T','R-R']})
 return d
if __name__=='__main__':
 import sys
 build(sys.argv[1])
