"""Owner-authorized W-2/DA-1 synthetic profile; no data downloads."""
import hashlib,json
from decimal import Decimal as D
COHORTS={'T1':[40,10,50],'R1':[-20,10,-10],'T2':[25,20,25],'R2':[30,25,25]}
QUESTIONS={'T1':'Do positive returns persist?','R1':'Do negative returns reverse?', 'T2':'Does trend persist across volatility conditions?', 'R2':'Does reversal work in quiet regimes?'}
MANDATE={'id':'Z-M1','name':'Two-cycle synthetic desk','universe':['AAA','BBB'],'cash':'100000.00','gross':'0.40','underlying':'0.25','strategy':'0.20','cash_floor':'0.60','ordinary_turnover':'0.20','fee_per_share':'0.10','exit_cost_fraction':'0.0025','price':'100.00','research_per_cycle':'10.00','checker_per_cycle':'2.00','setup_checker_cap':'8.00','research_lineage_combined_cap':'10.00','slots':['D1 18:00','D2 18:00'],'research_expiry':['D1 23:00','D2 23:00'],'opening_expiry':'D2 21:00','holding_deadlines':{'T1':'D1 20:00','T2':'D3 20:00','R2':'D3 20:00'},'monitor_minutes':5,'mark_stale_minutes':30,'authority':'Owner instruction: build and launch first working local synthetic app using documented mandate and bounded policies.','policy':'DA-1 / ES-M1 / C-05','evidence_class':'Historical Reconstruction','cooperative_identity':True,'forward_observations':0}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def cohort(name):
 return [{'row_id':name+'-'+str(i),'instrument':'AAA','return_bp':g*10,'quiet':True,'gross_dollars':g,'feature_available':'09:00','decision':'09:05','entry':'10:00','outcome_available':'16:00','entry_notional':'1000.00'} for i,g in enumerate(COHORTS[name])]
def manifest(name):
 rows=cohort(name)
 return {'id':'SPLIT-'+name,'partition':'V'+name[-1]+name[0],'development':'DEV','rows_sha256':digest(rows),'rows':rows,'availability_rule':'Features available 09:00 <= decision 09:05; outcomes 16:00 excluded from decision inputs. Analysis follows event day.','revision':'first-release-r1','predeclared':True,'synthetic':True,'independent_forward_support':0,'base_cost':'10.00','stress_cost':'20.00'}
def calculate(rows):
 gross=[D(str(r['return_bp']))/10 for r in rows];capital=D(1000);peak=capital;dd=D(0);path=[]
 for g in gross:
  capital+=g-10;peak=max(peak,capital);dd=max(dd,(peak-capital)/peak);path.append(str(capital))
 return {'sum_bp':sum(r['return_bp'] for r in rows),'gross':str(sum(gross)),'base_net':str(sum(gross)-10*len(rows)),'stress_net':str(sum(gross)-20*len(rows)),'drawdown':str(dd),'equity':path,'n':len(rows)}
