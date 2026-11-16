"""Separately audit declared rejection boundaries; no catch-all skips."""
import json
from pathlib import Path
import subprocess
import sys
import time
from discover import CONTEXTS, build, normalized, CONSUMERS
from literalizer import InputFormat
from literalizer.exceptions import UnrepresentableEmptyDictError, UnrepresentableInputError, UnrepresentableIntegerError, UnrepresentableStringError
from scripts.roundtrip_common import verify
from scripts.bounded_command import bounded_command

out=Path(sys.argv[1]); out.mkdir(exist_ok=False)
rows=[]; started=time.monotonic()
for ctx in CONTEXTS:
    boundaries=[('control-1','\x01',None if ctx.name=='php-multiline' else UnrepresentableStringError)]
    if ctx.backend=='php': boundaries += [('empty-mapping',{},UnrepresentableEmptyDictError),('numeric-key',{'0':'value'},UnrepresentableInputError),('integer-overflow',2**63,UnrepresentableIntegerError)]
    if ctx.backend=='javascript': boundaries += [('unsafe-integer',2**53+1,UnrepresentableIntegerError)]
    for label,data,exception in boundaries:
      for fmt in (InputFormat.JSON,InputFormat.YAML,InputFormat.TOML):
       for api in ('literal','new','existing','call'):
        row={'context':ctx.name,'input_format':fmt.name,'api':api,'boundary':label,'expected':None if exception is None else exception.__name__}
        try:
          source,program,logical=build(data,ctx,api,fmt)
        except Exception as exc:
          row['actual']=type(exc).__name__;row['message']=str(exc)
          row['pass']=exception is not None and type(exc) is exception
        else:
          if exception is not None: row.update(actual='accepted',pass_=False)
          else:
            p=out/f'{len(rows):03d}.php';p.write_text(program)
            command=bounded_command(args=['php',p],fixture=f'expected-safe-control-{len(rows)}',timeout_seconds=15)
            completed=subprocess.run(command,text=True,capture_output=True,timeout=17)
            (out/f'{len(rows):03d}-stdout.txt').write_text(completed.stdout)
            (out/f'{len(rows):03d}-stderr.txt').write_text(completed.stderr)
            assert completed.returncode==0,completed.stderr
            verify(label='safe-control',produced_json=completed.stdout,exclude_keys=(),expected_json=json.dumps({'value':normalized(logical,ctx)}))
            row.update(actual='native-pass');row['pass']=True
        rows.append(row)
        (out/'results.json').write_text(json.dumps(rows,indent=2))
summary={'controls':len(rows),'pass':sum(x.get('pass',False) for x in rows),'rejections':sum(x.get('pass',False) and x['expected'] is not None for x in rows),'native_programs':sum(x['actual']=='native-pass' for x in rows),'elapsed_seconds':time.monotonic()-started}
(out/'summary.json').write_text(json.dumps(summary,indent=2));print(summary)
assert summary['pass']==len(rows),[x for x in rows if not x.get('pass')]
