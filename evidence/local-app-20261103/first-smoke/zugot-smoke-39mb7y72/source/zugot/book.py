"""Murmur-owned portfolio, allocations, strategy eligibility and bounded exits."""
from decimal import Decimal as D,ROUND_FLOOR
from .fixtures import MANDATE,digest
from .store import Refused
from .execution import LostResponse

def cash(x):return f'{D(x):.2f}'
class Book:
 def __init__(self,store,adapter):self.s=store;self.adapter=adapter
 @property
 def mandate(self):return self.s.facts('MANDATE')[0]['body']
 def initialize(self):
  self.s.append('mandate','MANDATE',MANDATE,'owner')
  self.s.append('opening','CASH',{'amount':'100000.00','reason':'Synthetic paper opening capital'},'owner')
 def positions(self):
  p={}
  for f in self.s.facts('FILL'):
   b=f['body'];p[b['strategy']]=p.get(b['strategy'],0)+b['quantity']*(1 if b['side']=='BUY' else -1)
  return p
 def state(self):
  cash_balance=sum(D(x['body']['amount']) for x in self.s.facts('CASH'));fees=D(0);ordinary={};exit_turn={};positions=self.positions()
  fills=self.s.facts('FILL')
  for f in fills:
   b=f['body'];notional=D(b['price'])*b['quantity'];fee=D(b['fee']);cash_balance+=(-notional-fee if b['side']=='BUY' else notional-fee);fees+=fee
   target=exit_turn if b['exit'] else ordinary;target[b['day']]=target.get(b['day'],D(0))+notional
  orders=[];commitment=D(0)
  for r in self.s.facts('ORDER'):
   b=r['body'];filled=sum(x['body']['quantity'] for x in fills if x['body']['order']==b['id']);cancelled=self.s.find('cancel/'+b['id']);unknown=self.s.get('unknown/'+b['id'],False)
   remaining=0 if cancelled else b['quantity']-filled
   if b['side']=='BUY':commitment+=remaining*(D(b['price'])+D(b['fee_per_share']))
   orders.append(dict(b,filled=filled,remaining=remaining,status='UNKNOWN' if unknown else 'FILLED' if filled==b['quantity'] else 'CANCELLED' if cancelled else 'PARTIAL' if filled else 'PENDING'))
  nav=cash_balance+sum(positions.values())*D(self.mandate['price'])
  return {'cash':cash(cash_balance),'nav':cash(nav),'fees':cash(fees),'positions':positions,'quantity':sum(positions.values()),'orders':orders,'commitments':cash(commitment),'cash_after_commitments':cash(cash_balance-commitment),'ordinary_turnover':{k:cash(v) for k,v in ordinary.items()},'exit_turnover':{k:cash(v) for k,v in exit_turn.items()},'pnl':cash(nav-D(self.mandate['cash']))}
 def strategies(self):
  out={}
  for f in self.s.facts():
   b=f['body']
   if f['kind']=='STRATEGY':out[b['id']]=dict(b,status='candidate')
   if f['kind']=='STRATEGY_STATE' and b['id'] in out:out[b['id']].update(status=b['status'],reason=b.get('reason',''),decision_ref=f['seq'])
  return out
 def strategy_state(self,name,status,key,reason):
  previous=self.strategies().get(name,{}).get('status')
  allowed={'candidate':{'evaluated'},'evaluated':{'eligible','rejected'},'eligible':{'active','suspended'},'active':{'retiring','suspended'},'suspended':{'retiring'},'retiring':{'retired'},'retired':set(),'rejected':set()}
  if self.s.find(key):return
  if status not in allowed.get(previous,set()):raise Refused('INVALID_STRATEGY_TRANSITION',(previous,status))
  self.s.append(key,'STRATEGY_STATE',{'id':name,'status':status,'reason':reason,'policy':self.mandate['policy']})
 def opening_permitted(self):
  if self.s.get('paused',False):raise Refused('MANDATE_PAUSED','New exposure stopped; reconciliation and exits remain permitted')
  if self.s.get('opening_expired',False):raise Refused('OPENING_AUTHORITY_EXPIRED')
  if self.s.get('mark_age',0)>30:raise Refused('STALE_MARK','Fresh declared mark needed')
  if any(x['status']=='UNKNOWN' for x in self.state()['orders']):raise Refused('UNKNOWN_ORDER','Resolve original IDs before new exposure')
 def allocate(self,batch,requests,day,expected=None):
  existing=self.s.find(batch)
  if existing:return existing['body']
  self.opening_permitted()
  if expected is not None and expected!=self.s.revision():raise Refused('STALE_REVISION')
  book=self.state();strategies=self.strategies();eligible={k:D(v) for k,v in requests.items() if strategies[k]['status'] in ('eligible','active')};excluded={k:'Strategy is '+strategies[k]['status'] for k in requests if k not in eligible}
  price=D(self.mandate['price']);fee=D(self.mandate['fee_per_share']);nav=D(book['nav']);den=nav-sum(eligible.values())*fee-D(book['commitments'])*D('0.001')
  if den<=0:raise Refused('INVALID_RISK_DENOMINATOR')
  q={k:min(v,D('.20')*den/price) for k,v in eligible.items()};stages=[{'rule':'strategy 20%','quantities':{k:str(v) for k,v in q.items()}}]
  # All immutable strategies in this slice target the same canonical AAA exposure.
  if sum(q.values())*price>den*D('.25'):
   factor=den*D('.25')/(sum(q.values())*price);q={k:v*factor for k,v in q.items()}
  stages.append({'rule':'AAA aggregate 25%','quantities':{k:str(v) for k,v in q.items()}})
  opening=self.s.get('opening-nav/'+day)
  if opening is None:opening=book['nav'];self.s.set('opening-nav/'+day,opening)
  capacity=min(den*D('.40')/price,(D(book['cash_after_commitments'])-den*D('.60'))/(price+fee),(D(opening)*D('.20')-D(book['ordinary_turnover'].get(day,'0')))/price)
  if sum(q.values())>max(D(0),capacity):
   factor=max(D(0),capacity)/sum(q.values());q={k:v*factor for k,v in q.items()}
  stages.append({'rule':'gross / cash / daily turnover','quantities':{k:str(v) for k,v in q.items()}})
  quantities={k:int(v.to_integral_value(rounding=ROUND_FLOOR)) for k,v in q.items()}
  # New first allocations only; no hidden internal crossing or redistribution.
  if any(book['positions'].get(k,0) for k in eligible):raise Refused('NONZERO_STARTING_TARGET','This bounded batch opens new eligible versions only')
  final_cost=sum(quantities.values())*(price+fee)
  if D(book['cash_after_commitments'])-final_cost<den*D('.60'):raise Refused('CASH_FLOOR')
  body={'id':batch,'day':day,'requested':requests,'admitted':quantities,'excluded':excluded,'denominator':str(den),'constraints':stages,'opening_nav':opening,'portfolio_revision':self.s.revision(),'fee_ceiling':cash(sum(quantities.values())*fee),'absolute_targets':True,'rounding':'Down once to whole shares; residual remains cash'}
  self.s.append(batch,'ALLOCATION',body,'allocator',expected=expected)
  for k,n in quantities.items():
   if n:
    self.strategy_state(k,'active',batch+'/active/'+k,'First lawful allocation under DA-O')
    self.order(batch+'/'+k+'/BUY',k,n,'BUY',day,batch)
  return body
 def order(self,oid,strategy,n,side,day,decision,exit_id=None):
  if self.s.find('order/'+oid):return
  if side=='BUY':self.opening_permitted()
  else:
   if not exit_id or not self.s.find(exit_id):raise Refused('EXIT_AUTHORITY_MISSING')
   if n>self.positions().get(strategy,0):raise Refused('OVERSELL')
  self.s.append('order/'+oid,'ORDER',{'id':oid,'strategy':strategy,'instrument':'AAA','quantity':n,'side':side,'price':self.mandate['price'],'fee_per_share':self.mandate['fee_per_share'],'day':day,'virtual_time':self.s.get('clock','D1 18:00'),'decision':decision,'exit':exit_id,'revision':self.s.revision()},'paper-book')
 def reconcile(self,oid):
  response=self.adapter.query(oid);order=next(x for x in self.state()['orders'] if x['id']==oid)
  for receipt in response['fills']:
   old=self.s.find('fill/'+receipt['id'])
   body=dict(receipt,strategy=order['strategy'],side=order['side'],exit=order['exit'],day=order['day'])
   if old:
    if old['body']!=body:raise Refused('CONTRADICTORY_RECEIPT')
    continue
   already=sum(x['body']['quantity'] for x in self.s.facts('FILL') if x['body']['order']==oid)
   if receipt['quantity']<=0 or already+receipt['quantity']>order['quantity'] or D(receipt['price'])!=D(order['price']) or D(receipt['fee'])!=D(receipt['quantity'])*D(order['fee_per_share']):raise Refused('INVALID_EXECUTION_RECEIPT')
   if receipt['side'] if 'side' in receipt else False:raise Refused('UNEXPECTED_RECEIPT_FIELD')
   if order['side']=='SELL' and receipt['quantity']>self.positions().get(order['strategy'],0):raise Refused('OVERSELL_RECEIPT')
   self.s.append('fill/'+receipt['id'],'FILL',body,'paper-book')
  self.s.set('unknown/'+oid,False)
  if response['status']=='CANCELLED':self.s.append('cancel/'+oid,'CANCELLED',{'order':oid},'paper-book')
  return response
 def send(self,oid,quantity=None,lose_response=False):
  order=next(x for x in self.state()['orders'] if x['id']==oid)
  if order['status']=='FILLED':return
  # Submitted order recovery is permitted after revocation; a fresh buy is not.
  existing=None
  try:existing=self.adapter.query(oid)
  except Refused as ex:
   if ex.code!='ORDER_NOT_FOUND':raise
  if not existing:
   if order['side']=='BUY':self.opening_permitted()
   else:self.exit_check(order['exit'])
   raw=self.s.find('order/'+oid)['body']
   try:self.adapter.submit(raw,quantity if quantity is not None else order['quantity'],lose_response)
   except LostResponse:
    self.s.set('unknown/'+oid,True);self.s.append('lost/'+oid,'INTERRUPTION',{'order':oid,'reason':'Adapter accepted; caller response lost. Query original ID; no replacement.'},'operator');return
  self.reconcile(oid)
 def finish_order(self,oid):
  self.reconcile(oid);s=self.adapter.query(oid)
  if s['remaining'] and s['status']!='CANCELLED':
   if s['order']['side']=='BUY':
    if self.s.get('paused',False):self.adapter.cancel(oid);self.reconcile(oid);return
   else:self.exit_check(s['order']['exit'])
   self.adapter.advance(oid,s['remaining']);self.reconcile(oid)
 def exit_check(self,xid):
  if self.s.get('mark_age',0)>30:raise Refused('STALE_MARK','Exit retained; cannot invent a fill')
  x=self.s.find(xid)['body'];fills=[f['body'] for f in self.s.facts('FILL') if f['body']['exit']==xid];consumed=sum(D(f['fee']) for f in fills);remaining=x['quantity']-sum(f['quantity'] for f in fills);required=D(remaining)*D(self.mandate['fee_per_share'])
  if consumed+required>D(x['envelope']):raise Refused('EXIT_COST_ENVELOPE')
  if D(self.state()['cash'])<required:raise Refused('EXIT_PREFUNDING')
 def retire(self,strategy,day,first=None):
  xid='EXIT/'+strategy
  if self.strategies()[strategy]['status']=='retired':return
  # Cancel and reconcile every live opening order before sizing the exit.
  for o in self.state()['orders']:
   if o['strategy']==strategy and o['side']=='BUY' and o['remaining']:
    try:self.adapter.cancel(o['id']);self.reconcile(o['id'])
    except Refused as ex:
     if ex.code!='ORDER_NOT_FOUND':raise
     self.s.append('cancel/'+o['id'],'CANCELLED',{'order':o['id']},'paper-book')
  if not self.s.find(xid):
   quantity=self.positions().get(strategy,0);nav=D(self.state()['nav']);envelope=(nav*D('.0025')).quantize(D('.01'),rounding=ROUND_FLOOR)
   self.strategy_state(strategy,'retiring','retiring/'+strategy,'Immutable holding window ended; DA-X; exit-only authority survives research/opening expiry')
   self.s.append(xid,'EXIT',{'strategy':strategy,'quantity':quantity,'target':0,'pre_exit_nav':cash(nav),'envelope':cash(envelope),'authority':'DA-X / C-05','deadline':self.strategies()[strategy]['deadline'],'revision':self.s.revision()},'portfolio')
  x=self.s.find(xid)['body'];self.exit_check(xid)
  if x['quantity']:
   oid=xid+'/SELL';self.order(oid,strategy,x['quantity'],'SELL',day,xid,xid);self.send(oid,first)
   if first is None:self.finish_order(oid)
  if self.positions().get(strategy,0)==0 and not any(o['strategy']==strategy and o['remaining'] for o in self.state()['orders']):self.strategy_state(strategy,'retired','retired/'+strategy,'Flat, no executable order, all receipts reconciled')
