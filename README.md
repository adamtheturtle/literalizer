# Generated per-row call roundtrips

This archive records the bounded discovery pass for [Literalizer #7218](https://github.com/adamtheturtle/literalizer/issues/7218) against [source commit `5ab5f4eb6898c57a0fcd662ace570aa4eeb564bf`](https://github.com/adamtheturtle/literalizer/tree/5ab5f4eb6898c57a0fcd662ace570aa4eeb564bf). It builds on the Python and JavaScript profiles and typed comparison from the [#5493 discovery archive](https://github.com/adamtheturtle/literalizer/tree/e53380545ca7d7b3f5e9b682cff8f0e3f0764da1).

| Profile | Options |
| --- | --- |
| Python tuple | Default tuple and keyword calls, compact layout |
| Python list | List, safe hints, single-quoted strings, scientific floats, hex integers, multiline layout |
| JavaScript object | Default object mappings and object-style calls, compact layout |
| JavaScript Map | Map, let, positional calls, multiline strings, fixed floats, hex integers, multiline layout |

Each profile renders JSON and YAML inputs with `literalize_call(per_element=True)`. Examples have two to four distinct rows of a uniform arity from two to four. Each row begins with a generated unique string identifier. Remaining arguments can be null, booleans, bounded integers and finite floats, strings, or nested lists and string-keyed mappings. The generator limits nesting to depth three, container width to three, string length to twelve, and the numerical range to ±1,000,000.

A native consumer records every invocation in order, checks argument arity or names, and tags native values before JSON transport. The shared verifier compares the resulting ordered calls with the expected values derived from the generated rows. Tags preserve booleans, signed zero, sequence kinds, and mapping kinds. Equal integer and float values compare numerically. Each passing program also supplies three negative controls using the recorded output, swapping the first two rows, swapping the first two arguments of the first row, and dropping the first row.

## Results

| Seed | Native programs | Calls verified | Mutations rejected | Seconds |
| --- | ---: | ---: | ---: | ---: |
| 5493 | 192 | 608 | 576 | 38.471 |
| 6569 | 192 | 608 | 576 | 38.934 |
| 0 | 192 | 528 | 576 | 38.239 |
| **Total** | **576** | **1,744** | **1,728** | |

Each profile and format pair ran 72 native programs. Seeded input draws repeat across profiles and formats. The archive contains observed nulls, booleans, both zero signs, and every configured sequence and mapping kind. All programs passed and every mutation was rejected. The run found no defect requiring a deterministic regression. The existing call-error and roundtrip-mismatch tests passed (28 tests).

The evidence archive SHA-256 is `94087513a82c1f19c96447e89523b4463e2453ef9073c4871f68789e1a2c9671`.

## Reproduce

From a checkout at the source commit, install the pinned environment and put Node and GNU timeout on PATH. The recorded tools were Python 3.14.8, Node 26.13.1, and Hypothesis 6.170.15. Each run allows 24 examples per profile and format, a 10-second cap for subprocesses, and a 120-second overall deadline.

```sh
uvx uv@0.13.0 sync --locked --group dev --python 3.14
for seed in 5493 6569 0; do
    PYTHONPATH=.:src scripts/run-bounded.sh row-discovery --signal=KILL 120s \
        .venv/bin/python /path/to/archive/discover_rows.py \
        --output "/fresh/path/seed-$seed" --seed "$seed" --examples 24 \
        --budget-seconds 120 --child-seconds 10
done
```

After extracting `evidence.tar.gz`, replay a specific input through the same renderer and oracle.

```sh
PYTHONPATH=.:src scripts/run-bounded.sh row-replay --signal=KILL 120s \
    .venv/bin/python /path/to/archive/discover_rows.py \
    --output /fresh/path/replay \
    --replay /path/to/evidence/literalizer-7218-final-5493/0000/input.json
```

Each run retains the tool versions, complete profile options, seed, commands, and results. Each case retains the generated input, serialized source, native program, expected and observed calls, and the three rejected payloads. The recorded per-case shell commands reflect the original checkout paths.
