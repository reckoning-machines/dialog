"""Replaceable execution adapter and deterministic durable synthetic receipts.

This is a bounded fixture adapter, not a market backtester or broker. The desk
owns admission/book facts; this separate database owns only simulated receipts.
"""
from typing import Protocol
from decimal import Decimal as D
from .store import Store,Refused
class LostResponse(Exception):pass
class ExecutionAdapter(Protocol):
 def submit(self,order:dict,first:int,lose_response:bool=False)->dict:...
 def query(self,order_id:str)->dict:...
 def advance(self,order_id:str,quantity:int)->dict:...
 def cancel(self,order_id:str)->dict:...
class SyntheticExecution:
 model='synthetic-fixed-price-v1'
 def __init__(self,path):self.store=Store(path)
 def query(self,order_id):
  order=self.store.find('order/'+order_id)
  if not order:raise Refused('ORDER_NOT_FOUND',order_id)
  receipts=[x['body'] for x in self.store.facts('EXECUTION') if x['body']['order']==order_id]
  total=sum(x['quantity'] for x in receipts);cancelled=self.store.find('cancel/'+order_id)
  return {'order':order['body'],'fills':receipts,'filled':total,'remaining':order['body']['quantity']-total,'status':'FILLED' if total==order['body']['quantity'] else 'CANCELLED' if cancelled else 'PARTIAL' if total else 'ACCEPTED','model':self.model}
 def submit(self,order,first,lose_response=False):
  existed=self.store.find('order/'+order['id']);self.store.append('order/'+order['id'],'ORDER_RECEIPT',order,'adapter')
  if not existed:self.advance(order['id'],first)
  if lose_response and not existed:raise LostResponse(order['id'])
  return self.query(order['id'])
 def advance(self,order_id,quantity):
  s=self.query(order_id)
  if s['status']=='CANCELLED':raise Refused('ORDER_CANCELLED')
  if s['remaining']==0:return s
  if quantity<=0 or quantity>s['remaining']:raise Refused('INVALID_FILL_QUANTITY')
  total=s['filled']+quantity;order=s['order'];receipt={'id':order_id+'/F'+str(total),'order':order_id,'quantity':quantity,'price':order['price'],'fee':f"{D(quantity)*D(order['fee_per_share']):.2f}",'timestamp':order['virtual_time'],'model':self.model}
  self.store.append(receipt['id'],'EXECUTION',receipt,'adapter');return self.query(order_id)
 def cancel(self,order_id):
  s=self.query(order_id)
  if s['status']!='FILLED':self.store.append('cancel/'+order_id,'CANCEL_RECEIPT',{'order':order_id},'adapter')
  return self.query(order_id)
