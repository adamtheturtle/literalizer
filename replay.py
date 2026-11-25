"""Bounded native transformation and option experiments for #5491 and #5490."""

import collections
import dataclasses
import datetime as dt
import itertools
import json
import sys
import time
from pathlib import Path

from literalizer import (
    CollectionLayout,
    ExistingVariable,
    IdentifierCase,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import JavaScript, Lua, Php, Python, Ruby
from literalizer.exceptions import (
    CallArgNotSupportedError,
    UnrepresentableInputError,
)
from native_observers import (
    OBSERVERS,
    expected_lines,
    language_profiles,
    observe,
    yaml_source,
)

CLASSES = (Python, JavaScript, Lua, Ruby, Php)
ROOT = Path("tests/integration/cases").resolve()
SIBLINGS = (
    [[], [1, 2]],
    [["a", b"\x80"], [False, -0.0, ["c"]]],
    [[None, None], ["filled", False]],
    [[dt.date(2024, 2, 29), b"\x00\xff"], [dt.date(1970, 1, 1), b"x"]],
)
FIELDS = ("person_name", "renamed_field", "class")
REF_NAMES = ("shared_value", "other_binding", "record_name")

OBSERVE = {
    "Python": "capture({value})",
    "JavaScript": "observe({value});",
    "Lua": "capture({value})",
    "Ruby": "observe({value})",
    "Php": "capture(${value});",
}
READ_FIELD = {
    "Python": "assert tuple({binding}) == ({key},)\ncapture({binding}[{key}])",
    "JavaScript": "if (Object.keys({binding}).length !== 1 || !Object.hasOwn({binding}, {key})) throw new Error('wrong key');\nobserve({binding}[{key}]);",
    "Lua": "assert(next({binding}) == {key} and next({binding}, {key}) == nil)\ncapture({binding}[{key}])",
    "Ruby": "raise 'wrong key' unless {binding}.keys == [{key}]\nobserve({binding}[{key}])",
    "Php": "if (array_keys(${binding}) !== [{key}]) throw new Exception('wrong key');\ncapture(${binding}[{key}]);",
}
RELAY = {
    "Python": "def relay(value):\n    return value",
    "JavaScript": "function relay({value}) { return value; }",
    "Lua": "local function relay(value) return value end",
    "Ruby": "def relay(value:)\n  value\nend",
    "Php": "function relay($value) { return $value; }",
}


def checked_execute(backend, program, expected, label, deadline):
    try:
        status, actual, stderr = observe(backend, program, deadline)
    except Exception as exc:
        raise RuntimeError((label, program)) from exc
    if status or actual != expected:
        raise AssertionError((label, expected, actual, stderr, program))


def assembled(program, backend, check, *, scaffold=""):
    """Honor the generated mandatory file prefix before adding observers."""
    prefix = {
        "Php": "<?php",
        "Python": "from __future__ import annotations",
    }.get(backend)
    lines = [OBSERVERS[backend], scaffold, program, check, ""]
    if prefix is not None and program.startswith(prefix + "\n"):
        lines[2] = program.removeprefix(prefix + "\n")
        lines.insert(0, prefix)
    return "\n".join(lines)


def typed_yaml(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return "!!timestamp " + json.dumps(value.isoformat())
    if isinstance(value, list):
        return "[" + ", ".join(map(typed_yaml, value)) + "]"
    return yaml_source(value)


def named_literal(language, value, name, *, shape=None):
    input_format = InputFormat.YAML if shape is None else InputFormat.JSON
    source = typed_yaml(value) if shape is None else json.dumps(value)
    return literalize(
        source=source,
        input_format=input_format,
        language=language,
        variable_form=NewVariable(name=name, modifiers=frozenset()),
    )


def alias_check(backend, value, reverse, alternate):
    """Check identity and mutation semantics independently of the value oracle."""
    if backend == "Python":
        return f"""left = {value}[{int(reverse)}]
right = {value}[{int(not reverse)}][0]
assert left is right
if type(left) is list:
    left.append(88)
    assert right[-1] == 88
    left.pop()"""
    if backend == "JavaScript":
        return f"""const left = {value}[{int(reverse)}];
const right = {value}[{int(not reverse)}][0];
if (left !== right) throw new Error('reference identity lost');
left.push(88);
if (right[right.length - 1] !== 88) throw new Error('alias did not observe mutation');
left.pop();"""
    if backend == "Lua":
        return f"""local left = {value}[{1 + int(reverse)}]
local right = {value}[{1 + int(not reverse)}][1]
assert(rawequal(left, right))
left[#left+1] = 88
assert(right[#right] == 88)
left[#left] = nil"""
    if backend == "Ruby":
        return f"""left = {value}[{int(reverse)}]
right = {value}[{int(not reverse)}][0]
raise 'reference identity lost' unless left.equal?(right)
left << 88
raise 'alias did not observe mutation' unless right.last == 88
left.pop"""
    first, second = int(reverse), int(not reverse)
    return f"""${value}[{first}][] = 88;
if (${value}[{second}][0] !== [1, 2]) throw new Exception('array copy-on-write lost');
array_pop(${value}[{first}]);"""


def invariant_controls(deadline):
    injected = {
        "Python": "specimen = (tuple([1, 2]), (tuple([1, 2]),))",
        "JavaScript": "const specimen = [[1, 2], [[1, 2]]];",
        "Lua": "local specimen = {{1, 2}, {{1, 2}}}",
        "Ruby": "specimen = [[1, 2], [[1, 2]]]",
        "Php": "<?php\n$shared = [1, 2]; $specimen = [&$shared, [&$shared]];",
    }
    relation_controls = []
    for backend, code in injected.items():
        readback = OBSERVE[backend].format(value="specimen")
        program = assembled(
            code,
            backend,
            readback + "\n" + alias_check(backend, "specimen", False, False),
        )
        status, actual, stderr = observe(backend, program, deadline)
        expectation = expected_lines([[1, 2], [[1, 2]]], backend, False)
        assert actual[: len(expectation)] == expectation, (backend, actual)
        assert status != 0, (backend, program)
        marker = {
            "JavaScript": "reference identity lost",
            "Ruby": "reference identity lost",
            "Php": "array copy-on-write lost",
        }.get(backend, "assert")
        assert marker in stderr or any(
            marker in line for line in actual[len(expectation) :]
        ), (backend, stderr, actual)
        relation_controls.append(backend)

    language = Python(
        heterogeneous_strategy=Python.heterogeneous_strategies.RECORD
    )
    verified_records = []
    for key in ("person_name", "renamed_field", "Record0"):
        result = named_literal(
            language, {"count": 3, key: "value"}, "specimen", shape="map"
        )
        code = "\n".join(
            (*result.preamble, *result.body_preamble, result.code)
        )
        checked_execute(
            "Python",
            assembled(
                code,
                "Python",
                f"capture(dataclasses.asdict(specimen)[{key!r}])\ncapture(specimen.count)",
            ),
            expected_lines("value", "Python", False) + ["int:3"],
            ("Python", "record field rename", key),
            deadline,
        )
        verified_records.append(key)
    try:
        named_literal(
            language, {"count": 3, "class": "value"}, "specimen", shape="map"
        )
    except UnrepresentableInputError as error:
        assert "record field name 'class' is reserved" in str(error), error
    else:
        raise AssertionError(
            "expected a reserved Python record field rejection"
        )
    return {
        "wrong_identity_detected": relation_controls,
        "record_renames": verified_records,
        "expected_rejection": "reserved Python record field",
    }


def run_invariants(deadline):
    counts = collections.Counter()
    excluded = collections.Counter()
    for backend, alternate, language in language_profiles():
        for i, values in enumerate(SIBLINGS):
            if backend == "Lua" and i == 2:
                excluded["Lua null slots in a native table"] += 2
                continue
            for reverse in (False, True):
                data = values[::-1] if reverse else values
                result = named_literal(language, data, "specimen")
                text = "\n".join(
                    (*result.preamble, *result.body_preamble, result.code)
                )
                checked_execute(
                    backend,
                    assembled(
                        text,
                        backend,
                        OBSERVE[backend].format(value="specimen"),
                    ),
                    expected_lines(data, backend, alternate),
                    (backend, alternate, "siblings", i, reverse),
                    deadline,
                )
                counts[backend, "siblings"] += 1

        for name, key in itertools.product(REF_NAMES, FIELDS):
            result = named_literal(
                language, {key: [3, False]}, name, shape="map"
            )
            code = "\n".join(
                (*result.preamble, *result.body_preamble, result.code)
            )
            check = READ_FIELD[backend].format(
                binding=name, key=json.dumps(key)
            )
            checked_execute(
                backend,
                assembled(code, backend, check),
                expected_lines([3, False], backend, alternate),
                (backend, alternate, "rename", name, key),
                deadline,
            )
            counts[backend, "rename"] += 1

        for name, ref_case in itertools.product(
            REF_NAMES, (None, IdentifierCase.CAMEL)
        ):
            if (
                ref_case is not None
                and ref_case not in language.supported_ref_cases
            ):
                excluded[f"{backend} {ref_case.name} reference spelling"] += 4
                continue
            bound_name = (
                name if ref_case is None else ref_case.convert(name=name)
            )
            bound = named_literal(language, [1, 2], bound_name)
            for reverse, hints in itertools.product((False, True), repeat=2):
                marker = {"$ref": name}
                source, expected = [marker, [marker]], [[1, 2], [[1, 2]]]
                if reverse:
                    source, expected = source[::-1], expected[::-1]
                result = literalize_call(
                    source=json.dumps(source),
                    input_format=InputFormat.JSON,
                    language=language,
                    target_function="relay",
                    parameter_names=("value",),
                    per_element=False,
                    ref_key="$ref",
                    ref_case=ref_case,
                    ref_values={name: [1, 2]} if hints else None,
                    variable_form=NewVariable(
                        name="specimen", modifiers=frozenset()
                    ),
                )
                code = literalize_call_with_declarations(
                    language=language,
                    declarations=(bound,),
                    call=result,
                ).code
                checks = "\n".join(
                    (
                        alias_check(backend, "specimen", reverse, alternate),
                        OBSERVE[backend].format(value="specimen"),
                    )
                )
                program = assembled(
                    code, backend, checks, scaffold=RELAY[backend]
                )
                label = (
                    backend,
                    alternate,
                    "reference",
                    name,
                    ref_case,
                    reverse,
                    hints,
                )
                checked_execute(
                    backend,
                    program,
                    expected_lines(expected, backend, alternate),
                    label,
                    deadline,
                )
                counts[backend, "reference"] += 1
        for reverse in (False, True):
            name = "shared_value"
            raw = [{"$ref": name}, [{"$ref": name}]]
            expected = [[1, 2], [[1, 2]]]
            if reverse:
                raw, expected = raw[::-1], expected[::-1]
            try:
                bound_result = literalize(
                    source=json.dumps(raw),
                    input_format=InputFormat.JSON,
                    language=language,
                    bound_refs={name: [1, 2]},
                    ref_key="$ref",
                    wrap_in_file=True,
                    variable_form=NewVariable(
                        name="specimen", modifiers=frozenset()
                    ),
                )
            except CallArgNotSupportedError as error:
                assert backend == "Ruby" and "surrounding assignment" in str(
                    error
                ), error
                excluded["Ruby API-materialized references"] += 1
                continue
            assert backend != "Ruby", (
                "Ruby API-materialized reference exclusion changed"
            )
            checks = "\n".join(
                (
                    alias_check(backend, "specimen", reverse, alternate),
                    OBSERVE[backend].format(value="specimen"),
                )
            )
            checked_execute(
                backend,
                assembled(bound_result.code, backend, checks),
                expected_lines(expected, backend, alternate),
                (backend, alternate, "bound_refs", reverse),
                deadline,
            )
            counts[backend, "bound_refs"] += 1
    return {
        "passes": records(counts),
        "excluded": dict(excluded),
        "controls": invariant_controls(deadline),
    }


def pairs(row):
    return frozenset(itertools.combinations(sorted(row.items()), 2))


def product_rows(factors):
    return [
        dict(zip(factors, values, strict=True))
        for values in itertools.product(*factors.values())
    ]


def cover_pairs(factors):
    candidates = product_rows(factors)
    rows = [
        row
        for row in candidates
        if not (
            row.get("declaration") == "CONST" and row["binding"] == "existing"
        )
    ]
    all_pairs = frozenset().union(*(pairs(row) for row in rows))
    uncovered = set(all_pairs)
    selected = []
    while uncovered:
        row = max(rows, key=lambda row: len(pairs(row) & uncovered))
        selected.append(row)
        uncovered -= pairs(row)
    triple = next(
        row
        for row in rows
        if row["references"] == "hinted"
        and row["binding"] == "existing"
        and row["call"] == "rows"
    )
    if not any(
        all(
            row[key] == triple[key]
            for key in ("references", "binding", "call")
        )
        for row in selected
    ):
        selected.append(triple)
    assert frozenset().union(*(pairs(row) for row in selected)) == all_pairs
    return len(candidates), len(rows), all_pairs, selected


def factors_for(backend):
    factors = {
        "quote": ("DOUBLE", "SINGLE"),
        "integer": ("DECIMAL", "HEX"),
        "float": ("REPR", "SCIENTIFIC"),
        "bytes": ("HEX", "BASE64"),
        "layout": ("COMPACT", "MULTILINE"),
        "binding": ("new", "existing"),
        "call": ("whole", "rows"),
        "references": ("direct", "unhinted", "hinted"),
    }
    if backend == "Python":
        factors["sequence"] = ("TUPLE", "LIST")
        factors["hints"] = ("NEVER", "ALWAYS")
    else:
        factors["temporal"] = ("native", "ISO")
    if backend == "JavaScript":
        factors["declaration"] = ("CONST", "LET")
    return factors


def initial_value(value):
    """Seed an existing binding with a different value of the same shape."""
    if isinstance(value, list):
        return [initial_value(child) for child in value]
    if type(value) is bool:
        return not value
    if type(value) is int:
        return -value if value else 1
    if type(value) is float:
        return 0.5
    if isinstance(value, (dt.date, dt.datetime)):
        return value + dt.timedelta(days=1)
    if isinstance(value, bytes):
        return value + b"!"
    if isinstance(value, str):
        return value + "!"
    raise TypeError(type(value))


def pair_program(cls, row, item, companion):
    backend = cls.__name__
    options = dict(
        string_format=cls.string_formats[row["quote"]],
        integer_format=cls.integer_formats[row["integer"]],
        float_format=cls.float_formats[row["float"]],
        bytes_format=cls.bytes_formats[row["bytes"]],
    )
    if row.get("temporal") == "ISO":
        options.update(
            date_format=cls.date_formats.ISO,
            datetime_format=cls.datetime_formats.ISO,
        )
    if cls is Python:
        options["sequence_format"] = Python.sequence_formats[row["sequence"]]
        options["variable_type_hints"] = Python.variable_type_hints_formats[
            row["hints"]
        ]
    if cls is JavaScript:
        options["declaration_style"] = JavaScript.declaration_styles[
            row["declaration"]
        ]
    language = cls(**options)
    setup = []
    refs = row["references"]
    if refs != "direct":
        setup.append(named_literal(language, companion, "shared_value"))
    form = NewVariable(name="specimen", modifiers=frozenset())
    value_source = typed_yaml(item)
    expected = item
    if refs != "direct":
        value_source = f"[{value_source}, {{'$ref': 'shared_value'}}]"
        expected = [item, companion]
    if row["binding"] == "existing":
        setup.append(
            named_literal(language, initial_value(expected), "specimen")
        )
        form = ExistingVariable(name="specimen")
    rows = row["call"] == "rows"
    call = literalize_call(
        source=f"[[{value_source}]]" if rows else value_source,
        input_format=InputFormat.YAML,
        language=language,
        target_function="relay",
        parameter_names=("value",),
        per_element=rows,
        variable_form=form,
        ref_key="$ref" if refs != "direct" else None,
        ref_values={"shared_value": companion} if refs == "hinted" else None,
        collection_layout=CollectionLayout[row["layout"]],
    )
    result = literalize_call_with_declarations(
        language=language, declarations=setup, call=call
    )
    program = assembled(
        result.code,
        backend,
        OBSERVE[backend].format(value="specimen"),
        scaffold=RELAY[backend],
    )
    return program, expected_for_row(expected, backend, row)


def expected_for_row(value, backend, row):
    if isinstance(value, list):
        return [
            f"{row.get('sequence', 'LIST').lower()}:{len(value)}",
            *(
                entry
                for child in value
                for entry in expected_for_row(child, backend, row)
            ),
        ]
    if isinstance(value, bytes):
        alternate = row["bytes"] == "BASE64"
        if backend == "Python" and not alternate:
            return expected_lines(value.hex(), backend, False)
        return expected_lines(value, backend, alternate)
    return expected_lines(value, backend, row.get("temporal") == "ISO")


def manifest_projection():
    from tests.integration.golden_outcomes import Success
    from tests.integration.call_variant_cases import call_golden_cases
    from tests.integration.variant_cases import build_variant_cases
    from tests.integration.case_manifests import ComposedCallFixture
    from tests.integration.reference_cases import reference_golden_cases

    inventories = collections.defaultdict(list)
    backends = {cls.__name__ for cls in CLASSES}

    def projection(spec, layout, form):
        row = {
            "quote": spec.string_format.name,
            "integer": spec.integer_format.name,
            "float": spec.float_format.name,
            "bytes": spec.bytes_format.name,
            "layout": layout.name,
        }
        if isinstance(form, NewVariable):
            row["binding"] = "new"
        elif isinstance(form, ExistingVariable):
            row["binding"] = "existing"
        if spec.language_id == "python":
            row["sequence"] = spec.sequence_format.name
            row["hints"] = spec.variable_type_hints.name
        if spec.language_id == "javascript":
            row["declaration"] = spec.declaration_style.name
        if spec.language_id != "python":
            date = spec.date_format.name
            moment = spec.datetime_format.name
            if date == moment == "ISO":
                row["temporal"] = "ISO"
            elif date == moment == type(spec).date_format.name:
                row["temporal"] = "native"
        return row

    for case in build_variant_cases(cases_dir=ROOT):
        variant = case.variant
        backend = variant.lang_cls.__name__
        if backend in backends:
            inventories[backend, "literal-variant"].append(
                projection(
                    variant.spec, variant.collection_layout, case.variable_form
                )
            )
    for case in call_golden_cases(cases_dir=ROOT):
        backend = case.lang_cls.__name__
        if backend not in backends:
            continue
        for rendering in case.renderings:
            if not isinstance(rendering.outcome, Success):
                continue
            config = rendering.config
            row = projection(
                rendering.spec,
                CollectionLayout(config.collection_layout),
                config.variable_form,
            )
            row["call"] = "rows" if config.per_element else "whole"
            if not config.detect_references:
                row["references"] = "direct"
            elif (
                isinstance(config.fixture, ComposedCallFixture)
                and len(config.fixture.ref_declarations) > 0
            ):
                row["references"] = (
                    "hinted"
                    if config.explicit_ref_value_sources != {}
                    else "unhinted"
                )
            inventories[backend, "call"].append(row)
    for case in reference_golden_cases(cases_dir=ROOT):
        backend = case.lang_cls.__name__
        if backend not in backends:
            continue
        for rendering in case.renderings:
            if isinstance(rendering.outcome, Success):
                config = rendering.config
                row = projection(
                    rendering.spec,
                    CollectionLayout(config.collection_layout),
                    config.resolved_variable_form(),
                )
                if config.explicit_ref_value_sources is not None:
                    row["references"] = (
                        "hinted"
                        if config.explicit_ref_value_sources
                        else "unhinted"
                    )
                inventories[backend, "reference"].append(row)
    return inventories


def run_pairwise(deadline):
    inventory = manifest_projection()
    result = {}
    typed = [
        True,
        31,
        -0.0,
        b"\x00\x80\xff",
        "é ' \\",
        dt.date(2024, 2, 29),
        dt.datetime(1969, 12, 31, 23, 59, 59, 500000, tzinfo=dt.timezone.utc),
    ]
    inputs = (typed, [[], [False, [17, b"x"]]], "scalar ' 17")
    for cls in CLASSES:
        backend = cls.__name__
        factors = factors_for(backend)
        candidates, supported, admitted_pairs, selected = cover_pairs(factors)
        for index, row in enumerate(selected):
            for case_index, item in enumerate(inputs):
                code, expected = pair_program(cls, row, item, [1, 2])
                checked_execute(
                    backend,
                    code,
                    expected,
                    (backend, index, case_index, row),
                    deadline,
                )
        before = {}
        for family in ("literal-variant", "call", "reference"):
            rows = inventory[backend, family]
            witnesses = admitted_pairs & frozenset().union(
                *(pairs(row) for row in rows)
            )
            before[family] = {"contexts": len(rows), "pairs": len(witnesses)}
        combined = admitted_pairs & frozenset().union(
            *(
                pairs(row)
                for family in ("literal-variant", "call", "reference")
                for row in inventory[backend, family]
            )
        )
        result[backend] = {
            "candidates": candidates,
            "supported_contexts": supported,
            "admitted_pairs": len(admitted_pairs),
            "inventory": before,
            "pairs_not_present_in_inventory": len(admitted_pairs - combined),
            "unwitnessed_pairs": sorted(admitted_pairs - combined),
            "configurations": selected,
            "programs": len(selected) * len(inputs),
        }
    return {"backends": result, "controls": pairwise_controls(deadline)}


def pairwise_controls(deadline):
    row = dict(
        quote="SINGLE",
        integer="HEX",
        float="SCIENTIFIC",
        bytes="BASE64",
        layout="MULTILINE",
        binding="existing",
        call="rows",
        references="hinted",
        temporal="native",
        declaration="LET",
    )
    too_precise = dt.datetime(
        1969, 12, 31, 23, 59, 59, 123456, tzinfo=dt.timezone.utc
    )
    try:
        pair_program(
            JavaScript, {**row, "binding": "new"}, too_precise, [1, 2]
        )
    except UnrepresentableInputError as error:
        assert "sub-millisecond datetime precision" in str(error), error
    else:
        raise AssertionError(
            "expected precision rejection for the native Date profile"
        )

    iso = {**row, "temporal": "ISO"}
    program, expected = pair_program(JavaScript, iso, too_precise, [1, 2])
    checked_execute(
        "JavaScript", program, expected, "ISO retains microseconds", deadline
    )

    invalid_binding = {**row, "declaration": "CONST"}
    program, _ = pair_program(JavaScript, invalid_binding, "value", [1, 2])
    status, _, stderr = observe("JavaScript", program, deadline)
    assert status != 0 and "Assignment to constant variable" in stderr, stderr

    wrong_binding = []
    for cls in CLASSES:
        backend = cls.__name__
        factors = factors_for(backend)
        profile = {key: values[0] for key, values in factors.items()}
        profile.update(references="hinted", call="rows", binding="existing")
        if cls is JavaScript:
            profile["declaration"] = "LET"
        program, expected = pair_program(cls, profile, True, [1, 2])
        checked_execute(
            backend,
            program,
            expected,
            (backend, "original reference"),
            deadline,
        )
        changed, changed_expected = pair_program(cls, profile, True, [9, 2])
        checked_execute(
            backend,
            changed,
            changed_expected,
            (backend, "changed reference"),
            deadline,
        )
        assert changed_expected != expected, backend
        wrong_binding.append(backend)
    return {
        "wrong_reference_values_detected": wrong_binding,
        "expected_native_date_precision_rejection": True,
        "iso_microseconds_preserved": True,
        "expected_const_reassignment_rejection": True,
    }


def records(counts):
    return [(*key, count) for key, count in sorted(counts.items())]


def main():
    phase, path = sys.argv[1:]
    start = time.monotonic()
    run = {"invariants": run_invariants, "pairwise": run_pairwise}[phase]
    result = run(start + 240)
    output = dict(
        phase=phase,
        elapsed_seconds=round(time.monotonic() - start, 3),
        details=result,
    )
    Path(path).write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(phase, output["elapsed_seconds"])


if __name__ == "__main__":
    main()
