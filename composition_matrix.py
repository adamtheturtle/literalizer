import contextlib,io,json,os,pathlib,subprocess,time
from collections import Counter
import generated_typed as g
from literalizer import InputFormat,NewVariable,literalize,literalize_call,literalize_call_with_declarations,StubReturn
from literalizer.languages import Python,Go,Rust,Cpp
from scripts.roundtrip_common import verify
root=pathlib.Path(__file__).parent/os.environ.get('COMPOSITION_TAG','composition-matrix');root.mkdir(exist_ok=False)
pairs=[({'a':1},{'a':2}),({'a':{'b':1}},{'a':{'b':2}}),({'a':[1,2]},{'a':[3]}),({'a':True},{'a':False}),({'a':[]},{'a':[]}),({'a':1,'b':'x','c':True},{'a':2,'b':'y','c':False})]
rows=[];start=time.monotonic()
for name,cls in [('python',Python),('go',Go),('rust',Rust),('cpp',Cpp)]:
 if os.environ.get('COMPOSITION_BACKEND') and os.environ['COMPOSITION_BACKEND']!=name:continue
 for index,(a,b) in enumerate(pairs):
  for reverse in [False,True]:
   for known in [False,True]:
    assert time.monotonic()-start<300
    row=dict(backend=name,case=index,reverse=reverse,known=known);folder=root/f'{name}-{index}-{reverse}-{known}';folder.mkdir()
    p=cls(heterogeneous_strategy=cls.heterogeneous_strategies.RECORD,**({'module_name':'main'} if name=='cpp' else {}))
    try:
     declarations=[literalize(source=json.dumps(v),input_format=InputFormat.JSON,language=p,variable_form=NewVariable(name=n,modifiers=frozenset())) for n,v in [('alpha',a),('beta',b)]]
     if reverse:declarations.reverse()
     call=literalize_call(source='[[{"$ref":"alpha"},{"$ref":"beta"}]]',input_format=InputFormat.JSON,language=p,target_function='consume',parameter_names=('first','second'),per_element=True,ref_key='$ref',ref_values={'alpha':a,'beta':b} if known else None)
     if name=='python':body=('def consume(*,first,second):\n    global result_data\n    result_data = [first,second]',)
     elif name=='go':body=()
     else:body=p.format_call_stub(('consume',),('first','second'),StubReturn.VOID,([a,b],))
     class_extra=()
     extra=()
     if name in ('rust','cpp'):
      class_extra=p.format_call_class_scope_stub(('consume',),('first','second'),StubReturn.VOID,([a,b],))
      extra=p.format_call_preamble_stub(('consume',),('first','second'),StubReturn.VOID,([a,b],))
     if name=='go':extra=()
     result=literalize_call_with_declarations(language=p,declarations=declarations,call=call,extra_body_preamble=body,extra_class_preamble=class_extra,extra_preamble=extra)
     code=result.code
     if name=='python':code+='\n'+g.PY;extension='.py'
     elif name=='go':code=code.replace('package main\n','package main\nimport ("encoding/json";"reflect";"sort";"fmt";"strconv";"strings")\n',1);code+='\nvar probeSchema=map[string]string{}\n'+g.GO+'\nfunc consume(first any,second any){out,err:=json.Marshal(map[string]any{"value":probeNorm(reflect.ValueOf([]any{first,second}),"")});if err!=nil{panic(err)};fmt.Print(string(out))}\n';extension='.go'
     else:
      def assertion(n,v):
       def field_checks(field,x):
        if isinstance(x,dict):return ''.join(field_checks(field+'.'+k,z) for k,z in x.items())
        if name=='rust':
         if isinstance(x,list) and not x:return 'assert!('+field+'.is_empty());'
         wanted=('vec!'+json.dumps(x) if isinstance(x,list) else json.dumps(x));return 'assert_eq!('+field+','+wanted+');'
        if isinstance(x,list):return 'assert('+field+'.size()=='+str(len(x))+');'+''.join('assert('+field+'['+str(i)+']=='+str(e)+');' for i,e in enumerate(x))
        return 'assert('+field+'=='+json.dumps(x)+');'
       return ''.join(field_checks(n+'.'+k,x) for k,x in v.items())
      before,after=code.rsplit('}',1);checks=assertion('alpha',a)+assertion('beta',b)
      if name=='cpp':
       # Insert checks before the existing main return, not after unreachable code.
       before=before.replace('    return 0;',checks+'\n    return 0;');code='#include <cassert>\n'+before+'}'+after;extension='.cpp'
      else:code=before+'\n'+checks+'\n}'+after;extension='.rs'
     file=folder/('main'+extension);file.write_text(code)
     if name=='python':cmd=[g.RUNTIMES['python1'],str(file)]
     elif name=='go':cmd=[g.RUNTIMES['go'],'run',str(file)]
     else:
      binary=folder/'main.bin';compilecmd=(['rustc','--edition=2021',str(file),'-o',str(binary)] if name=='rust' else ['clang++','-std=c++20',str(file),'-o',str(binary)])
      q=subprocess.run(compilecmd,capture_output=True,text=True,timeout=30);(folder/'compile.txt').write_text(q.stdout+q.stderr)
      if q.returncode:row.update(status='compile_failure',stderr=q.stderr);raise RuntimeError('compile')
      cmd=[str(binary)]
     q=subprocess.run(cmd,capture_output=True,text=True,timeout=20);(folder/'stdout.txt').write_text(q.stdout);(folder/'stderr.txt').write_text(q.stderr)
     if q.returncode:row.update(status='runtime_failure',stderr=q.stderr)
     elif name in ('python','go'):
      wanted={'value':g.expected([a,b],name,0)}
      with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
       verify(label='composition',produced_json=q.stdout,expected_json=json.dumps(wanted),exclude_keys=())
       bad,changed=g.mutation(json.loads(q.stdout)['value'])
       if not changed:
        bad=['sequence',[['mapping',[[['str','a'],['bool',False]]]],['mapping',[[['str','a'],['bool',False]]]]]];changed=True
       assert changed
       try:verify(label='composition-negative',produced_json=json.dumps({'value':bad}),expected_json=json.dumps(wanted),exclude_keys=())
       except SystemExit:row['mutation_rejected']=True
       else:raise AssertionError('mutation accepted')
      row['status']='pass'
     else:row['status']='pass'
    except RuntimeError as e:
     if str(e)!='compile':row.update(status='exception',message=str(e))
    except SystemExit as e:row.update(status='mismatch',message=str(e))
    except Exception as e:row.update(status='exception',exception=type(e).__name__,message=str(e))
    (folder/'context.json').write_text(json.dumps(row,indent=2));rows.append(row);(root/'report.json').write_text(json.dumps(dict(seconds=time.monotonic()-start,rows=rows),indent=2))
print(json.dumps(dict(seconds=time.monotonic()-start,counts=Counter(x['status'] for x in rows))))
for r in rows:
 if r['status']!='pass':print(json.dumps(r))
