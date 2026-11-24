"""Kotlin JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Kotlin
``val myData: JsonElement = ...`` declaration under
``json_type=Kotlin.JsonTypes.KOTLINX_JSON_ELEMENT`` (so the binding is a
``kotlinx.serialization.json.JsonElement`` tree built via
``Json.parseToJsonElement``), wrap it in a tiny ``.kts`` script that
prints ``Json.encodeToString(JsonElement.serializer(), myData)`` to
stdout, run it with ``kotlin``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-kotlin`` job in
``.github/workflows/lint.yml``, because that job is where the Kotlin
toolchain and the ``kotlinx-serialization-json`` jars are already
installed (same ``LITERALIZER_LINT_CLASSPATH`` the per-fixture compile
host reads).  It shares the same input and comparison logic as the
other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
``kotlinx.serialization.json``'s ``parseToJsonElement`` falls back to a
``Double`` for integer literals that overflow ``Long``, so the 26-digit
value re-emerges as ``1e+26``.  Same shape as the Go, TypeScript, Swift,
Rust and Zig-pre-``std.json.Value`` exclusions.
"""

import shutil
from pathlib import Path

import click

from literalizer import (
    InputFormat,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Kotlin
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Kotlin"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Kotlin script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Kotlin(
            json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT,
        ),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join(result.preamble)
    return (
        f"{preamble}\n"
        f"{result.code}\n"
        "val negativeZero =\n"
        f"    ({_VAR_NAME} as kotlinx.serialization.json.JsonObject)\n"
        '    .getValue("negative_zero").toString().toDouble()\n'
        "check(negativeZero.toRawBits() == Long.MIN_VALUE) {\n"
        '    "negative_zero lost its sign"\n'
        "}\n"
        "print(Json.encodeToString("
        "JsonElement.serializer(), "
        f"{_VAR_NAME}"
        "))\n"
    )


def _check_record_composition(*, step: roundtrip_common.Step) -> None:
    """Reuse independently rendered declarations in a typed native
    call.
    """
    language = Kotlin(
        heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
    )
    declaring = roundtrip_common.literalize_new_variable(
        language=language,
        json_text='{"name":"first","values":[1,2]}',
        var_name="declaring",
        pre_indent_level=0,
    )
    dependent = roundtrip_common.literalize_new_variable(
        language=language,
        json_text='{"name":"second","values":[3,4]}',
        var_name="dependent",
        pre_indent_level=0,
    )
    call = literalize_call(
        source=(
            '[[{"$ref":"declaring"},{"$ref":"dependent"},'
            '{"$ref":"dependent"}]]'
        ),
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("first", "second", "again"),
        ref_key="$ref",
        per_element=True,
    )
    consumer = (
        "fun consume(first: Record0, second: Record0, again: Record0) {",
        '    check(first.name == "first")',
        "    check(first.values.contentEquals(intArrayOf(1, 2)))",
        '    check(second.name == "second")',
        "    check(second.values.contentEquals(intArrayOf(3, 4)))",
        "    check(second === again)",
        '    println("""{"matched":true}""")',
        "}",
    )
    for order, declarations in (
        ("declaring first", (declaring, dependent)),
        ("dependent first", (dependent, declaring)),
    ):
        result = literalize_call_with_declarations(
            language=language,
            declarations=declarations,
            call=call,
            extra_body_preamble=consumer,
        )
        roundtrip_common.execute(
            label=f"{_LABEL} record composition ({order})",
            source_filename="main.kts",
            program=result.code,
            steps=[step],
            excluded_keys=(),
            expected_json='{"matched":true}',
            extra_files=None,
        )


@click.command()
def main() -> None:
    """Round-trip the shared document through the Kotlin backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Kotlin.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    kotlin = shutil.which(cmd="kotlin")
    if kotlin is None or kotlin == "":
        kotlin = "kotlin"
    compiler = (
        Path(kotlin).resolve().parent.parent / "lib" / "kotlin-compiler.jar"
    )
    step = roundtrip_common.Step(
        args=[
            kotlin,
            "-classpath",
            str(object=compiler),
            str(object=Path(__file__).parent / "lint-kotlin.kts"),
            "main.kts",
        ],
        failure_label="kotlin run error",
    )
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.kts",
        program=program,
        steps=[step],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )
    _check_record_composition(step=step)


if __name__ == "__main__":
    main()
