import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.exceptions import HeterogeneousSiblingListsError
from literalizer.languages import Go, Kotlin, Python
from scripts.shared_record_common import DECLARING_DOCUMENT, DEPENDENT_DOCUMENT

PAIR_INPUTS = {
    "scalar": (
        {"name": "first", "count": 1, "flag": True},
        {"name": "second", "count": 2, "flag": False},
    ),
    "nested": (
        {"name": "first", "values": [{"key": 1, "active": True}]},
        {"name": "second", "values": [{"key": 2, "active": False}]},
    ),
    "array": (
        {"name": "first", "values": [1, 2]},
        {"name": "second", "values": [3]},
    ),
    "typed_empty": (
        {"name": "first", "values": []},
        {"name": "second", "values": [3]},
    ),
    "incompatible": (
        {"name": "first", "count": 1, "flag": True},
        {"name": "second", "count": "two", "flag": False},
    ),
}
go_cases = {
    "scalar": (
        'first.Name=="first" && first.Count==1 && first.Flag && second.Name=="second" && second.Count==2 && !second.Flag',
        "first, second, again Record0",
        "first == again",
    ),
    "nested": (
        'first.Name=="first" && len(first.Values)==1 && first.Values[0].Key==1 && first.Values[0].Active && second.Name=="second" && len(second.Values)==1 && second.Values[0].Key==2 && !second.Values[0].Active',
        "first, second, again Record0",
        "&first.Values[0] == &again.Values[0]",
    ),
    "array": (
        'first.Name=="first" && len(first.Values)==2 && first.Values[0]==1 && first.Values[1]==2 && second.Name=="second" && len(second.Values)==1 && second.Values[0]==3',
        "first, second, again Record0",
        "&first.Values[0] == &again.Values[0]",
    ),
    "typed_empty": (
        'first.Name=="first" && first.Values!=nil && len(first.Values)==0 && second.Name=="second" && len(second.Values)==1 && second.Values[0]==3',
        "first, second, again Record0",
        "&second.Values[0] == &again.Values[0]",
    ),
    "maps": (
        'len(first)==2 && len(second)==2 && first[0].Name=="row_1" && first[0].Attributes["colour"]=="red" && first[0].Attributes["discounted"]==true && first[1].Attributes["size"]=="large" && second[0].Name=="row_3" && second[0].Attributes["size"]=="small" && second[1].Attributes["colour"]=="white"',
        "first, second, again []Record0",
        "&first[0] == &again[0]",
    ),
}
kotlin_cases = {
    "scalar": 'first.name == "first" && first.count == 1 && first.flag && second.name == "second" && second.count == 2 && !second.flag',
    "nested": 'first.name == "first" && first.values.single().key == 1 && first.values.single().active && second.name == "second" && second.values.single().key == 2 && !second.values.single().active',
    "array": 'first.name == "first" && first.values.contentEquals(intArrayOf(1, 2)) && second.name == "second" && second.values.contentEquals(intArrayOf(3))',
    "typed_empty": 'first.name == "first" && first.values.isEmpty() && second.name == "second" && second.values.contentEquals(intArrayOf(3))',
    "maps": 'first.size == 2 && second.size == 2 && first[0].name == "row_1" && first[0].attributes["colour"] == "red" && first[0].attributes["discounted"] == true && first[1].attributes["size"] == "large" && second[0].name == "row_3" && second[0].attributes["size"] == "small" && second[1].attributes["colour"] == "white" && second[1].attributes["discounted"] == false',
}


