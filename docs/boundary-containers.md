# Boundary propagation discovery (#5492)

This opt-in experiment compares the existing capability-selected roundtrip
corpus with a bounded container expansion on the same revision and runner.
It does not add an expansion to ordinary pytest or compiler CI.

The pre-expansion audit and capability inventory are published in
[issue #5492](https://github.com/adamtheturtle/literalizer/issues/5492#issuecomment-6192259189).
The existing scalar corpus covers signed 64-bit endpoints, negative zero,
DBL_MAX, ordinary Unicode, and generic empty/nested collections. It is
null-free. Existing goldens cover particular epoch/container regressions;
they do not establish semantic preservation for this entire shape set.

## Selected contracts

| Lane | Contract | Integer domain |
| --- | --- | --- |
| Python | LIST, EPOCH | arbitrary precision |
| JavaScript | Number, EPOCH | safe integers: ±(2^53 − 1) |
| Go | default maps/slices, EPOCH | −2^63 through 2^64 − 1 |
| Go RECORD | native records, EPOCH | −2^63 through 2^64 − 1 |
| C# | ARRAY, EPOCH | −2^63 through 2^64 − 1 |
| C# RECORD | native records, EPOCH | −2^63 through 2^64 − 1 |

`scripts/boundary_containers.py` lists every selected value explicitly:
signed 32/64-bit endpoints and immediate neighbors; unsigned 32/64-bit
maxima and neighbors; safe-integer endpoints; binary64 signed zero,
smallest subnormal/normal, neighboring values around 1 and 2^53, and
maximum finite value; composed/decomposed/non-BMP Unicode, escaping,
interpolation, line separators, NUL and controls; datetimes around the
epoch and ±2^31 seconds; and empty/all-null/populated lists and maps.

Each supported value appears in a singleton list, a map field, a record
inside a list, list/map/list nesting, beside an empty sibling list, and
beside a string forcing a heterogeneous carrier. Selected smaller integer
families additionally appear beside a wider integer. This deliberately
bounded representative set is not an exhaustive backend/option matrix.

The capability metadata gates raw C0 controls. Unsupported controls must
raise `UnrepresentableStringError` both alone and in all six shapes.
Go RECORD explicitly rejects dictionary-list/empty-list siblings with
`UnrepresentableInputError`; those three combinations are error checks.
Finite-domain integers immediately outside the target range must raise
`UnrepresentableIntegerError`, again alone and in all six shapes.
Python's integer range in the selection object exceeds every sampled
integer; it is a corpus selection bound, not a representability limit.

## Oracle and bounds

Runtime observers walk native maps, arrays and records, tag integer
versus floating runtime types, and encode floats as exact binary64 bits
*before* JSON serialization. Strings and collection shapes are compared
recursively. JavaScript intentionally uses Number observations for all
numbers. EPOCH expectations use integer datetime arithmetic, independently
of the renderer. Native record field casing is normalized; corpus keys
use only lowercase letters and digits. Baseline keys have underscores
removed before rendering to avoid testing field-name conversion.

A baseline warm-up runs before both measured commands so compiler caches
start warm. C# programs select SDK 8.0.426 through `global.json`, not the
latest SDK preinstalled on the runner.

The hard limits are 400 value/shape cases per lane, depth 6, 60 seconds per
compiler/runtime subprocess, 8 minutes per outer command and 15 minutes
per hosted job. Six matrix cells cap total active hosted job time at 90
runner-minutes including setup. No random generation or automatic
subprocess-heavy minimization runs in CI. The normal baseline exclusions
for the `biginteger` field apply to JavaScript, Go and C#.

Run the manual **Boundary container discovery** workflow, or locally:

```sh
uv run --group dev python -m scripts.boundary_containers \
  --target go --mode expanded --output /tmp/boundary-go
```

Use `--mode baseline` for the matched existing corpus; use, for example,
`--case float0nested` to isolate a failing value/shape. Artifacts include
the exact input, generated source, runtime stdout/stderr, semantic
expectations on mismatch, revision/tool versions and timed verdicts.
GitHub step start/end timestamps measure active work separately from
queue time; the script reports render/compile/run/compare time without
interpreter import and dependency setup. A failed expanded batch is a
diagnostic cost, not a successful-suite forecast.

Any discovered failure must be classified against the chosen contract.
Publish minimal library defects separately, check existing issue coverage,
and retain deterministic manifest-owned goldens. Keep harness failures,
tool installation failures, documented limitations and CI costs separate.


## Results: October 15, 2026

Production source was frozen at main `00f99ec9af`. The final matched
[GitHub experiment](https://github.com/adamtheturtle/literalizer/actions/runs/38738902541)
used discovery revision `489da908c58b49424374e8489ef0fb4b75cacc33`
on Ubuntu 24.04, Python 3.14.8, Go 1.24.13, Node 22.23.3 and .NET SDK
8.0.426 (C# 10, net8.0). All six baseline corpora passed.

| Lane | Baseline cases | Expanded cases | Baseline active seconds | Expanded active seconds | Expanded verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| Python | 23 | 336 | 3 | 4 | semantic pass |
| JavaScript | 28 | 294 | 4 | 4 | semantic pass |
| Go | 32 | 336 | 3 | 4 | semantic pass |
| Go RECORD | 32 | 333 | 3 | 4 | semantic pass |
| C# | 32 | 336 | 5 | 6 | compiler failure, #5660 |
| C# RECORD | 32 | 336 | 4 | 4 | compiler failure, #5661 |
| Total | 179 | 1,971 | 22 | 26 | four passing lanes, two failing lanes |

Active seconds use GitHub step timestamps, with one-second resolution;
queue time is excluded. The expanded work costs 0.43 runner-minutes
versus 0.37 for the baseline. Complete jobs, including setup and warm-up,
used 5.58 runner-minutes. All three diagnostic attempts together used
17.12 runner-minutes, below the 120-minute overall discovery budget.
The first attempt mixed cold and warm compiler caches; the second exposed
that installing an SDK does not select it on a runner with a newer SDK.
Neither is used for the final cost comparison.

This is one matched sample of a **failing diagnostic batch**, not a cost
forecast for a repaired green suite or the full golden matrix. Compilation
stops before runtime checks in the two C# batches. Warm compiler/runtime
batches remained below two seconds of core script execution; interpreter
imports account for much of the active command time. No fixture reached
its deadline. The JSON runtime reports and tool/version records are in
the linked run's six `boundary-*` artifacts.

Two library defects were minimized and filed separately:

| Defect | Retained focused cases | Compiler evidence |
| --- | --- | --- |
| [#5660](https://github.com/adamtheturtle/literalizer/issues/5660): default C# nested map arrays infer `int[]` for wide EPOCH values | `epoch0nested`, `epoch8nested` | `CS0029`, `long[]` cannot convert to `int[]` |
| [#5661](https://github.com/adamtheturtle/literalizer/issues/5661): C# RECORD empty siblings infer dictionary arrays beside native record arrays | `collection4empty`, `collection6empty` | `CS0826` and `CS0029` |

Each retained case was compiled individually with SDK 8.0.426. Removing
those two cases from each C# batch locally allowed the other 334 cases
in each lane to compile and pass the typed semantic oracle, with no
further mismatches. In total, 1,967 expanded value/shape combinations
were semantically verified; four have focused compiler failures.
The named cases remain deterministic opt-in regression checks and still
fail while their separate defect reports are open. They are not promoted
into passing ordinary golden/compiler CI before their defects are fixed.

Documented limitations were checked separately: 115 scalar/container
rejections across the six lanes, for outside-domain integers, unsupported
raw C0 controls, and Go RECORD's three empty-sibling combinations. These
are explicit errors, not silently skipped semantic inputs. No new
roundtrip-harness defect was filed. Observer field casing and local SDK
availability were corrected before the final experiment; the .NET SDK
selection problem was also corrected in the workflow and runner.

Validation of the retained tooling included all four static type checkers,
Ruff, Pylint, workflow security checks, and the nine existing capability/
orphan-golden tests. Production library code and the existing golden
corpus were unchanged by this discovery exercise.
