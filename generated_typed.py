"""Temporary seeded typed discovery with independent native consumers."""
import base64, contextlib, datetime as dt, io, json, math, os, pathlib, random, subprocess, time
import tomlkit
from ruamel.yaml import YAML
from literalizer import InputFormat, NewVariable, CollectionLayout, literalize, literalize_call
from literalizer.languages import Python, Ruby, Go, JavaScript
from literalizer.exceptions import UnrepresentableInputError
from scripts.roundtrip_common import verify

ROOT=pathlib.Path(__file__).parent/os.environ.get('DISCOVERY_TAG','typed-generated')
UTC=dt.timezone.utc
SEEDS=[5493,6579,0]
RUNTIMES={'python0':'/Users/adam/.local/share/uv/python/cpython-3.8.20-macos-aarch64-none/bin/python3.8','python1':'/Users/adam/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/bin/python3.12','ruby':'/opt/homebrew/opt/ruby/bin/ruby','go':'/opt/homebrew/bin/go','javascript':'/opt/homebrew/bin/node'}

def epoch_us(v):
    if v.tzinfo is None:v=v.replace(tzinfo=UTC)
    return (v-dt.datetime(1970,1,1,tzinfo=UTC))//dt.timedelta(microseconds=1)

def sort_tagged(v):return sorted(v,key=lambda x:json.dumps(x,separators=(',',':'),ensure_ascii=False))
def expected(v,b,mode):
    if isinstance(v,dt.datetime):
        if mode==2 or (b=='python' and mode==1):return expected(epoch_us(v)//1000000,b,mode)
        if mode==1:return ['str',v.isoformat()]
        if b in ('python','javascript') and v.tzinfo is None:return ['datetime-naive',v.isoformat(timespec='microseconds')]
        off=(v.utcoffset() or dt.timedelta())//dt.timedelta(microseconds=1)
        return ['datetime',str(epoch_us(v)),str(0 if b=='javascript' else off)]
    if isinstance(v,dt.date):return ['date' if mode==0 else 'str',v.isoformat()]
    if isinstance(v,dt.time):
        return ['time',v.isoformat(timespec='microseconds')] if b in ('python','go') else ['str',v.isoformat()]
    if isinstance(v,bytes):
        if b=='python' and mode==0:return ['bytes',v.hex()]
        return ['str',base64.b64encode(v).decode() if mode==1 else v.hex()]
    if isinstance(v,dict):return ['mapping',sort_tagged([[expected(k,b,mode),expected(x,b,mode)] for k,x in v.items()])]
    if isinstance(v,list):return ['sequence',[expected(x,b,mode) for x in v]]
    if isinstance(v,set):return ['set',sort_tagged([expected(x,b,mode) for x in v])]
    if isinstance(v,bool):return ['bool',v]
    if isinstance(v,(int,float)) and not isinstance(v,bool):
        tag='number' if b=='javascript' else type(v).__name__
        if isinstance(v,float) and math.isnan(v):return [tag,'nan']
        if isinstance(v,float) and math.isinf(v):return [tag,'-inf' if v<0 else '+inf']
        if v==0 and (isinstance(v,float) or b=='javascript'):return [tag,'-zero' if math.copysign(1,v)<0 else '+zero']
        return [tag,v]
    return ['str',v] if isinstance(v,str) else ['NoneType',None]

def schema(v,path='',out=None):
    if out is None:out={}
    if isinstance(v,dt.datetime):out[path]='datetime-naive' if v.tzinfo is None else 'datetime'
    elif isinstance(v,dt.date):out[path]='date'
    elif isinstance(v,dt.time):out[path]='time'
    elif isinstance(v,dict):
        for k,x in v.items():schema(x,path+'/'+str(k),out)
    elif isinstance(v,list):
        for i,x in enumerate(v):schema(x,path+'/'+str(i),out)
    elif isinstance(v,set):
        for x in v:schema(x,path+'/#',out)
    return out

def rejection(v,b,mode):
    if isinstance(v,dt.datetime):
        if mode==2 or (b=='python' and mode==1):return 'fractional integer epoch' if epoch_us(v)%1000000 else None
        if b=='javascript' and mode==0:return 'submillisecond Date' if epoch_us(v)%1000 else None
    if isinstance(v,dict):
        for x in v.values():
            r=rejection(x,b,mode)
            if r:return r
    if isinstance(v,(list,set)):
        for x in v:
            r=rejection(x,b,mode)
            if r:return r
    return None

PY='''
import datetime as _d, dataclasses as _dc, json as _j, math as _m
def _norm(v,p=''):
    if isinstance(v,_d.datetime):
        if v.tzinfo is None:return ['datetime-naive',v.isoformat(timespec='microseconds')]
        return ['datetime',str((v-_d.datetime(1970,1,1,tzinfo=_d.timezone.utc))//_d.timedelta(microseconds=1)),str(v.utcoffset()//_d.timedelta(microseconds=1))]
    if isinstance(v,_d.date):return ['date',v.isoformat()]
    if isinstance(v,_d.time):return ['time',v.isoformat(timespec='microseconds')]
    if isinstance(v,bytes):return ['bytes',v.hex()]
    if _dc.is_dataclass(v):v={f.name:getattr(v,f.name) for f in _dc.fields(v)}
    if isinstance(v,dict):return ['mapping',sorted([[_norm(k),_norm(x)] for k,x in v.items()],key=lambda x:_j.dumps(x,separators=(',',':'),ensure_ascii=False))]
    if isinstance(v,(list,tuple)):return ['sequence',[_norm(x) for x in v]]
    if isinstance(v,(set,frozenset)):return ['set',sorted([_norm(x) for x in v],key=lambda x:_j.dumps(x,separators=(',',':'),ensure_ascii=False))]
    if isinstance(v,float):
        if _m.isnan(v):return ['float','nan']
        if _m.isinf(v):return ['float','-inf' if v<0 else '+inf']
        if v==0:return ['float','-zero' if _m.copysign(1,v)<0 else '+zero']
    return [type(v).__name__,v]
print(_j.dumps({'value':_norm(result_data)}))
'''
RB='''
require 'json'
def probe_norm(v)
  if v.is_a?(Time)
    instant=v.to_r*1000000; offset=v.utc_offset.to_r*1000000
    raise 'submicrosecond drift' unless instant.denominator==1 && offset.denominator==1
    return ['datetime',instant.numerator.to_s,offset.numerator.to_s]
  end
  return ['date',v.iso8601] if defined?(Date) && v.is_a?(Date)
  return ['set',v.to_a.map{|x|probe_norm(x)}.sort_by{|x|JSON.generate(x)}] if defined?(Set) && v.is_a?(Set)
  return ['mapping',v.map{|k,x|[probe_norm(k.is_a?(Symbol) ? k.to_s : k),probe_norm(x)]}.sort_by{|x|JSON.generate(x)}] if v.is_a?(Hash)
  return ['sequence',v.map{|x|probe_norm(x)}] if v.is_a?(Array)
  return ['bool',v] if v==true || v==false
  return ['int',v] if v.is_a?(Integer)
  if v.is_a?(Float)
    return ['float','nan'] if v.nan?
    return ['float',v.negative? ? '-inf' : '+inf'] if v.infinite?
    return ['float',(1.0/v).negative? ? '-zero' : '+zero'] if v.zero?
    return ['float',v]
  end
  return ['str',v] if v.is_a?(String)
  ['NoneType',nil]
end
STDOUT.write(JSON.generate({'value'=>probe_norm(result_data)}))
'''
JS='''
function probeNorm(v,p='') {
 if(v instanceof Date) {
   if(Number.isNaN(v.getTime()))throw Error('invalid Date');
   const pad=(x,n=2)=>x.toString().padStart(n,'0');
   const day=pad(v.getFullYear(),4)+'-'+pad(v.getMonth()+1)+'-'+pad(v.getDate());
   if(probeSchema[p]==='date')return ['date',day];
   if(probeSchema[p]==='datetime-naive')return ['datetime-naive',day+'T'+pad(v.getHours())+':'+pad(v.getMinutes())+':'+pad(v.getSeconds())+'.'+pad(v.getMilliseconds()*1000,6)];
   return ['datetime',(BigInt(v.getTime())*1000n).toString(),'0'];
 }
 if(v instanceof Set)return ['set',Array.from(v,x=>probeNorm(x,p+'/#')).sort((a,b)=>JSON.stringify(a)<JSON.stringify(b)?-1:JSON.stringify(a)>JSON.stringify(b)?1:0)];
 if(Array.isArray(v))return ['sequence',v.map((x,i)=>probeNorm(x,p+'/'+i))];
 if(v instanceof Map || (v && typeof v==='object')) {
   let pairs=Array.from(v instanceof Map ? v.entries() : Object.entries(v),([k,x])=>[probeNorm(k),probeNorm(x,p+'/'+k)]);
   pairs.sort((a,b)=>JSON.stringify(a)<JSON.stringify(b)?-1:JSON.stringify(a)>JSON.stringify(b)?1:0);return ['mapping',pairs];
 }
 if(typeof v==='number') {
   if(Number.isNaN(v))return ['number','nan'];
   if(!Number.isFinite(v))return ['number',v<0?'-inf':'+inf'];
   if(v===0)return ['number',Object.is(v,-0)?'-zero':'+zero'];
   return ['number',v];
 }
 return [typeof v==='boolean'?'bool':typeof v==='string'?'str':'NoneType',v];
}
process.stdout.write(JSON.stringify({value:probeNorm(result_data)}));
'''
GO='''
func probeNorm(v reflect.Value,p string) any {
 if v.Kind()==reflect.Interface {return probeNorm(v.Elem(),p)}
 if v.Type().PkgPath()=="time" && v.Type().Name()=="Time" {
   format:=func(layout string)string{return v.MethodByName("Format").Call([]reflect.Value{reflect.ValueOf(layout)})[0].String()}
   nanos:=v.MethodByName("Nanosecond").Call(nil)[0].Int();if nanos%1000!=0{panic("submicrosecond drift")}
   switch probeSchema[p] {
    case "date": if format("15:04:05.000000Z07:00")!="00:00:00.000000Z"{panic("date clock drift")};return []any{"date",format("2006-01-02")}
    case "time": if format("2006-01-02")!="0000-01-01"{panic("time date drift")};return []any{"time",format("15:04:05.000000")}
    default: u:=v.MethodByName("UnixMicro").Call(nil)[0].Int();o:=v.MethodByName("Zone").Call(nil)[1].Int();return []any{"datetime",strconv.FormatInt(u,10),strconv.FormatInt(o*1000000,10)}
   }
 }
 sortValues:=func(items []any){sort.Slice(items,func(i,j int)bool{a,_:=json.Marshal(items[i]);b,_:=json.Marshal(items[j]);return string(a)<string(b)})}
 switch v.Kind() {
 case reflect.Struct:
   pairs:=[]any{};for i:=0;i<v.NumField();i++{name:=v.Type().Field(i).Tag.Get("json");if name==""{name=strings.ToLower(v.Type().Field(i).Name)};pairs=append(pairs,[]any{[]any{"str",name},probeNorm(v.Field(i),p+"/"+name)})};sortValues(pairs);return []any{"mapping",pairs}
 case reflect.Map:
   items:=[]any{};isSet:=v.Type().Elem().Kind()==reflect.Struct && v.Type().Elem().NumField()==0
   for _,k:=range v.MapKeys(){if isSet{items=append(items,probeNorm(k,p+"/#"))}else{items=append(items,[]any{probeNorm(k,p+"/@key"),probeNorm(v.MapIndex(k),p+"/"+fmt.Sprint(k.Interface()))})}};sortValues(items);if isSet{return []any{"set",items}};return []any{"mapping",items}
 case reflect.Slice,reflect.Array:
   items:=[]any{};for i:=0;i<v.Len();i++{items=append(items,probeNorm(v.Index(i),p+"/"+strconv.Itoa(i)))};return []any{"sequence",items}
 case reflect.Bool:return []any{"bool",v.Bool()}
 case reflect.String:return []any{"str",v.String()}
 case reflect.Int,reflect.Int8,reflect.Int16,reflect.Int32,reflect.Int64:return []any{"int",v.Int()}
 case reflect.Float32,reflect.Float64:
   f:=v.Float();if f!=f{return []any{"float","nan"}};if f>1.7976931348623157e308{return []any{"float","+inf"}};if f< -1.7976931348623157e308{return []any{"float","-inf"}};if f==0{if 1/f<0{return []any{"float","-zero"}};return []any{"float","+zero"}};return []any{"float",f}
 }
 return []any{"NoneType",nil}
}
'''

def spec(b,m):
    cls={'python':Python,'ruby':Ruby,'go':Go,'javascript':JavaScript}[b]
    native={'python':'PYTHON','ruby':'RUBY','go':'GO','javascript':'JS'}[b]
    kwargs=dict(date_format=cls.date_formats[native if m==0 else 'ISO'],datetime_format=cls.datetime_formats[native if m==0 else 'EPOCH' if (m==2 or b=='python') else 'ISO'],bytes_format=cls.bytes_formats['PYTHON' if b=='python' and m==0 else 'BASE64' if m==1 else 'HEX'],variable_type_hints=cls.variable_type_hints_formats['NEVER' if m==0 else 'SAFE'])
    if b=='python':kwargs.update(sequence_format=Python.sequence_formats['LIST' if m==0 else 'TUPLE'],set_format=Python.set_formats['SET' if m==0 else 'FROZENSET'],language_version=Python.version_formats['PY38' if m==0 else 'PY39'],annotation_evaluation=Python.annotation_evaluations.EAGER)
    if b=='go':kwargs.update(declaration_style=Go.declaration_styles['SHORT' if m==0 else 'VAR'],heterogeneous_strategy=Go.heterogeneous_strategies['ERROR' if m==0 else 'RECORD'])
    if b=='javascript':kwargs.update(dict_format=JavaScript.dict_formats['MAP' if m==1 else 'OBJECT'],declaration_style=JavaScript.declaration_styles['CONST' if m==0 else 'LET'])
    if b=='ruby' and m==1:kwargs.update(dict_entry_style=Ruby.dict_entry_styles.SYMBOL)
    return cls(**kwargs)

def make_program(value,b,m,api,source,fmt):
    language=spec(b,m);args=dict(source=source,input_format=fmt,language=language,variable_form=NewVariable(name='result_data',modifiers=frozenset()),collection_layout=CollectionLayout.COMPACT if m==0 else CollectionLayout.MULTILINE)
    if api=='call':result=literalize_call(target_function='probe_consume',parameter_names=['value'],per_element=False,**args)
    else:result=literalize(**args)
    pre='\n'.join(result.preamble)+'\n';code=result.code
    if b=='python':return pre+'def probe_consume(value): return value\n'+code+'\n'+PY,'.py'
    if b=='ruby':return pre+'def probe_consume(value:); value; end\n'+code+'\n'+RB,'.rb'
    if b=='javascript':return pre+'function probe_consume({value}){return value;}\n'+code+'\nconst probeSchema='+json.dumps(schema(value))+';\n'+JS,'.js'
    package,*rest=result.preamble
    schema_literal='map[string]string{'+','.join(json.dumps(k)+':'+json.dumps(v) for k,v in schema(value).items())+'}'
    return package+'\nimport ("encoding/json";"reflect";"sort";"fmt";"strconv";"strings")\n'+'\n'.join(rest)+'\nvar probeSchema='+schema_literal+'\nfunc probe_consume(value any)any{return value}\n'+GO+'\nfunc main(){\n'+code+'\nout,err:=json.Marshal(map[string]any{"value":probeNorm(reflect.ValueOf(result_data),"")});if err!=nil{panic(err)};fmt.Print(string(out))\n}\n','.go'

def mutation(v):
    if not isinstance(v,list) or len(v)!=2 and (not v or v[0]!='datetime'):return v,False
    tag=v[0]
    if tag=='mapping':
        out=list(v[1])
        for i,(key,value) in enumerate(out):
            if key==['str','guard']:continue
            changed,ok=mutation(value)
            if ok:out[i]=[key,changed];return [tag,out],True
        return v,False
    if tag in ('sequence','set'):
        out=list(v[1])
        if not out:return [tag,[['int',0]]],True
        for i,value in enumerate(out):
            changed,ok=mutation(value)
            if ok:
                out[i]=changed
                return [tag,sort_tagged(out) if tag=='set' else out],True
        return v,False
    if tag=='bool':return [tag,not v[1]],True
    if tag=='date':
        day=dt.date.fromisoformat(v[1]);day+=dt.timedelta(days=-1 if day==dt.date.max else 1)
        return [tag,day.isoformat()],True
    if tag=='datetime':return [tag,str(int(v[1])+1000),v[2]],True
    if tag=='datetime-naive':return [tag,(dt.datetime.fromisoformat(v[1])+dt.timedelta(microseconds=1)).isoformat(timespec='microseconds')],True
    if tag=='time':
        clock=dt.time.fromisoformat(v[1]);return [tag,clock.replace(hour=(clock.hour+1)%24).isoformat(timespec='microseconds')],True
    if tag=='bytes':return [tag,v[1]+'00'],True
    if tag=='str':return [tag,v[1]+'changed'],True
    if tag in ('int','float','number'):
        if isinstance(v[1],str):return [tag,{'+zero':'-zero','-zero':'+zero','nan':'+inf','+inf':'-inf','-inf':'+inf'}[v[1]]],True
        return [tag,v[1]+1],True
    return v,False

def date(r):return dt.date.fromordinal(r.randint(dt.date(1,1,1).toordinal(),dt.date(9999,12,31).toordinal()))
def stamp(r):return dt.datetime(r.choice([1969,1970,2001,2024]),r.randint(1,12),r.randint(1,28),r.randrange(24),r.randrange(60),r.randrange(60),r.choice([0,0,1000,123456,999999]),tzinfo=r.choice([None,UTC,dt.timezone(dt.timedelta(hours=5,minutes=30)),dt.timezone(dt.timedelta(hours=-23,minutes=-59))]))
def cases(seed):
    r=random.Random(seed)
    for i in range(12):
        kind=i%6;fmt=InputFormat.YAML
        if kind==0:v=[date(r),date(r)]
        elif kind==1:v=stamp(r) if i<6 else {'stamp':stamp(r),'empty':[]}
        elif kind==2:v=[dt.time(r.randrange(24),r.randrange(60),r.randrange(60),r.choice([0,1,123456])),dt.time(0,0,0)];fmt=InputFormat.TOML
        elif kind==3:v=[bytes(r.randrange(256) for _ in range(r.randrange(6))),b'',b'\0\xff\n']
        elif kind==4:v={date(r),date(r)} if i<6 else {r.randint(-10,10),r.randint(-10,10)}
        else:v=[{'date':date(r),'binary':b'x\xff','empty':[],'number':-0.0},{'date':date(r),'binary':b'','empty':[],'number':1.25}]
        yield i,{'guard':True,'value':v},fmt

def main():
    ROOT.mkdir(exist_ok=False)
    start=time.monotonic();rows=[]
    for si,seed in enumerate(SEEDS):
     for index,value,fmt in cases(seed):
      if fmt is InputFormat.YAML:
       buf=io.StringIO();YAML().dump(value,buf);source=buf.getvalue()
      else:source=tomlkit.dumps(value)
      for b in ('python','ruby','go','javascript'):
       for m in range(2 if b=='python' else 3):
        assert time.monotonic()-start<900
        api='call' if (si+index+m)%2 else 'literal';row=dict(seed=seed,index=index,backend=b,mode=m,api=api,expected_rejection=rejection(value,b,m))
        path=ROOT/f'{seed}-{index}-{b}-{m}';path.mkdir();(path/('input.toml' if fmt is InputFormat.TOML else 'input.yaml')).write_text(source)
        try:
         program,extension=make_program(value,b,m,api,source,fmt);file=path/('main'+extension);file.write_text(program)
         runtime=RUNTIMES[b+str(m)] if b=='python' else RUNTIMES[b]
         cmd=[runtime,'run',str(file)] if b=='go' else [runtime,str(file)]
         p=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
         (path/'stdout.txt').write_text(p.stdout);(path/'stderr.txt').write_text(p.stderr);row.update(command=cmd,returncode=p.returncode)
         if p.returncode:row.update(status='runtime_failure',stderr=p.stderr)
         elif row['expected_rejection']:row.update(status='unexpected_acceptance',actual=json.loads(p.stdout))
         else:
          wanted={'value':expected(value,b,m)};row['expected']=wanted
          with contextlib.redirect_stderr(io.StringIO()),contextlib.redirect_stdout(io.StringIO()):
           verify(label='typed',produced_json=p.stdout,expected_json=json.dumps(wanted),exclude_keys=())
           altered,changed=mutation(json.loads(p.stdout)['value']);assert changed
           try:verify(label='typed-negative',produced_json=json.dumps({'value':altered}),expected_json=json.dumps(wanted),exclude_keys=())
           except SystemExit:row['mutation_rejected']=True
           else:raise AssertionError('mutation accepted')
          row['status']='pass'
        except UnrepresentableInputError as e:row.update(status='expected_rejection' if row['expected_rejection'] else 'unexpected_rejection',message=str(e))
        except SystemExit as e:row.update(status='mismatch',message=str(e))
        except Exception as e:row.update(status='exception',exception=type(e).__name__,message=str(e))
        (path/'context.json').write_text(json.dumps(row,indent=2));rows.append(row)
        (ROOT/'report.json').write_text(json.dumps(dict(seconds=time.monotonic()-start,rows=rows),indent=2))
    from collections import Counter
    print(json.dumps(dict(seconds=time.monotonic()-start,counts=Counter(r['status'] for r in rows))))
    for row in rows:
     if row['status'] not in ('pass','expected_rejection'):print(json.dumps(row))

if __name__=="__main__":main()
