"""Minimize accepted-but-lossy PHP mappings and retain native witnesses."""
import json, subprocess, sys, time
from pathlib import Path
from hypothesis import find, seed, settings, strategies as st
from literalizer import InputFormat, literalize, literalize_call
from literalizer.exceptions import UnrepresentableInputError, UnrepresentableEmptyDictError
from literalizer.languages import Php, Lua
from scripts.bounded_command import bounded_command
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
trace=[]
def mismatch(data):
    source=json.dumps(data)
    try:
        literalize(source=source,input_format=InputFormat.JSON,language=Php())
    except (UnrepresentableInputError,UnrepresentableEmptyDictError):
        try:
            result=literalize_call(source=source,input_format=InputFormat.JSON,language=Php(),target_function='consume',parameter_names=('value',),per_element=False)
        except (UnrepresentableInputError,UnrepresentableEmptyDictError):return False
        trace.append({'data':data,'code':result.code});return True
    return False
settings_=settings(max_examples=100,deadline=None,database=None,derandomize=True)
witnesses=[find(st.dictionaries(st.text(alphabet='0123456789',min_size=1,max_size=4),st.text(max_size=4),min_size=1,max_size=3),mismatch,settings=settings_),find(st.one_of(st.dictionaries(st.just('a'),st.just({}),max_size=3),st.just({})),mismatch,settings=settings_)]
for i,data in enumerate(witnesses):
    r=literalize_call(source=json.dumps(data),input_format=InputFormat.JSON,language=Php(),target_function='consume',parameter_names=('value',),per_element=False)
    program='\n'.join((*r.preamble,*r.body_preamble))+'\nfunction consume($value) { echo json_encode(["is_list" => array_is_list($value), "first_key_type" => is_null(array_key_first($value)) ? null : gettype(array_key_first($value)), "encoded_value" => json_encode($value)]); }\n'+r.code
    p=out/f'{i}.php';p.write_text(program)
    command=bounded_command(args=['php',p],fixture=f'minimized-{i}',timeout_seconds=15)
    r=subprocess.run(command,capture_output=True,text=True,timeout=17)
    assert r.returncode==0,r.stderr
    (out/f'{i}.json').write_text(json.dumps({'data':data,'command':command,'stdout':r.stdout,'stderr':r.stderr},indent=2))
(out/'trace.json').write_text(json.dumps(trace,indent=2));(out/'witnesses.json').write_text(json.dumps(witnesses,indent=2));print(witnesses,len(trace))
