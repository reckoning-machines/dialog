import tempfile,unittest
from decimal import Decimal
from pathlib import Path
from zugot.store import Store,Refused
from zugot.book import Book
from zugot.execution import SyntheticExecution
from zugot.fixtures import calculate,cohort,manifest
from zugot.evidence import assess

class BookContracts(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.s=Store(self.root/'book.sqlite');self.adapter=SyntheticExecution(self.root/'adapter.sqlite');self.b=Book(self.s,self.adapter);self.b.initialize();self.s.set('clock','D1 18:00')
 def tearDown(self):self.temp.cleanup()
 def strategy(self,name,status='eligible'):
  self.s.append('strategy/'+name,'STRATEGY',{'id':name,'deadline':'D1 20:00' if name.endswith('1') else 'D3 20:00','instrument':'AAA'})
  self.b.strategy_state(name,'evaluated','eval/'+name,'Unit fixture independent dossier')
  self.b.strategy_state(name,status,'admit/'+name,'Unit fixture policy decision')
 def open(self):
  self.strategy('T1');self.b.allocate('A',{'T1':200},'D1');self.b.send('A/T1/BUY',80,True)
 def test_correct_calculation_is_not_sufficient_evidence(self):
  r=calculate(cohort('T1'));self.assertFalse(assess(r,None,True)['eligible']);self.assertTrue(assess(r,manifest('T1'),True)['eligible']);self.assertFalse(assess(r,manifest('T1'),False)['eligible']);self.assertFalse(assess(r,manifest('T1'),True,True)['eligible']);self.assertFalse(assess(calculate(cohort('R1')),manifest('R1'),True)['eligible'])
  mf=manifest('T1');mf['rows'][0]['feature_available']='09:06';self.assertFalse(assess(r,mf,True)['eligible'])
 def test_fee_aware_allocation_loss_partial_fill_and_replay(self):
  self.open();self.assertEqual(self.b.state()['quantity'],0);self.assertEqual(self.b.state()['commitments'],'19919.90');self.b.reconcile('A/T1/BUY');self.assertEqual(self.b.state()['cash'],'91992.00');self.b.reconcile('A/T1/BUY');self.assertEqual(len(self.s.facts('FILL')),1);self.b.finish_order('A/T1/BUY');self.assertEqual(self.b.state()['cash'],'80080.10');self.assertEqual(self.b.state()['quantity'],199)
 def test_two_eligible_strategies_share_underlying_and_turnover(self):
  self.s.append('prior','CASH',{'amount':'-39.80'});self.strategy('T2');self.strategy('R2');a=self.b.allocate('A',{'T2':200,'R2':200},'D2');self.assertEqual(a['admitted'],{'T2':99,'R2':99});self.assertEqual(Decimal(a['denominator']),Decimal('99920.20'))
  for n in ('T2','R2'):self.b.send('A/'+n+'/BUY')
  self.assertEqual(self.b.state()['cash'],'80140.40');self.assertEqual(self.b.state()['nav'],'99940.40')
 def test_allocation_survives_death_between_batch_and_children(self):
  self.strategy('T2');self.strategy('R2');original=self.b.order
  def die(*args,**kwargs):raise RuntimeError('Injected process boundary after allocation')
  self.b.order=die
  with self.assertRaises(RuntimeError):self.b.allocate('A',{'T2':200,'R2':200},'D2')
  self.b=Book(Store(self.root/'book.sqlite'),self.adapter);self.b.allocate('A',{'T2':200,'R2':200},'D2');self.b.allocate('A',{'T2':200,'R2':200},'D2');self.assertEqual(len(self.s.facts('ALLOCATION')),1);self.assertEqual(len(self.s.facts('ORDER')),2)
 def test_required_exit_exceeds_ordinary_limit_without_resetting_cost(self):
  self.open();self.b.finish_order('A/T1/BUY');self.s.set('clock','D1 20:00');self.b.retire('T1','D1',79);self.assertEqual(self.b.state()['cash'],'87972.20');x=self.s.find('EXIT/T1')['body'];self.assertEqual(x['envelope'],'249.95');self.b=Book(Store(self.root/'book.sqlite'),self.adapter);self.b.finish_order('EXIT/T1/SELL');self.b.retire('T1','D1');self.assertEqual(self.b.state()['cash'],'99960.20');self.assertEqual(self.b.state()['ordinary_turnover']['D1'],'19900.00');self.assertEqual(self.b.state()['exit_turnover']['D1'],'19900.00');self.assertEqual(self.b.strategies()['T1']['status'],'retired')
 def test_early_retirement_stale_marks_and_stale_revision_refuse(self):
  self.open();self.b.finish_order('A/T1/BUY')
  with self.assertRaisesRegex(Refused,'HOLDING_WINDOW_NOT_ENDED'):self.b.retire('T1','D1')
  self.s.set('clock','D1 20:00');self.s.set('mark_age',31)
  with self.assertRaisesRegex(Refused,'STALE_MARK'):self.b.retire('T1','D1')
  self.assertEqual(self.b.state()['quantity'],199);self.assertEqual(self.b.strategies()['T1']['status'],'retiring');self.s.set('mark_age',0);self.strategy('T2')
  with self.assertRaisesRegex(Refused,'STALE_REVISION'):self.b.allocate('B',{'T2':200},'D2',expected=0)
 def test_pause_preserves_real_fills_and_cancels_remaining_buys(self):
  self.open();self.s.set('paused',True);self.b.finish_order('A/T1/BUY');self.assertEqual(self.b.state()['quantity'],80);self.assertEqual(self.b.state()['orders'][0]['status'],'CANCELLED');self.s.set('clock','D1 20:00');self.b.retire('T1','D1');self.assertEqual(self.b.state()['quantity'],0)
 def test_contradictory_receipt_is_not_rebooked(self):
  self.open();self.b.reconcile('A/T1/BUY');query=self.adapter.query
  def bad(oid):
   result=query(oid);result['fills'][0]['fee']='8.01';return result
  self.adapter.query=bad
  with self.assertRaisesRegex(Refused,'CONTRADICTORY_RECEIPT'):self.b.reconcile('A/T1/BUY')
  self.assertEqual(self.b.state()['cash'],'91992.00')
 def test_new_batch_refuses_existing_exposure_or_unfilled_orders(self):
  self.strategy('T1');self.b.allocate('A',{'T1':200},'D1');self.strategy('T2')
  with self.assertRaisesRegex(Refused,'OPEN_ORDER_ALLOCATION'):self.b.allocate('B',{'T2':200},'D2')
  self.b.send('A/T1/BUY')
  with self.assertRaisesRegex(Refused,'NONZERO_STARTING_TARGET'):self.b.allocate('B',{'T2':200},'D2')
 def test_authority_expiry_and_unknown_order_prevent_new_exposure(self):
  self.open();self.strategy('T2')
  with self.assertRaisesRegex(Refused,'UNKNOWN_ORDER'):self.b.allocate('B',{'T2':200},'D2')
  self.b.reconcile('A/T1/BUY');self.s.set('opening_expired',True)
  with self.assertRaisesRegex(Refused,'OPENING_AUTHORITY_EXPIRED'):self.b.allocate('B',{'T2':200},'D2')
  self.b.finish_order('A/T1/BUY');self.assertEqual(self.b.state()['quantity'],80)
if __name__=='__main__':unittest.main()
