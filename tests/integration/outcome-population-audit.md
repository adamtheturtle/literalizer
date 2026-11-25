# Golden outcome populations before and after the skip migration

The audit compares the baseline from issue 7014 with main after the case-owned fixture migration.
[Baseline revision](https://github.com/adamtheturtle/literalizer/tree/d08e2a1ea234c60a16c757a068785cc34aeca0c4) · [Current revision](https://github.com/adamtheturtle/literalizer/tree/a4ab86e6168ac86e01aa8ee22e3f698f4ac627ef) · [Audit issue](https://github.com/adamtheturtle/literalizer/issues/7316)

| Family | Before success | Before rejection | Before historical skip | After success | After rejection | After exclusion |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Literal | 41,643 | 94 | 3,565 | 41,644 | 3,660 | 0 |
| Variant | 51,409 | 158 | 5,649 | 51,410 | 5,807 | 0 |
| Call | 21,552 | 2,321 | 1,802 | 21,612 | 3,813 | 316 |
| Reference | 5,991 | 0 | 1,573 | 5,993 | 1,444 | 305 |
| Constructor | 132 | 0 | 1 | 132 | 1 | 0 |
| Total | 120,727 | 2,573 | 12,590 | 120,791 | 14,725 | 621 |

The comparison matched 135,889 cell identities across the two revisions.
Of the 12,590 historical skips, 12,143 now assert a rejection, 443 have an explicit exclusion, and four compare a success fixture.
The baseline did not record explicit exclusions.
The current run had zero execution skips.

The current catalog adds 248 identities, comprising 68 successes, two rejections, and 178 explicit reference exclusions that the baseline never scheduled.
One baseline identity was removed.
Its PureScript call used to run in the default context and is now exercised under the qualified import option.
Both executions compare a successful fixture.
[PureScript scenario update](https://github.com/adamtheturtle/literalizer/commit/3e4871e1bd12be54621658cd8c70d84d89cffcbc)

## Historical successes that changed

Seven Lua call cells now assert `UnrepresentableEmptyDictError`.
The historical programs constructed empty Lua tables and could lose the input's empty mapping semantics.
The case directories are `call_dotted_nested_empty_mapping_arguments`, `call_dotted_receiver_parameter_collisions` (default plus three options), `call_empty_container_type_hint`, and `call_empty_mapping_receiver_parameter`.
The PureScript identity above accounts for the only other baseline success without the same identity succeeding at both revisions.
[Lua renderer fix](https://github.com/adamtheturtle/literalizer/commit/bbcbe0a3f9550173c49f0c33be59c4af5dfedf54)

## Representative transitions

| Case and target | Before | After |
| --- | --- | --- |
| `array_map_element_type`, Dhall, base | Historical skip | Asserted rejection |
| `call_binding_existing_seeded`, Dhall, default call | Historical skip | Excluded because the synthetic seed cannot precede a second immutable binding |
| `call_wrapper_zip_integer`, Groovy and Zig, default call | Historical skip | Success |
| `literalize_ref_scalar`, Rust, const and static declarations | Historical skip | Success |
| `constructor_binding`, C#, const call binding | Historical skip | Asserted rejection |
| `call_dotted_nested_empty_mapping_arguments`, Lua, default call | Success | Asserted rejection |

For a focused execution control, include the five modules below and select `call_wrapper_zip_integer`, `literalize_ref_scalar`, `constructor_call_const`, or `call_dotted_nested_empty_mapping_arguments` with pytest's `-k` filter.
The audit compares the full set because literal pytest batches group multiple case identities.

## Counting rules

- Each cell is identified by family, case directory, language ID, version, and scenario.
  A scenario includes the authored example suffix when there is one.
  The comparison strips the former language prefix from the scenario, normalizes case, and ignores pytest batch numbers and parameter-ID collision suffixes.
- The variant family consists of the literal runner's `format_variant` scenario.
  Its other scenarios belong to the literal family.
  The reference family includes both default and explicit reference handling and their option variants.
  The constructor family includes target and binding cases.
  Standalone error contracts, native smoke programs, and other golden runners are outside these five families.
- A passing rendering with a checked-in fixture counts as a success.
  A passing rendering without one counts as an asserted rejection.
  The current catalog validates both classifications against the resolved outcome.
  Execution skips at the baseline remain historical skips, even when their reasons suggest a rejection or an exclusion.
- Exclusions count only when the current discovered catalog explicitly resolves them.
  Both revisions can filter combinations out before constructing a rendering.
  Those absent combinations cannot be counted as exclusions with this method.
  An unmatched identity is a catalog addition or removal, which can include an input or options rename.
- Count distinct cells once even when pytest groups several cells in a parent test.
  Both recorded runs passed.

## Reproduce

Use separate worktrees at the two pinned revisions.
Create a development environment at the current revision with `uv sync --group=dev`.
The audit used Python 3.15 and pytest 9.2.0 for both runs, with each worktree's own source on the import path.

Save the archived Python listing below as `/tmp/golden-outcome-audit.py`.
Run these commands from each pinned checkout with `revision=before` or `revision=after` and `audit_python` set to the absolute path to the shared environment's Python executable.

```sh
PYTHONPATH="$PWD/src:$PWD" "$audit_python" -m pytest -q -n 8 -o addopts='' \
  --report-log="/tmp/golden-$revision.jsonl" \
  tests/integration/test_literalize_golden.py \
  tests/integration/test_calls.py \
  tests/integration/test_literalize_ref_golden.py \
  tests/integration/test_literalize_ref_default.py \
  tests/integration/test_constructor_targets.py
PYTHONPATH="$PWD/src:$PWD" "$audit_python" /tmp/golden-outcome-audit.py \
  "$revision" "/tmp/golden-$revision.jsonl" > "/tmp/golden-$revision.json"
```

Compare the two catalogs from either checkout.

```sh
"$audit_python" /tmp/golden-outcome-audit.py compare \
  /tmp/golden-before.json /tmp/golden-after.json
```

<details>
<summary>Comparison script</summary>

```text
"""Compare resolved golden cells with pytest-reportlog results."""

import ast
import collections
import json
import re
import sys
from pathlib import Path


def compare(before_path, after_path):
    before, after = (
        {tuple(key): tuple(value) for key, value in json.loads(Path(path).read_text())}
        for path in (before_path, after_path)
    )
    transitions = collections.Counter()
    witnesses = {}
    old_successes = []
    for key in sorted(before.keys() | after.keys()):
        old = before.get(key, ("Absent", ""))[0]
        new = after.get(key, ("Absent", ""))[0]
        transitions[key[0], old, new] += 1
        witnesses.setdefault((key[0], old, new), key[1:])
        if old == "Success" and new != "Success":
            old_successes.append((key, new))
    for (family, old, new), count in sorted(transitions.items()):
        print(
            family, old, new, count, " / ".join(witnesses[family, old, new]), sep=" | "
        )
    print("Historical successes with no same-identity success:")
    for key, new in old_successes:
        print(*key, new, sep=" / ")


if sys.argv[1] == "compare":
    compare(*sys.argv[2:])
    sys.exit(0)


from tests.integration.call_variant_cases import call_golden_cases
from tests.integration.case_manifests import REF_DEFAULT_OWNER, REF_OWNER
from tests.integration.constructor_cases import constructor_binding_cases
from tests.integration.golden_scenarios import scenario_renderings
from tests.integration.reference_cases import (
    build_literalize_ref_variant_cases,
    discover_literalize_ref_cases,
)

revision, report_path = sys.argv[1:]
current = revision == "after"
root = Path("tests/integration/cases").resolve()
catalog = {}


def record(report_key, family, case, language, version, name, path, outcome):
    scenario = (
        "base"
        if name == language.__name__
        else name.removeprefix(language.__name__ + "_")
    )
    key = (family, case, language.language_id, version.lower(), scenario.lower())
    if report_key in catalog and catalog[report_key][0] != key:
        raise ValueError((report_key, key, catalog[report_key]))
    catalog[report_key] = key, path, outcome


for (scenario, language), renderings in scenario_renderings().items():
    family = "variant" if scenario == "format_variant" else "literal"
    for rendering in renderings:
        for spec in rendering.specs:
            version = spec.language_version
            path = (
                rendering.artifact(version=version).path
                if current
                else rendering.golden_path(version=version)
            )
            outcome = type(rendering.outcome(spec=spec)).__name__ if current else None
            record(
                (
                    "test_golden_file",
                    scenario,
                    language.__name__,
                    rendering.case_dir_name,
                    rendering.golden_name,
                    version.name,
                ),
                family,
                rendering.case_dir_name,
                language,
                version.name,
                rendering.golden_name,
                path,
                outcome,
            )


def call_or_reference(cases, family, test):
    for case in cases:
        for rendering in case.renderings:
            cfg = rendering.config
            language = rendering.lang_cls
            version = rendering.spec.language_version.name
            if family == "call":
                label = case.test_id
            else:
                target = (
                    case.variant.name
                    if test == "test_literalize_ref_variant_golden_file"
                    else language.__name__
                )
                label = f"{cfg.coverage_id}/{target}"
            path = (
                rendering.artifact(cases_dir=root).path
                if current
                else rendering.golden_path(cases_dir=root)
            )
            outcome = type(rendering.outcome).__name__ if current else None
            record(
                (test, label, version),
                family,
                cfg.case_dir_name,
                language,
                version,
                cfg.golden_name(name=rendering.golden_name),
                path,
                outcome,
            )


call_or_reference(call_golden_cases(cases_dir=root), "call", "test_call_golden_file")
for owner, test in (
    (REF_OWNER, "test_literalize_ref_golden_file"),
    (REF_DEFAULT_OWNER, "test_literalize_ref_default_golden_file"),
):
    kwargs = {"cases_dir": root} if current else {}
    call_or_reference(
        discover_literalize_ref_cases(owner=owner, **kwargs), "reference", test
    )
call_or_reference(
    build_literalize_ref_variant_cases(**kwargs),
    "reference",
    "test_literalize_ref_variant_golden_file",
)

for case in constructor_binding_cases(cases_dir=root):
    name = case.manifest.case_dir.name
    for rendering in case.renderings:
        version = rendering.version.name
        path = rendering.artifact.path if current else rendering.golden_path
        outcome = type(rendering.outcome).__name__ if current else None
        record(
            ("test_constructor_binding_golden_file", f"{name}/{case.name}", version),
            "constructor",
            name,
            case.lang_cls,
            version,
            case.name,
            path,
            outcome,
        )

observed = {}
failures = []
with Path(report_path).open() as reports:
    for line in reports:
        report = json.loads(line)
        if report.get("when") != "call" or "_subtest.context" not in report:
            continue
        node = report["nodeid"].split("::", 1)[1]
        test, label = node.rstrip("]").split("[", 1)
        context = {
            name: ast.literal_eval(ast.literal_eval(value))
            for name, value in report["_subtest.context"]["kwargs"].items()
        }
        version = context["version"]
        if test == "test_golden_file":
            group, language = re.fullmatch(
                r"(.+?)-([A-Za-z0-9]+)(?:-batch[0-9]+)?", label
            ).groups()
            key = (
                test,
                group,
                language,
                context["case_dir_name"],
                context["golden_name"],
                version,
            )
        else:
            key = (test, label, version)
        if key not in catalog and test != "test_golden_file":
            # Pytest appends sequence numbers to duplicate parameter IDs.
            key = (test, re.sub(r"[0-9]+$", "", label), version)
        if key not in catalog:
            failures.append(("unmatched", key))
            continue
        if report["outcome"] == "skipped":
            observed[key] = ("Historical skip", report["longrepr"][-1])
        elif report["outcome"] == "passed":
            observed[key] = (
                "Success" if catalog[key][1].is_file() else "Rejection",
                "",
            )
        else:
            failures.append(("failed", key))
results = {}
duplicates = collections.Counter()
for report_key, (key, path, expected) in catalog.items():
    found = observed.get(report_key)
    if found is None and expected == "Exclusion":
        found = ("Exclusion", "")
    if found is None:
        failures.append(("missing", report_key))
        continue
    if expected is not None and found[0] != expected:
        failures.append(("disagrees", report_key, expected, found))
    if key in results:
        duplicates[key[0]] += 1
        if results[key][0] != found[0]:
            failures.append(("duplicate disagrees", key, found, results[key]))
    results[key] = found
print(
    "candidate records:",
    len(catalog),
    "observed:",
    len(observed),
    "duplicate identities:",
    duplicates,
    file=sys.stderr,
)
print("failures:", len(failures), failures[:15], file=sys.stderr)
print(
    collections.Counter((key[0], result[0]) for key, result in results.items()),
    file=sys.stderr,
)
if failures:
    sys.exit(1)
json.dump([[key, value] for key, value in sorted(results.items())], sys.stdout)
```

</details>
