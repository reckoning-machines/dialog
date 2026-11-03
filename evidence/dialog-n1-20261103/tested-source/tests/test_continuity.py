"""Actual process death, fresh coordinator and public-host recovery; no ARH DB reads."""
import json,os,signal,socket,subprocess,sys,tempfile,time,unittest,urllib.request,urllib.error,uuid
from pathlib import Path
from dialog.governance import Governance,write
class LocalDeskContinuity(unittest.TestCase):
 def test_two_cycles_process_death_and_final_exit(self):
  root=Path(tempfile.mkdtemp(prefix='dialog-cpoc-',dir='/private/tmp'));out=Path(os.environ.get('DIALOG_TEST_EVIDENCE','/private/tmp/dialog-app-evidence'))/root.name;out.mkdir(parents=True);process=None;boundaries=[]
  with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
  base='http://127.0.0.1:'+str(port)
  def state():return json.load(urllib.request.urlopen(base+'/api/state',timeout=30))
  def start():
   log=open(root/'web.log','ab');p=subprocess.Popen([sys.executable,'-m','dialog','--data',str(root),'--port',str(port)],stdout=log,stderr=log,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));log.close()
   for _ in range(1200):
    if p.poll() is not None:raise AssertionError((root/'web.log').read_text()[-3500:])
    try:state();return p
    except Exception:time.sleep(.05)
   raise AssertionError('Server readiness timeout')
  def action(name,expected=None,key=None):
   s=state();payload={'action':name,'expected':s['revision'] if expected is None else expected,'key':key or str(uuid.uuid4())};req=urllib.request.Request(base+'/api/action',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','X-Dialog':'local-desk'});return json.load(urllib.request.urlopen(req,timeout=30))
  def next_step():
   before=state()['step'];action('next')
   for _ in range(1200):
    s=state()
    if not s['busy']:
     self.assertIsNone(s['error'],s['error']);self.assertEqual(s['step'],before+1);write(out/f"step-{s['step']:02}.json",s);return s
    time.sleep(.05)
   raise AssertionError('Step did not finish')
  try:
   process=start();write(out/'opened.json',state())
   with self.assertRaises(urllib.error.HTTPError) as invalid:action('next',expected=-1)
   self.assertEqual(invalid.exception.code,409)
   # A second coordinator is refused by the process lock before new governance work.
   second=subprocess.run([sys.executable,'-m','dialog','--data',str(root),'--port',str(port+1)],capture_output=True,text=True,env=os.environ)
   self.assertNotEqual(second.returncode,0);self.assertIn('active coordinator',second.stderr)
   for target in (4,7,10):
    while state()['step']<target:next_step()
    before=state();old_pid=process.pid;process.kill();process.wait(timeout=10);self.assertEqual(process.returncode,-9)
    # At the uncertain-research boundary also replace the actual ARH host/core.
    if target==10:Governance(root).stop()
    process=start();after=state();self.assertEqual(before['book'],after['book']);self.assertEqual(before['budgets'],after['budgets'])
    boundaries.append({'boundary':target,'old_pid':old_pid,'old_returncode':-9,'fresh_pid':process.pid,'same_book':True,'same_budgets':True,'core_reopened':target==10})
   while state()['step']<15:next_step()
   s=state();self.assertEqual(s['book']['quantity'],198);self.assertEqual(s['book']['cash'],'80140.40');self.assertEqual(s['book']['fees'],'59.60');self.assertEqual(s['strategies']['R1']['status'],'rejected');self.assertEqual(s['strategies']['T1']['status'],'retired');self.assertEqual(s['obligations']['pending_attempts'],[])
   self.assertEqual(s['budgets']['G-R1']['committed'],'1.75');self.assertEqual(s['budgets']['G-R2']['committed'],'2.25');self.assertEqual(s['budgets']['G-C1']['committed'],'1.00');self.assertEqual(s['budgets']['G-C2']['committed'],'1.00')
   before=Governance(root).export();process.kill();process.wait(timeout=10);process=start();after=Governance(root).export();self.assertEqual(before['closure'],after['closure'])
   next_step();s=next_step();self.assertEqual(s['book']['quantity'],0);self.assertEqual(s['book']['cash'],'99920.60');self.assertEqual(s['book']['fees'],'79.40');self.assertTrue(all(v['status'] in ('retired','rejected') for v in s['strategies'].values()))
   self.assertEqual(len(s['book']['orders']),6)
   evidence=json.load(urllib.request.urlopen(base+'/api/evidence'));write(out/'evidence.json',evidence)
   events=evidence['domain_records'];self.assertEqual(len([x for x in events if x['kind']=='FILL']),8)
   self.assertEqual(len([x for x in events if x['kind']=='ALLOCATION']),2)
   self.assertTrue(any(x['kind']=='MONITOR' for x in events));write(out/'boundaries.json',boundaries);write(out/'result.json',{'status':'PASS','root':str(root),'step15':{'cash':'80140.40','quantity':198,'fees':'59.60'},'step17':{'cash':'99920.60','quantity':0,'fees':'79.40'},'actual_kill_boundaries':4,'public_interface_only':True})
  finally:
   if process and process.poll() is None:process.terminate();process.wait(timeout=10)
   Governance(root).stop()
if __name__=='__main__':unittest.main()
