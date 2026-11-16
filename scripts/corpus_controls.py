"""Run the existing capability corpora through each pilot API/options context."""
import json, shutil, subprocess, sys, time
from pathlib import Path
from discover import CONTEXTS, build, normalized, mutation
from literalizer import InputFormat
from scripts.roundtrip_common import input_for_capabilities, verify
from scripts.bounded_command import bounded_command
out=Path(sys.argv[1]);out.mkdir(exist_ok=False);rows=[];started=time.monotonic()
for ctx in CONTEXTS:
    data=json.loads(input_for_capabilities(ctx.language.variant_metadata.round_trip_capabilities))
    exclusions={'python':(), 'javascript':('biginteger',),'php':('biginteger','empty_object')}[ctx.backend]
    for key in exclusions: del data[key]
    for fmt in (InputFormat.JSON,InputFormat.YAML,InputFormat.TOML):
      for api in ('literal','new','existing','call'):
        p=out/f'{len(rows):03d}';p.mkdir()
        source,program,logical=build(data,ctx,api,fmt)
        extension={'python':'py','javascript':'js','php':'php'}[ctx.backend]
        path=p/f'main.{extension}';path.write_text(program)
        (p/'source.txt').write_text(source)
        (p/'input.json').write_text(json.dumps(dict(data=data,context=ctx.name,api=api,input_format=fmt.name)))
        exe=sys.executable if ctx.backend=='python' else shutil.which('node' if ctx.backend=='javascript' else 'php')
        command=bounded_command(args=[exe,path],fixture=str(p/'input.json'),timeout_seconds=15)
        completed=subprocess.run(command,text=True,capture_output=True,timeout=17)
        expected=json.dumps({'value':normalized(logical,ctx)})
        (p/'command.json').write_text(json.dumps(command));(p/'expected.json').write_text(expected)
        (p/'stdout.txt').write_text(completed.stdout);(p/'stderr.txt').write_text(completed.stderr)
        row=dict(context=ctx.name,api=api,input_format=fmt.name,exclusions=exclusions,returncode=completed.returncode)
        rows.append(row);(out/'results.json').write_text(json.dumps(rows,indent=2))
        assert completed.returncode==0,(row,completed.stderr)
        verify(label=ctx.name,produced_json=completed.stdout,exclude_keys=(),expected_json=expected)
summary={'programs':len(rows),'elapsed_seconds':time.monotonic()-started}
(out/'summary.json').write_text(json.dumps(summary,indent=2));print(summary)
