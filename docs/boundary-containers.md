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

The hard limits are 400 value/shape cases per lane, depth 6, 60 seconds per
compiler/runtime subprocess, 8 minutes per outer command and 20 minutes
per hosted job. Six matrix cells cap total active hosted job time at 120
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
