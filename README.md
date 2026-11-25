# Rendering invariants and option-pair discovery

These bounded replays cover [#5491](https://github.com/adamtheturtle/literalizer/issues/5491) and [#5490](https://github.com/adamtheturtle/literalizer/issues/5490) on [Literalizer 35b11399](https://github.com/adamtheturtle/literalizer/tree/35b11399bc1b115a2a94971b0f8be6fa490df783). The native observers come from the [typed roundtrip replay](https://github.com/adamtheturtle/literalizer/tree/b0dc4eba6ce0e31b82686622270ab76b281e3a00). The observed tools were CPython 3.15.0, Node 26.13.1, Lua 5.5.1, Ruby 2.6.10, and PHP 8.5.12 on macOS arm64. Each phase has a 240-second controller budget and an eight-second runtime deadline per program.

## Rendering invariants

425 positive native programs passed in 18.002 seconds. The sample exercises empty and populated siblings, null-only siblings where the runtime preserves the slots, mixed typed sequences, independent binding and field renames, and nested repeated references. It tests both sibling orders for the direct and nested references, with original and converted reference spellings and with or without inference hints. Three Python record field controls compile and read back independently renamed dataclass fields. A reserved Python record field raises its documented error.

Python tuples retain identity and mutable Python lists share mutation. JavaScript arrays, Lua tables and Ruby arrays retain shared identity and expose mutation through either reference. PHP arrays retain equal values with copy-on-write isolation. Five deliberately changed identity or ownership relations were detected after the native observer confirmed the same initial values. Ruby's API-materialized reference rejection was exercised in four configurations. Four Lua null-slot configurations were excluded because native tables cannot preserve those positions. The Ruby caller-scaffold checks passed for independently rendered declarations and calls.

## Pairwise option interactions

The candidate space covers string quotes, integer and float formats, byte encodings, collection layout, new and existing call-result bindings, whole-value and row calls, and direct, unhinted, or hinted reference inputs. Python adds list or tuple representation and type hints. JavaScript adds declaration style. JavaScript, Lua, Ruby, and PHP add native or ISO temporal representations. The positive sample excludes reassignment of a caller's JavaScript constant. The native control demonstrates that error.

| Backend | Candidate configurations | Admitted configurations | Supported pairs | Selected configurations | Pairs absent from the manifest projection |
| --- | ---: | ---: | ---: | ---: | ---: |
| Python | 1,536 | 1,536 | 198 | 10 | 59 |
| JavaScript | 1,536 | 1,152 | 197 | 10 | 73 |
| Lua | 768 | 768 | 160 | 10 | 63 |
| Ruby | 768 | 768 | 160 | 10 | 65 |
| PHP | 768 | 768 | 160 | 10 | 63 |

The selected profiles cover all 875 admitted pairs across the five backends, plus a hinted-reference, existing-binding, row-call combination in each backend. All 150 primary programs passed in a 9.319-second run. Each selected profile consumed a typed sequence, a nested sequence, and a scalar. Five wrong reference values were detected. JavaScript rejected sub-millisecond input in its native Date representation, and its ISO option preserved those same microseconds.

The inventory projects current literal variant builders, call renderings and reference renderings onto the declared factors. Its counts describe configuration contexts, while the new replay provides native semantic evidence for these particular inputs. Other representation options and backends are outside this declared matrix. The earlier issue records retain Python and Go sweeps and the smaller Lua and Perl interaction tests.

## Reproduce

From a development environment at the pinned source checkout, set `archive_dir` to this archive's absolute path. Each command writes the sampled scope and results, and a failure reports the backend, configuration and native diagnostic.

```sh
uv sync --group=dev
PYTHONPATH="$PWD/src:$PWD" timeout 250 .venv/bin/python "$archive_dir/replay.py" invariants /tmp/invariants.json
PYTHONPATH="$PWD/src:$PWD" timeout 250 .venv/bin/python "$archive_dir/replay.py" pairwise /tmp/pairwise.json
```