def probe(
    cls,
    case,
    inputs,
    reverse,
    hints,
    *,
    bad=False,
    collision=False,
    reuse_only=False,
    mutate=False,
):
    kwargs = {"heterogeneous_strategy": cls.heterogeneous_strategies.RECORD}
    if case == "typed_empty" and cls is not Kotlin:
        kwargs["default_sequence_element_type"] = "int"
    if case == "maps" and cls is Go:
        kwargs["record_map_value_typing"] = Go.record_map_value_typings.WIDE
    language = cls(**kwargs)
    values = dict(zip(("declaring", "dependent"), inputs, strict=True))
    if mutate:
        values["declaring"] = {**values["declaring"], "flag": False}
    bindings = tuple(
        literalize(
            source=json.dumps(value),
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name=name, modifiers=frozenset()),
        )
        for name, value in values.items()
    )
    if not bad:
        assert bindings[0].preamble == bindings[1].preamble, (cls, case)
        assert bindings[0].body_preamble == bindings[1].body_preamble, (
            cls,
            case,
        )
    repeated = "dependent" if case == "typed_empty" else "declaring"
    call = literalize_call(
        source=json.dumps(
            [[{"$ref": name} for name in ("declaring", "dependent", repeated)]]
        ),
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("first", "second", "again"),
        per_element=True,
        ref_key="$ref",
        ref_values=values if hints else None,
    )
    if cls is Go:
        check, signature, identity = go_cases[
            "scalar" if case == "incompatible" else case
        ]
        consumer = f'func consume({signature}) {{ if !({check} && {identity}) {{ panic("value or reuse mismatch") }} }}'
        if collision:
            consumer += "\nfunc Record0() {}"
        header, body, filename, command = (
            (consumer,),
            (),
            "main.go",
            ["go", "run", "main.go"],
        )
    elif cls is Kotlin:
        check = kotlin_cases["scalar" if case == "incompatible" else case]
        dtype = "List<Record0>" if case == "maps" else "Record0"
        if case == "typed_empty" and bad:
            check = 'first.name == "first" && second.name == "second"'
        identity = "second === again" if case == "typed_empty" else "first === again"
        consumer = f"fun consume(first: {dtype}, second: {dtype}, again: {dtype}) {{ check({check}); check({identity}) }}"
        if collision:
            consumer += "\ndata class Record0(val collision: Int)"
        header, body, filename, command = (
            (),
            (consumer,),
            "main.kts",
            ["kotlinc", "-script", "main.kts"],
        )
    else:
        consumer = "\n".join(
            (
                "from dataclasses import asdict",
                "import json",
                "def consume(first, second, again):",
                f"    assert first is again"
                if case != "typed_empty"
                else "    assert second is again",
                "    assert type(first.count) is int and type(second.count) is int"
                if case in ("scalar", "incompatible")
                else "    assert type(first) is type(second)",
                f"    assert json.loads(json.dumps([asdict(first), asdict(second)])) == {list(inputs)!r}",
            )
        )
        header, body, filename, command = (
            (),
            (consumer,),
            "main.py",
            [sys.executable, "main.py"],
        )
    ordered = bindings[::-1] if reverse else bindings
    if reuse_only:
        # The selected declaration is the only source of record definitions.
        shared = (
            *ordered[0].preamble,
            *header,
            *ordered[0].body_preamble,
            *body,
        )
        statements = (ordered[0].code, ordered[1].code, call.code)
        if cls is Go:
            statements = ("func main() {", *statements, "}")
        program = "\n".join((*shared, *statements))
    else:
        program = literalize_call_with_declarations(
            language=language,
            declarations=ordered,
            call=call,
            extra_preamble=header,
            extra_body_preamble=body,
        ).code
    with tempfile.TemporaryDirectory() as temp:
        (Path(temp) / filename).write_text(program, encoding="utf-8")
        completed = subprocess.run(
            command, cwd=temp, capture_output=True, text=True, timeout=40
        )
    if bad or collision or mutate:
        assert completed.returncode != 0, (cls, case, program)
        reason = (
            "caller-name-collision"
            if collision
            else "value-mutation"
            if mutate
            else "incompatible-schema"
        )
        expected_error = {
            "Python": {
                "value-mutation": "AssertionError",
                "incompatible-schema": "AssertionError",
            },
            "Go": {
                "value-mutation": "panic: value or reuse mismatch",
                "caller-name-collision": "Record0 redeclared",
                "incompatible-schema": "cannot use",
            },
            "Kotlin": {
                "value-mutation": "IllegalStateException",
                "caller-name-collision": "duplicate JVM class name",
                "incompatible-schema": "duplicate JVM class name",
            },
        }[cls.__name__][reason]
        assert expected_error in completed.stderr, (
            cls,
            case,
            program,
            completed.stderr,
        )
        print(
            cls.__name__, case, reason, "rejected", expected_error, flush=True
        )
    else:
        assert completed.returncode == 0, (
            cls,
            case,
            reverse,
            hints,
            program,
            completed.stderr,
        )
        print(
            cls.__name__,
            case,
            "reuse-only" if reuse_only else "compose",
            reverse,
            hints,
            "OK",
            flush=True,
        )


started = time.monotonic()
for cls in (Python, Go, Kotlin):
    for case in ("scalar", "nested", "array", "typed_empty", "maps"):
        if (
            case == "maps"
            and cls is Python
            or case == "typed_empty"
            and cls is Kotlin
        ):
            continue
        if case == "maps":
            inputs = (
                json.loads(DECLARING_DOCUMENT),
                json.loads(DEPENDENT_DOCUMENT),
            )
            if cls is Kotlin:
                inputs[1][1]["attributes"]["discounted"] = False
        else:
            inputs = PAIR_INPUTS[case]
        for reverse in (False, True):
            for hints in (False, True):
                probe(cls, case, inputs, reverse, hints)
            probe(cls, case, inputs, reverse, False, reuse_only=True)
    probe(cls, "scalar", PAIR_INPUTS["scalar"], False, True, mutate=True)
    probe(
        cls, "incompatible", PAIR_INPUTS["incompatible"], False, True, bad=True
    )
    if cls is not Python:
        probe(
            cls, "scalar", PAIR_INPUTS["scalar"], False, True, collision=True
        )
probe(Kotlin, "typed_empty", PAIR_INPUTS["typed_empty"], False, True, bad=True)
try:
    literalize(
        source=DECLARING_DOCUMENT,
        input_format=InputFormat.JSON,
        language=Python(
            heterogeneous_strategy=Python.heterogeneous_strategies.RECORD
        ),
    )
except HeterogeneousSiblingListsError:
    print(
        "Python maps rejected standalone as heterogeneous sibling shapes",
        flush=True,
    )
else:
    raise AssertionError("Expected standalone Python record-shape rejection")
print(f"Elapsed {time.monotonic() - started:.3f}s")
