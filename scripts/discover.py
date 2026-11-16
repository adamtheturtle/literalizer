"""Bounded seeded semantic discovery; run from the audited source checkout."""
import argparse
import contextlib
import dataclasses
import enum
import io
import json
import math
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time

import hypothesis
import hashlib
from hypothesis import Phase, given, seed, settings, strategies as st
import tomlkit
from ruamel.yaml import YAML

from literalizer import CollectionLayout, ExistingVariable, InputFormat, NewVariable, literalize, literalize_call
from literalizer.languages import Python, JavaScript, Php
from scripts.bounded_command import bounded_command
from scripts.roundtrip_common import verify

HERE = Path(__file__).resolve().parent

# The consumers preserve concrete collection kinds as well as logical values.
CONSUMERS = {
'python': r'''
import json as _json, math as _math
def probe_norm(v):
    if v is None: return ['null']
    if isinstance(v, bool): return ['bool', v]
    if isinstance(v, str): return ['string', v]
    if isinstance(v, (int, float)):
        return ['number', '-zero' if _math.copysign(1, v) < 0 else '+zero'] if v == 0 else ['number', v]
    if isinstance(v, dict): return ['dict', [[k, probe_norm(v[k])] for k in sorted(v)]]
    if isinstance(v, (list, tuple)): return [type(v).__name__, [probe_norm(x) for x in v]]
    raise TypeError(type(v))
print(_json.dumps({'value': probe_norm(probe_value)}, ensure_ascii=True, allow_nan=False))
''',
'javascript': r'''
function probeNorm(v) {
    if (v === null) return ['null'];
    if (typeof v === 'boolean') return ['bool', v];
    if (typeof v === 'string') return ['string', v];
    if (typeof v === 'number') return ['number', v === 0 ? (Object.is(v, -0) ? '-zero' : '+zero') : v];
    if (Array.isArray(v)) return ['array', v.map(probeNorm)];
    if (v instanceof Map) return ['map', [...v.keys()].sort().map(k => [k, probeNorm(v.get(k))])];
    if (typeof v === 'object') return ['object', Object.keys(v).sort().map(k => [k, probeNorm(v[k])])];
    throw Error('unexpected value');
}
process.stdout.write(JSON.stringify({value: probeNorm(probe_value)}));
''',
'php': r'''
function probe_norm($v) {
    if (is_null($v)) return ['null'];
    if (is_bool($v)) return ['bool', $v];
    if (is_string($v)) return ['string', $v];
    if (is_int($v) || is_float($v)) {
        if ($v == 0) return ['number', is_float($v) && pack('d', $v) === pack('d', -0.0) ? '-zero' : '+zero'];
        return ['number', $v];
    }
    if (is_array($v) && array_is_list($v)) return ['array', array_map('probe_norm', $v)];
    if (is_array($v)) {
        ksort($v, SORT_STRING); $pairs = [];
        foreach ($v as $k => $x) { $pairs[] = [$k, probe_norm($x)]; }
        return ['mapping', $pairs];
    }
    throw new Exception('unexpected value');
}
echo json_encode(['value' => probe_norm($probe_value)], JSON_THROW_ON_ERROR | JSON_PRESERVE_ZERO_FRACTION);
''',
}

@dataclasses.dataclass(frozen=True)
class Context:
    name: str
    backend: str
    language: object
    layout: CollectionLayout

CONTEXTS = [
    Context('python-tuple', 'python', Python(), CollectionLayout.COMPACT),
    Context('python-list', 'python', Python(sequence_format=Python.sequence_formats.LIST, variable_type_hints=Python.variable_type_hints_formats.SAFE, string_format=Python.string_formats.SINGLE, float_format=Python.float_formats.SCIENTIFIC, integer_format=Python.integer_formats.HEX), CollectionLayout.MULTILINE),
    Context('javascript-object', 'javascript', JavaScript(), CollectionLayout.COMPACT),
    Context('javascript-map', 'javascript', JavaScript(dict_format=JavaScript.dict_formats.MAP, declaration_style=JavaScript.declaration_styles.LET, call_style=JavaScript.call_styles.POSITIONAL, string_format=JavaScript.string_formats.MULTILINE, float_format=JavaScript.float_formats.FIXED, integer_format=JavaScript.integer_formats.HEX), CollectionLayout.MULTILINE),
    Context('php-double', 'php', Php(), CollectionLayout.COMPACT),
    Context('php-single', 'php', Php(string_format=Php.string_formats.SINGLE, float_format=Php.float_formats.SCIENTIFIC, integer_format=Php.integer_formats.HEX, variable_type_hints=Php.variable_type_hints_formats.SAFE), CollectionLayout.MULTILINE),
    Context('php-multiline', 'php', Php(string_format=Php.string_formats.MULTILINE, float_format=Php.float_formats.FIXED, integer_format=Php.integer_formats.BINARY), CollectionLayout.MULTILINE),
]


