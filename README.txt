Literalizer bounded discovery archive - 2026-10-30

This orphan research branch is evidence for issues #5493 and #5494. It is not intended to be merged. Production fixes and minimized ordinary regressions live in PRs #6585, #6586, #6587 and #6588. The CI reliability fix is PR #6580. summary.json records limits, excluded adapter failures and the exact combined source heads.

The controllers run from a Literalizer source checkout with its pinned dev environment. Set PYTHONPATH=.:src and use UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev python /path/to/archive/SCRIPT.py. The scripts intentionally retain the observed executable paths in generated_typed.RUNTIMES; adjust those paths for another machine, recording replacement versions. YAML/TOML dependencies and Hypothesis come from the project dev group. Each run needs a fresh output tag.

Examples (after obtaining these archive files in a separate directory):
  DISCOVERY_TAG=typed-fixed ... python /path/to/archive/generated_typed.py
  DISCOVERY_TAG=native-temporal-fixed SKIP_SHRINK=1 ... python /path/to/archive/native_temporal.py
  COMPOSITION_TAG=composition-combined-final ... python /path/to/archive/composition_matrix.py
  ... python /path/to/archive/audit_mutations.py
Replace the ellipsis with the pinned environment command above. The native minimizer runs without SKIP_SHRINK on the recorded baseline; minimized.json retains the original 316-call trace. The audit reads typed-fixed and composition-combined-final outputs. Its valid typed-value changes preserve every mapping key. The final-head composition run has the same 96 passing controls and emits these corrected mutations directly.

To reproduce the combined source, start from the recorded base and apply the four source PRs independently, or use their eventual merged main version. The all-source smoke check passed all 32 minimized controls. Ordinary project CI remains the gate for production changes. All reported durations are local execution time rather than GitHub queue time or matched hosted runner-minute comparisons.
