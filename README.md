# Bounded generated-input and API discovery — 2026-11-16

This is an immutable research archive for [#5493](https://github.com/adamtheturtle/literalizer/issues/5493), separate from the production [PHP repair in #6989](https://github.com/adamtheturtle/literalizer/pull/6989). This branch is not intended to be merged.

## Results and counting unit

The final completed cohort has **2,016 passing native programs**: seeds **5493 and 6569**, twelve generated examples in each of seven option contexts × three input formats × four API forms. These are program executions, not 2,016 independent payloads; draws intentionally repeat across API/configuration comparisons.

All **6,048 output mutations** are rejected: 2,016 boolean/type changes, 2,016 negative-zero sign changes, and 2,016 changes to another mapping-kind tag in the common transport. Every mapping key remains unchanged. The archive retains actual native outputs, expected values and each mutated payload. The value tags come from native runtime checks before JSON serialization.

Another **84 programs** run the existing capability corpora through all pilot contexts, formats and APIs. Exclusions retain each existing consumer boundary: JavaScript omits `biginteger`; PHP omits `biginteger` and `empty_object`. Python retains the corpus accepted by its parser/runtime; this is not a claim of strict TOML specification validation for that corpus's wide integers.

Separately, **216 boundary controls pass**: 204 documented rejections and twelve supported PHP multiline-string programs. **36 native PHP reference controls** preserve mapping keys, mapping kind and value 42, with/without inference hints, in whole/row calls across all three input formats and PHP profiles.

## Pilot coverage

| Context | Selected options |
| --- | --- |
| Python tuple | Defaults; compact layout |
| Python list | LIST, SAFE hints, SINGLE strings, SCIENTIFIC floats, HEX integers; multiline |
| JavaScript object | Defaults; compact layout |
| JavaScript Map | MAP, LET, POSITIONAL calls, MULTILINE strings, FIXED floats, HEX integers; multiline |
| PHP double | Defaults; compact layout |
| PHP single | SINGLE strings, SCIENTIFIC floats, HEX integers, SAFE hints; multiline |
| PHP multiline | MULTILINE strings, FIXED floats, BINARY integers; multiline |

Each context crosses JSON, YAML and TOML with bare literals, new declarations, existing-variable assignments and whole-value calls. The generator bounds the candidate to depth 3, width 3, strings of length 12, integers in ±1,000,000 and finite floats in that range. A fixed outer wrapper adds boolean and negative-zero controls. PHP generated maps are nonempty and avoid integer-coercible string keys. Those boundaries are checked separately rather than silently skipped. TOML generated values exclude null; JSON/YAML generation includes it.

The common transport retains concrete Python list/tuple, JavaScript Object/Map and PHP mapping/sequence distinctions. Equal integer/float representations otherwise follow the existing shared verifier's numerical equivalence contract. Booleans and signed zeros are distinct.

## Classified findings

* **Renderer defect #6986:** PHP call arguments accepted lossy empty mappings and numeric string keys. Hypothesis reduces these to `{}` and `{"0":""}`. Native PHP turns both into sequences and the latter key into integer 0. See [the minimal witnesses](minimized/witnesses.json), native sources and outputs. The retained trace has eleven successful mismatch-predicate evaluations; it is not a total-predicate-call count. The focused repair validates actual mapping construction, including ordered mappings and reference-valued keys. Four ordinary rejection manifests retain the lesson; two lossy PHP success fixtures are removed. A shared reference-only mapping case adds 53 compiling fixtures.
* **Renderer defect #6987:** Lua calls accept a nil table key that ordinary rendering rejects. Executing `consume({[nil] = 1})` fails with `table index is nil`. Empty mapping calls also bypass Lua's policy. This is separately filed, not repaired by the PHP PR. Native sources, commands and outputs are in the evidence archive.
* **Excluded harness/generator experiments:** the first smoke adapter added an extra argument wrapper; an early generator admitted unsupported raw C0 controls; a broad binding-validation hook was rejected because declaration-specific checks are not universally call checks. These are not additional renderer findings.
* **Infrastructure exclusions:** seed 0 retry attempts and broad local validation suffered repeated ENOSPC. A packaging scratch directory was also picked up during an early root collection, and a later broad run ended with xdist teardown errors. Interrupted runs are excluded from the completed cohort. The broad local suite is inconclusive; no full-suite/coverage success is claimed.

The PHP rejection families fail against the old renderer and pass with the repair. Targeted PHP literal goldens pass (26 tests, 1,355 subtests), as do PHP call goldens (368 tests, 361 subtests). Mypy and Pyright pass for the changed Python modules. Hosted CI is the complete compiler/version matrix gate.

## Audit and remaining gaps

At frozen main `c0ce16c04f0afc3b04299ca917e095d472cbc220`, the registry has **65 languages**, **62 fixed-corpus roundtrip scripts**, and two retained generated-program property modules: `test_json_program_roundtrip.py` and `test_binary_program_goldens.py`, both Python-focused. The issue's old `tests/test_roundtrip.py` location has been reorganized. [coverage-audit.json](coverage-audit.json) retains the static runner/API inventory; indirect helper selection can limit static option attribution.

This pass samples configurations; it does not certify a Cartesian product. Wider backends, generated typed temporal/bytes/set inputs, nonfinite transports, other versioned runtimes, generated row calls, native-call/invocation APIs, declaration composition and zipped transforms remain uncovered here. The actual Python runtime was 3.14.8; selecting a Python target syntax version does not establish an older runtime result. Lua's separately filed defect remains open. The parent discovery issue remains open.

## Reproduction and limits

Use the source checkout at `05087cf378bf0365506c4c95d742949a494dd6c5` (or the audited base plus [renderer.patch](renderer.patch)). Install that checkout's pinned development environment and the recorded native runtimes. The controller's observed tools are Python 3.14.8, Hypothesis 6.170.15, Node 26.12.1 and PHP 8.5.12. The separate Lua control ran Lua 5.5.1.

Run from the source checkout, with these archive files in another directory:

```sh
uvx uv@0.13.0 sync --group dev --python 3.14
PYTHONPATH=.:src scripts/run-bounded.sh discovery --signal=KILL 440s \
  .venv/bin/python /path/to/archive/scripts/discover.py \
  --output /fresh/output/seed-5493 --seed 5493 --examples 12 --budget-seconds 420
```

Repeat with seed 6569 and a fresh output directory. Every native child gets at most fifteen seconds; the controller has a 420-second guard and the outer process a 440-second deadline. The actual completed seed runs took 120.247 and 131.114 local seconds under contention. These are not matched hosted cost measurements. Metadata records every constructor option, controller/tool version and source hash. Each example retains its input, source, program, expected value, stdout/stderr, classification, command and a direct `--replay input.json` invocation.

Download and extract [evidence.tar.gz](evidence.tar.gz), then independently validate the retained outputs and mutation payloads:

```sh
PYTHONPATH=.:src .venv/bin/python /path/to/archive/scripts/verify_archive.py \
  /path/to/archive/evidence.tar.gz
```

Replay any extracted `final-*/NNNNNN/input.json` with `discover.py --replay ... --output /fresh/replay`. Rerun the corpus, error and reference controllers with fresh output directories. The minimizer must run against baseline `c0ce16c04f0afc3b04299ca917e095d472cbc220`, with its recorded Hypothesis settings; the fixed renderer correctly supplies no accepted mismatch.

The evidence is 651,123 bytes, with SHA-256 `7d7f1b240705d7848ca212a7d124249ff022a8e545d1a6855bca1d147d73285d`. It includes 24,924 files with the final outputs, all mutation payloads, capability/boundary/reference controls, minimized native witnesses and validation logs. Partial audit files from disk interruptions were replaced by independently verified mutations while constructing this archive. No broad randomized command or CI job is added to main.