def normalized(v, ctx):
    if v is None: return ['null']
    if isinstance(v, bool): return ['bool', v]
    if isinstance(v, str): return ['string', v]
    if isinstance(v, (int, float)):
        return ['number', '-zero' if math.copysign(1, v) < 0 else '+zero'] if v == 0 else ['number', v]
    if isinstance(v, list):
        kind = ('tuple' if ctx.language.sequence_format is Python.sequence_formats.TUPLE else 'list') if ctx.backend == 'python' else 'array'
        return [kind, [normalized(x, ctx) for x in v]]
    if isinstance(v, dict):
        kind = 'dict' if ctx.backend == 'python' else 'mapping' if ctx.backend == 'php' else 'map' if ctx.language.dict_format is JavaScript.dict_formats.MAP else 'object'
        return [kind, [[k, normalized(v[k], ctx)] for k in sorted(v)]]
    raise TypeError(type(v))

TEXT = st.text(alphabet='abXYZ09 _-\n\r\t\x00\"\'\\${}`é中🙂', max_size=12)
# ASCII keys make the independent ordering identical in all three consumers.
KEY = st.one_of(st.sampled_from(['', '__proto__', 'constructor', 'value', 'a', 'z', '${x}', '01']), st.text(alphabet='abcXYZ_-$', min_size=1, max_size=8))
SCALAR = st.one_of(st.booleans(), st.integers(min_value=-1000000, max_value=1000000), st.floats(min_value=-1000000, max_value=1000000, allow_nan=False, allow_infinity=False), st.sampled_from([-0.0, 0.0, 1.0, 0.1, 1e-100]), TEXT)


def values(depth, php, nullable):
    scalar = st.one_of(SCALAR, st.none()) if nullable else SCALAR
    if depth == 0: return scalar
    children = values(depth - 1, php, nullable)
    return st.one_of(scalar, st.lists(children, max_size=3), st.dictionaries(KEY, children, min_size=1 if php else 0, max_size=3))


def serialize(data, fmt):
    if fmt is InputFormat.JSON: return json.dumps(data, ensure_ascii=True, allow_nan=False)
    if fmt is InputFormat.TOML: return tomlkit.dumps(data)
    stream = io.StringIO()
    YAML(typ='safe', pure=True).dump(data, stream)
    return stream.getvalue()


def build(data, ctx, api, fmt):
    # A wrapper gives TOML its required mapping root while preserving arbitrary
    # scalars, arrays and dictionaries as the tested value.
    source_data = {'value': data, 'negative_zero': -0.0, 'false': False, 'true': True}
    source = serialize(source_data, fmt)
    kw = dict(source=source, input_format=fmt, language=ctx.language, collection_layout=ctx.layout)
    prefix = ''
    if api == 'call':
        # A positional call receives the wrapper mapping as a single argument.
        # Object/keyword calls receive its named value parameter instead.
        positional = ctx.backend == 'javascript' and ctx.language.call_style is JavaScript.call_styles.POSITIONAL
        call_data = source_data
        call_source = serialize(call_data, fmt) if fmt is not InputFormat.TOML else tomlkit.dumps({'row': call_data})
        result = literalize_call(**(kw | dict(source=call_source)), input_root_key='row' if fmt is InputFormat.TOML else None, target_function='probe_accept', parameter_names=('value',), per_element=False)
        prefix = {'python':'def probe_accept(value):\n    global probe_value\n    probe_value = value\n', 'javascript':('function probe_accept(value) { probe_value = value; }\n' if positional else 'function probe_accept({value}) { probe_value = value; }\n') + 'let probe_value;\n', 'php':'function probe_accept($value) { global $probe_value; $probe_value = $value; }\n'}[ctx.backend]
        code = result.code
    else:
        form = NewVariable(name='probe_value', modifiers=frozenset()) if api == 'new' else ExistingVariable(name='probe_value') if api == 'existing' else None
        result = literalize(**kw, variable_form=form)
        code = result.code
        if api == 'literal':
            code = {'python':'probe_value = ', 'javascript':'let probe_value = ', 'php':'$probe_value = '}[ctx.backend] + code + (';' if ctx.backend != 'python' else '')
        if api == 'existing' and ctx.backend == 'javascript': prefix = 'let probe_value;\n'
    preamble = '\n'.join((*result.preamble, *result.body_preamble))
    return source, preamble + '\n' + prefix + code + '\n' + CONSUMERS[ctx.backend], source_data


