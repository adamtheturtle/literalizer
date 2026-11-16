"""Jsonnet JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Jsonnet
expression, write it to a ``.jsonnet`` file, and evaluate it with the
``jsonnet`` interpreter.  Jsonnet is a JSON superset whose evaluator
emits JSON on stdout, so there is no separate "back to JSON" step: the
interpreter is both the language runtime and the serializer.  The
emitted JSON is then handed to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-go-installed`` job in
``.github/workflows/lint.yml``, because that job is where the
``jsonnet`` binary (installed via ``go install
github.com/google/go-jsonnet/cmd/jsonnet``) is already on the PATH.
It shares the same input and comparison logic as the other
per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison
because Jsonnet numbers are IEEE 754 doubles, so the 26-digit literal
rounds when the evaluator emits it.  Same shape as the Go, TypeScript,
Zig, Rust, and Elm exclusions.

This check declares the shared document with ``NewVariable`` and
evaluates the local binding at the end of the wrapped file.
"""

import shutil

import click

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Jsonnet
from scripts import roundtrip_common

_LABEL = "Jsonnet"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a Jsonnet program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Jsonnet(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    return f"{result.code}\n"


@click.command()
def main() -> None:
    """Round-trip the shared document through the Jsonnet backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Jsonnet.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    jsonnet = shutil.which(cmd="jsonnet")
    if jsonnet is None or jsonnet == "":
        jsonnet = "jsonnet"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.jsonnet",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[jsonnet, "main.jsonnet"],
                failure_label="jsonnet error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )


if __name__ == "__main__":
    main()
