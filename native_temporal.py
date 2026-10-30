import os
import contextlib,datetime as dt,io,json,pathlib,random,subprocess,time
import generated_typed as g
from hypothesis import find,settings,strategies as st
from literalizer import InputFormat,NewVariable,literalize
from literalizer.languages import Python
from literalizer.exceptions import UnrepresentableInputError
from scripts.roundtrip_common import verify

ROOT=pathlib.Path(__file__).parent/os.environ.get('DISCOVERY_TAG','native-temporal');ROOT.mkdir(exist_ok=False)
rows=[];start=time.monotonic()
def rejection(v,b,m):
    off=(v.utcoffset() or dt.timedelta())//dt.timedelta(microseconds=1)
    if (m==2 or (b=='python' and m==1)) and g.epoch_us(v)%1000000:return 'inexact integer epoch'
    if b=='javascript' and m==0 and g.epoch_us(v)%1000:return 'inexact native Date'
    if b=='go' and m==0 and off%1000000:return 'inexact native UTC offset'
    return None

def program(v,b,m):
    p=g.spec(b,m)
    if b=='ruby':return 'result_data = '+p.format_datetime(v)+'\n'+g.RB,'.rb'
    r=literalize(source='{"$ref":"native_value"}',input_format=InputFormat.JSON,language=p,ref_key='$ref',bound_refs={'native_value':v},variable_form=NewVariable(name='result_data',modifiers=frozenset()),wrap_in_file=True)
    if b=='python':return r.code+'\n'+g.PY,'.py'
    if b=='javascript':return r.code+'\nconst probeSchema='+json.dumps(g.schema(v))+';\n'+g.JS,'.js'
    assert r.code.startswith('package main\n')
    code=r.code.replace('package main\n','package main\nimport ("encoding/json";"reflect";"sort";"fmt";"strconv";"strings")\n',1)
    body,last=code.rsplit('\n}',1)
    out=body+'\nout,err:=json.Marshal(map[string]any{"value":probeNorm(reflect.ValueOf(result_data),"")});if err!=nil{panic(err)};fmt.Print(string(out))\n}'+last
    schema='map[string]string{'+','.join(json.dumps(k)+':'+json.dumps(t) for k,t in g.schema(v).items())+'}'
    return out+'\nvar probeSchema='+schema+'\n'+g.GO,'.go'

pairs=[(0,1),(0,-1),(0,1000000),(0,-1000000),(1000,1000),(1,1),(999999,-1),(123456,123456)]
for seed in [5493,6579,0]:
 rng=random.Random(seed)
 for i,(wall,off) in enumerate(pairs):
  v=dt.datetime(rng.choice([1969,1970,2001]),rng.randint(1,12),rng.randint(1,28),rng.randrange(24),rng.randrange(60),rng.randrange(60),wall,tzinfo=dt.timezone(dt.timedelta(microseconds=off)))
  for b in ['python','ruby','go','javascript']:
   for m in range(2 if b=='python' else 3):
    assert time.monotonic()-start<600
    row=dict(seed=seed,index=i,backend=b,mode=m,value=v.isoformat(),expected_rejection=rejection(v,b,m));path=ROOT/f'{seed}-{i}-{b}-{m}';path.mkdir()
    try:
     code,extension=program(v,b,m);file=path/('main'+extension);file.write_text(code)
     runtime=g.RUNTIMES[b+str(m)] if b=='python' else g.RUNTIMES[b];cmd=[runtime,'run',str(file)] if b=='go' else [runtime,str(file)]
     q=subprocess.run(cmd,capture_output=True,text=True,timeout=15);(path/'stdout.txt').write_text(q.stdout);(path/'stderr.txt').write_text(q.stderr)
     if q.returncode:row.update(status='runtime_failure',stderr=q.stderr)
     elif row['expected_rejection']:row.update(status='unexpected_acceptance',actual=json.loads(q.stdout))
     else:
      wanted={'value':g.expected(v,b,m)}
      with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):verify(label='native',produced_json=q.stdout,expected_json=json.dumps(wanted),exclude_keys=())
      row['status']='pass'
    except UnrepresentableInputError as e:row.update(status='expected_rejection' if row['expected_rejection'] else 'unexpected_rejection',message=str(e))
    except SystemExit as e:row.update(status='mismatch',message=str(e))
    except Exception as e:row.update(status='exception',exception=type(e).__name__,message=str(e))
    (path/'context.json').write_text(json.dumps(row,indent=2));rows.append(row)
    (ROOT/'report.json').write_text(json.dumps(dict(seconds=time.monotonic()-start,rows=rows),indent=2))

from collections import Counter
if os.environ.get('SKIP_SHRINK'):
 print(json.dumps(dict(seconds=time.monotonic()-start,counts=Counter(r['status'] for r in rows))))
 raise SystemExit(0)
spec=Python(datetime_format=Python.datetime_formats.EPOCH);calls=[]
strategy=st.builds(dt.datetime,year=st.integers(1970,2024),month=st.integers(1,12),day=st.integers(1,28),hour=st.integers(0,23),minute=st.integers(0,59),second=st.integers(0,59),microsecond=st.integers(0,999999),tzinfo=st.builds(dt.timezone,st.builds(dt.timedelta,microseconds=st.integers(-86399999999,86399999999))))
def fails(v):
 calls.append(v.isoformat())
 if g.epoch_us(v)%1000000==0:return False
 try:literalize(source='{"$ref":"stamp"}',input_format=InputFormat.JSON,language=spec,ref_key='$ref',bound_refs={'stamp':v},variable_form=NewVariable(name='result_data',modifiers=frozenset()),wrap_in_file=True)
 except UnrepresentableInputError:return False
 return True
smallest=find(strategy,fails,settings=settings(max_examples=200,database=None,derandomize=True,deadline=None))
(ROOT/'minimized.json').write_text(json.dumps(dict(value=smallest.isoformat(),calls=len(calls),trace=calls),indent=2))
from collections import Counter
print(json.dumps(dict(seconds=time.monotonic()-start,counts=Counter(r['status'] for r in rows),smallest=smallest.isoformat(),shrink_calls=len(calls))))
