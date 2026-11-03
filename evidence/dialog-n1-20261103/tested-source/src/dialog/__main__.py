"""Loopback workspace and local CLI. No broker, provider or remote deployment."""
import argparse,fcntl,json,os,threading,time,uuid,sys,signal
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from .desk import Desk
from .store import Refused

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--data',default='.local/dialog');parser.add_argument('--port',type=int,default=8787);parser.add_argument('--through',type=int);parser.add_argument('--stop-host',action='store_true');args=parser.parse_args()
 root=Path(args.data).resolve();root.mkdir(parents=True,exist_ok=True);lock=open(root/'desk.lock','a+')
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:raise SystemExit('This desk already has an active coordinator. Open its browser or use a different --data directory.')
 desk=Desk(root).start()
 if args.through is not None:
  try:
   while desk.checkpoint()<args.through:
    state=desk.advance();print(json.dumps({'step':state['step'],'stage':state['stage'],'cash':state['book']['cash']}),flush=True)
   print(json.dumps(desk.snapshot(),sort_keys=True),flush=True)
  finally:
   if args.stop_host:desk.g.stop()
  return
 mutex=threading.RLock();status={'busy':False,'last_error':None}
 def run_to(target):
  try:
   while desk.checkpoint()<target:
    with mutex:desk.advance()
    time.sleep(.65)
  except Exception as ex:
   status['last_error']=str(ex);desk.error=str(ex)
   desk.s.append('exception/'+str(uuid.uuid4()),'EXCEPTION',{'reason':str(ex),'action':'Recover the original operation or resolve the missing prerequisite; no bypass'},'operator')
  finally:status['busy']=False
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def send_json(self,body,status_code=200):
   raw=json.dumps(body).encode();self.send_response(status_code);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
  def do_GET(self):
   if self.path=='/':
    raw=Path(__file__).with_name('workspace.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'");self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
   elif self.path=='/api/state':
    if mutex.acquire(blocking=False):
     try:
      state=desk.snapshot(refresh=not status['busy']);state['busy']=status['busy'];state['error']=status['last_error'] or state['error']
      if state['error']:state['decisions']=[{'code':'DESK_BLOCKED','reason':state['error'],'action':'Reconnect / recover original work; missing authority cannot be waived'}]
     finally:mutex.release()
    else:state=desk.snapshot();state['busy']=True
    self.send_json(state)
   elif self.path=='/api/evidence':self.send_json({'domain_records':desk.s.facts(),'arh_public':desk.g.journal.get('public-export')})
   else:self.send_json({'error':'NOT_FOUND'},404)
  def do_POST(self):
   if self.path!='/api/action':return self.send_json({'error':'NOT_FOUND'},404)
   origin=self.headers.get('Origin');allowed={'http://127.0.0.1:'+str(args.port),'http://localhost:'+str(args.port)}
   if self.headers.get('X-Dialog')!='local-desk' or (origin and origin not in allowed):return self.send_json({'error':'ORIGIN_REFUSED'},403)
   try:
    length=int(self.headers.get('Content-Length','0'))
    if length>4096:raise Refused('REQUEST_TOO_LARGE')
    body=json.loads(self.rfile.read(length));action=body['action'];key=body['key'];uuid.UUID(key)
    if status['busy']:raise Refused('WORK_IN_PROGRESS','Observe current progress; no duplicate worker')
    with mutex:
     old=desk.s.intent('ui/'+key,action,body)
     if old:return self.send_json(old)
     if body.get('expected')!=desk.s.revision():raise Refused('STALE_REVISION','Refresh before a new action')
     if action=='pause':
      paused=not desk.s.get('paused',False);desk.s.append('ui/'+key,'OWNER_PAUSE',{'paused':paused,'reason':'Local owner pauses new work; settlement, fill reconciliation and bounded exits remain authorized'},'owner');desk.s.set('paused',paused)
     elif action in ('run','next','exits','recover'):
      if action=='exits' and desk.checkpoint()<15:raise Refused('RESEARCH_NOT_COMPLETE','Use the next scheduled step; no silent skipped slot')
      if action=='recover':desk.g.start();status['last_error']=None
      target=15 if action=='run' else 17 if action=='exits' else min(17,desk.checkpoint()+1)
      status['busy']=True;status['last_error']=None;threading.Thread(target=run_to,args=(target,),daemon=True).start()
     else:raise Refused('UNSUPPORTED_ACTION')
     result={'status':'ACCEPTED','action':action,'command':key};desk.s.reply('ui/'+key,result);self.send_json(result,202)
   except (Refused,ValueError,KeyError) as ex:self.send_json({'error':str(ex)},409)
 server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
 print('Dialog ready at http://127.0.0.1:'+str(args.port)+'/ · '+str(root),flush=True)
 try:server.serve_forever(poll_interval=.2)
 finally:server.server_close()
if __name__=='__main__':main()
