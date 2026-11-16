"""Native reference-only PHP mappings remain mappings, with and without hints."""
import json, subprocess, sys, time
from pathlib import Path
import tomlkit
from discover import CONTEXTS, serialize
from literalizer import InputFormat,literalize_call
from scripts.bounded_command import bounded_command
out=Path(sys.argv[1]);out.mkdir(exist_ok=False);rows=[];started=time.monotonic()
for ctx in (c for c in CONTEXTS if c.backend=='php'):
 for fmt in (InputFormat.JSON,InputFormat.YAML,InputFormat.TOML):
  for per_element in (False,True):
   for hints in (None,{'item':42}):
    value={'field':{'$ref':'item'}}; data=[[value]] if per_element else value
    source=tomlkit.dumps({'rows':data}) if fmt is InputFormat.TOML and per_element else serialize(data,fmt)
    result=literalize_call(source=source,input_format=fmt,input_root_key='rows' if fmt is InputFormat.TOML and per_element else None,language=ctx.language,target_function='consume',parameter_names=('value',),per_element=per_element,ref_key='$ref',ref_values=hints,collection_layout=ctx.layout)
    program='\n'.join((*result.preamble,*result.body_preamble))+'''\n$item = 42;
function consume($value) {
    if (array_is_list($value) || array_keys($value) !== ['field'] || $value['field'] !== 42) throw new Exception('reference-only mapping changed');
    echo json_encode(['reference_value' => $value['field'], 'is_list' => array_is_list($value)]);
}
'''+result.code
    case=out/f'{len(rows):03d}';case.mkdir();p=case/'main.php';p.write_text(program)
    (case/'source.txt').write_text(source)
    command=bounded_command(args=['php',p],fixture=str(case/'source.txt'),timeout_seconds=15)
    r=subprocess.run(command,capture_output=True,text=True,timeout=17)
    row=dict(context=ctx.name,input_format=fmt.name,per_element=per_element,hints=hints,command=command,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr)
    rows.append(row);(out/'results.json').write_text(json.dumps(rows,indent=2))
    assert r.returncode==0,row
    assert json.loads(r.stdout)=={'reference_value':42,'is_list':False},row
summary={'native_programs':len(rows),'elapsed_seconds':time.monotonic()-started}
(out/'summary.json').write_text(json.dumps(summary,indent=2));print(summary)
