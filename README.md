# Generated typed values and direct roots for #5493

Run the replay from the [pinned Literalizer tree](https://github.com/adamtheturtle/literalizer/tree/35b11399bc1b115a2a94971b0f8be6fa490df783). At that revision there are 65 registered languages, 62 `run_*_roundtrip.py` modules, and two retained Hypothesis integration modules, both focused on Python. The [earlier replay](https://github.com/adamtheturtle/literalizer/tree/e53380545ca7d7b3f5e9b682cff8f0e3f0764da1) covers mapping-root inputs, seven configurations, and the minimized PHP findings.

This pass uses seeds 5493, 6569, and 0 with Python, JavaScript, Lua, Ruby, and PHP. Each backend uses its native or default representation profile and an alternate profile with single-quoted strings, hex integers, scientific floats, base64 bytes, and multiline collections. The alternate Python profile uses lists. The other alternate profiles use ISO temporal strings. The input generator emits 15 values per seed, with sequences at depth three or less, small scalar counts, bounded strings and bytes, and explicit floating-point extremal values.

| Transport | Native program executions |
| --- | ---: |
| JSON direct roots | 840 |
| YAML direct roots | 1,200 |
| TOML selected roots | 480 |
| Total | 2,520 |

Each backend passed 504 programs. API counts are 750 bare expressions, 270 new bindings, 990 whole-value calls, and 510 per-element calls. Byte, date, datetime, and nested typed roots are represented in the YAML corpus. TOML selects its root via `input_root_key`.

The observers check native types and sequence widths before transport. Floats use binary64 bit patterns, preserving signed zero and subnormals. Dynamic temporal representations are compared against the expected calendar value, UTC instant, or epoch conversion. Binary values are checked as native bytes or against the selected hex or base64 encoding. Twenty deliberately changed native values were detected, and twelve expected API rejections were confirmed.

The initial generator produced JSON surrogate escapes inside YAML strings, and the initial Ruby observer referenced `Date` for ordinary scalars before the runtime defined that constant. The final run uses valid YAML Unicode and a guarded Ruby date observer. These were adapter failures. All admitted inputs passed on the final replay.

The sample covers the declared runtimes, two profiles, and scalar and sequence roots. The earlier archive covers mapping roots. Multi-argument row evaluation is covered in the existing Python regressions. Other runtimes, Lua tables with null elements, native invocation APIs, and other representation options remain outside this sample.

## Replay

Use a dev environment at the pinned checkout and set `archive_dir` to this archive's absolute path.

```sh
uv sync --group=dev
PYTHONPATH="$PWD/src:$PWD" timeout 250 .venv/bin/python "$archive_dir/replay.py" /tmp/literalizer-5493-mismatches.json
```

The observed runtimes were CPython 3.15.0, Node 26.13.1, Lua 5.5.1, Ruby 2.6.10, and PHP 8.5.12. Each runtime invocation is bounded to eight seconds, with a 240-second overall controller budget. The final run took 101.413 seconds. See `results.txt` for the execution breakdown and `mismatches.json` for the result of the mismatch check.
