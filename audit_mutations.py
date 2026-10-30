import contextlib,io,json,pathlib
from collections import Counter
import generated_typed as g
from scripts.roundtrip_common import verify
root=pathlib.Path(__file__).parent;results=[]
def keys(v,path=''):
 if isinstance(v,list) and v and v[0]=='mapping':return [(path,[k for k,x in v[1]])]+[item for i,(k,x) in enumerate(v[1]) for item in keys(x,path+'/'+str(i))]
 if isinstance(v,list) and v and v[0] in ('sequence','set'):return [item for i,x in enumerate(v[1]) for item in keys(x,path+'/'+str(i))]
 return []

for dataset in ['typed-fixed','composition-combined-final']:
 report=json.loads((root/dataset/'report.json').read_text())
 for row in report['rows']:
  if row['status']!='pass' or dataset.startswith('composition') and row['backend'] not in ('python','go'):continue
  folder=(f"{row['seed']}-{row['index']}-{row['backend']}-{row['mode']}" if dataset=='typed-fixed' else f"{row['backend']}-{row['case']}-{row['reverse']}-{row['known']}")
  actual=json.loads((root/dataset/folder/'stdout.txt').read_text());bad,changed=g.mutation(actual['value']);assert changed
  assert keys(bad)==keys(actual['value'])
  expected=row.get('expected',actual)
  with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
   verify(label='positive',produced_json=json.dumps(actual),expected_json=json.dumps(expected),exclude_keys=())
   try:verify(label='typed-value-negative',produced_json=json.dumps({'value':bad}),expected_json=json.dumps(expected),exclude_keys=())
   except SystemExit:pass
   else:raise AssertionError('mutation accepted')
  target=root/dataset/folder/'value-mutation.json';target.write_text(json.dumps({'value':bad}))
  results.append(dict(dataset=dataset,folder=folder,keys_unchanged=True,mutation_rejected=True))
(root/'mutation-audit.json').write_text(json.dumps(results,indent=2));print(Counter(x['dataset'] for x in results))