def mutation(v):
    tag = v[0]
    if tag == 'bool': return ['number', int(v[1])]
    if tag == 'number':
        return ['number', '+zero' if v[1] == '-zero' else '-zero' if v[1] == '+zero' else v[1] + 1]
    if tag in ('list', 'tuple', 'array'):
        for i, x in enumerate(v[1]):
            changed = mutation(x)
            if changed is not None: return [tag, v[1][:i] + [changed] + v[1][i+1:]]
    if tag in ('dict', 'object', 'map', 'mapping'):
        for i, (key, x) in enumerate(v[1]):
            changed = mutation(x)
            if changed is not None: return [tag, v[1][:i] + [[key, changed]] + v[1][i+1:]]
    return None


class DiscoveryFailure(Exception): pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=5493)
    parser.add_argument('--examples', type=int, default=12)
    parser.add_argument('--budget-seconds', type=float, default=420)
    parser.add_argument('--context', action='append')
    parser.add_argument('--replay', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    records = []
    tools = {'python':sys.executable, 'javascript':shutil.which('node'), 'php':shutil.which('php')}
    versions = {}
    for backend, exe in tools.items():
        if exe is None: raise RuntimeError(f'missing {backend}')
        p = subprocess.run([exe, '--version'], capture_output=True, text=True, timeout=5)
        versions[backend] = dict(path=exe, stdout=p.stdout, stderr=p.stderr, returncode=p.returncode)
    metadata = dict(seed=args.seed, examples=args.examples, budget_seconds=args.budget_seconds, hypothesis=hypothesis.__version__, versions=versions, controller=sys.version, source_head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True,timeout=5).stdout.strip(), limits=dict(depth=3,width=3,string_length=12,integer_range=[-1000000,1000000],float_range=[-1000000,1000000]), contexts=[dict(name=c.name, backend=c.backend, layout=c.layout.value, options={f.name:str(getattr(c.language,f.name)) for f in dataclasses.fields(c.language)}) for c in CONTEXTS])
    metadata['source_hashes'] = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('src').rglob('*.py'))}
    metadata['controller_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    metadata['working_tree_diff'] = subprocess.run(['git','diff','--','src'],capture_output=True,text=True,check=True,timeout=5).stdout
    (args.output/'metadata.json').write_text(json.dumps(metadata,indent=2))

    def run(data, ctx, api, fmt):
        remaining = args.budget_seconds - (time.monotonic() - started)
        if remaining <= 0: raise TimeoutError(f'overall budget exhausted before {ctx.name}/{api}/{fmt.name}; last={records[-1] if records else None}')
        case = args.output/f'{len(records):06d}'
        case.mkdir()
        config = dict(data=data, context=ctx.name, api=api, input_format=fmt.name)
        (case/'input.json').write_text(json.dumps(config,ensure_ascii=True,indent=2))
        rec = dict(case=case.name, context=ctx.name, api=api, input_format=fmt.name, classification='rendering')
        records.append(rec)
        (args.output/'active.json').write_text(json.dumps(rec))
        try:
            source, program, logical = build(data,ctx,api,fmt)
            (case/'source.txt').write_text(source)
            extension = {'python':'py','javascript':'js','php':'php'}[ctx.backend]
            path = case/f'main.{extension}'
            path.write_text(program)
            expected = json.dumps({'value':normalized(logical,ctx)},ensure_ascii=True)
            (case/'expected.json').write_text(expected)
            argv = [tools[ctx.backend], str(path)]
            command = bounded_command(args=argv, fixture=str(case/'input.json'), timeout_seconds=min(15,remaining))
            (case/'command.json').write_text(json.dumps(command))
            (case/'reproduce.txt').write_text('PYTHONPATH=.:src '+shlex.join([sys.executable,str(Path(__file__).resolve()),'--output',str(case)+'-replay','--replay',str(case/'input.json')])+'\n'+shlex.join(command)+'\n')
            p = subprocess.run(command, capture_output=True, text=True, timeout=min(17,remaining+2))
            (case/'stdout.txt').write_text(p.stdout)
            (case/'stderr.txt').write_text(p.stderr)
            rec['returncode'] = p.returncode
            if p.returncode:
                rec['classification'] = 'timeout' if p.returncode in (124,137) else 'consumer-or-renderer-runtime'
                raise DiscoveryFailure(str(case))
            try:
                verify(label=ctx.name, produced_json=p.stdout, exclude_keys=(), expected_json=expected)
            except SystemExit as exc:
                rec['classification'] = 'semantic-mismatch'
                raise DiscoveryFailure(str(case)) from exc
            # Mutate a VALUE tag, never the mapping key slot: each record has
            # an outer wrapper and the candidate explicitly descends its value.
            got = json.loads(p.stdout)
            changed = mutation(got['value'])
            if changed is not None:
                (case/'mutation.json').write_text(json.dumps({'value':changed}))
                with contextlib.redirect_stderr(io.StringIO()):
                    try: verify(label='mutation',produced_json=json.dumps({'value':changed}),exclude_keys=(),expected_json=expected)
                    except SystemExit: rec['mutation_rejected'] = True
                    else: raise AssertionError('oracle accepted mutation')
            rec['classification'] = 'pass'
        except DiscoveryFailure: raise
        except subprocess.TimeoutExpired as exc:
            rec['classification']='timeout'; rec['error']=repr(exc); raise DiscoveryFailure(str(case)) from exc
        except Exception as exc:
            rec['classification']='producer-or-adapter-error'; rec['error']=repr(exc); raise DiscoveryFailure(str(case)) from exc
        finally:
            (case/'result.json').write_text(json.dumps(rec,indent=2))
            (args.output/'results.json').write_text(json.dumps(records,indent=2))

    failures=[]
    selected=[c for c in CONTEXTS if not args.context or c.name in args.context]
    if args.replay:
        replay=json.loads(args.replay.read_text())
        run(replay['data'],next(c for c in CONTEXTS if c.name==replay['context']),replay['api'],InputFormat[replay['input_format']])
    else:
        for ctx in selected:
            for fmt in (InputFormat.JSON,InputFormat.YAML,InputFormat.TOML):
                strategy=values(3,ctx.backend=='php',fmt is not InputFormat.TOML)
                for api in ('literal','new','existing','call'):
                    @seed(args.seed)
                    @settings(max_examples=args.examples,deadline=None,database=None,phases=(Phase.generate,Phase.shrink),report_multiple_bugs=False)
                    @given(strategy)
                    def probe(data): run(data,ctx,api,fmt)
                    try: probe()
                    except DiscoveryFailure as exc:
                        failures.append(dict(context=ctx.name, api=api, input_format=fmt.name,last_case=records[-1]['case'],error=str(exc)))
                    print(ctx.name,fmt.name,api, 'fail' if failures and failures[-1].get('last_case')==records[-1]['case'] else 'pass',len(records),flush=True)
    summary=dict(elapsed_seconds=time.monotonic()-started,attempts=len(records),classifications={k:sum(r['classification']==k for r in records) for k in sorted({r['classification'] for r in records})},mutation_controls=sum(r.get('mutation_rejected',False) for r in records),failures=failures)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    return bool(failures)

if __name__=='__main__': sys.exit(main())
