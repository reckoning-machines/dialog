"""Dialog-domain command journal and append-only facts. Never opens ARH storage."""
import json,sqlite3,threading,time,uuid
from pathlib import Path
from contextlib import contextmanager
from .fixtures import digest
class Refused(Exception):
 def __init__(self,code,detail=''):self.code=code;self.detail=detail;super().__init__(code+(': '+str(detail) if detail else ''))
class Store:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.db() as c:
   c.executescript('''CREATE TABLE IF NOT EXISTS facts(seq INTEGER PRIMARY KEY, key TEXT UNIQUE NOT NULL, kind TEXT NOT NULL, actor TEXT NOT NULL, body TEXT NOT NULL, sha256 TEXT NOT NULL, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS requests(key TEXT PRIMARY KEY, op TEXT, payload TEXT, response TEXT);
CREATE TABLE IF NOT EXISTS values_store(key TEXT PRIMARY KEY,value TEXT NOT NULL);''')
 @contextmanager
 def db(self):
  c=sqlite3.connect(self.path,timeout=30);c.row_factory=sqlite3.Row;c.execute('PRAGMA journal_mode=WAL');c.execute('PRAGMA synchronous=FULL')
  try:
   c.execute('BEGIN IMMEDIATE');yield c;c.commit()
  except BaseException:c.rollback();raise
  finally:c.close()
 def get(self,key,default=None):
  with self.db() as c:r=c.execute('SELECT value FROM values_store WHERE key=?',(key,)).fetchone()
  return json.loads(r[0]) if r else default
 def set(self,key,value):
  with self.db() as c:c.execute('INSERT INTO values_store VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',(key,json.dumps(value,sort_keys=True)))
 def facts(self,kind=None):
  with self.db() as c:
   rows=c.execute('SELECT * FROM facts'+(' WHERE kind=?' if kind else '')+' ORDER BY seq',((kind,) if kind else ())).fetchall()
  return [dict(seq=r['seq'],key=r['key'],kind=r['kind'],actor=r['actor'],body=json.loads(r['body']),sha256=r['sha256'],created=r['created']) for r in rows]
 def find(self,key):return next((r for r in self.facts() if r['key']==key),None)
 def append(self,key,kind,body,actor='policy',expected=None):
  text=json.dumps(body,sort_keys=True);h=digest(body)
  with self.db() as c:
   old=c.execute('SELECT * FROM facts WHERE key=?',(key,)).fetchone()
   if old:
    if old['sha256']!=h or old['kind']!=kind:raise Refused('COMMAND_MISMATCH',key)
    return old['seq']
   n=c.execute('SELECT COALESCE(MAX(seq),0) FROM facts').fetchone()[0]
   if expected is not None and n!=expected:raise Refused('STALE_REVISION',{'expected':expected,'actual':n})
   c.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?)',(n+1,key,kind,actor,text,h,time.time()));return n+1
 def revision(self):
  with self.db() as c:return c.execute('SELECT COALESCE(MAX(seq),0) FROM facts').fetchone()[0]
 def intent(self,key,op,payload):
  raw=json.dumps(payload,sort_keys=True)
  with self.db() as c:
   r=c.execute('SELECT * FROM requests WHERE key=?',(key,)).fetchone()
   if r:
    if r['op']!=op or r['payload']!=raw:raise Refused('COMMAND_MISMATCH',key)
    return json.loads(r['response']) if r['response'] else None
   c.execute('INSERT INTO requests VALUES(?,?,?,NULL)',(key,op,raw))
 def reply(self,key,result):
  with self.db() as c:c.execute('UPDATE requests SET response=? WHERE key=?',(json.dumps(result,sort_keys=True),key))
 def call(self,connection,key,op,payload):
  response=self.intent(key,op,payload)
  if response is None:
   public_key=self.get('request-key/'+connection.actor+'/'+key)
   if public_key is None:
    public_key=connection.new_key();self.set('request-key/'+connection.actor+'/'+key,public_key)
   prior=connection.outcome(public_key)
   response=prior if prior.get('status') in ('COMMITTED','REFUSED') else connection.call(op,payload,public_key).raw
   self.reply(key,response)
  from arh_client import Outcome
  return Outcome.from_reply(response).raise_for_refusal()
