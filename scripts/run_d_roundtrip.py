"""D JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a D
``auto my_data = JSONValue(...);`` declaration via the default
``std.json.JSONValue`` model, wrap it in a tiny ``void main`` that
serializes ``my_data`` back to JSON via ``JSONValue.toString`` and writes
it to stdout, compile and run it with ``dmd``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-d`` job in
``.github/workflows/lint.yml``, because that job is where the D
toolchain (``dmd``) is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is trimmed before
literalization: its 26-digit value overflows D's unsigned 64-bit
``ulong`` (the widest integer the ``JSONValue`` integer node can carry
and the widest literal the D backend emits via a ``UL`` suffix), so the
literalizer raises
:class:`literalizer.exceptions.UnrepresentableIntegerError` rather than
emit a decimal literal ``dmd`` would reject.  Same shape as the Go,
TypeScript, Zig, Swift and Rust exclusions.
"""

import shutil

from literalizer.languages import D
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "D"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable D program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=D(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "import std.stdio;\n"
        "void main() {\n"
        f"{result.code}\n"
        f"    write({_VAR_NAME}.toString());\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the D backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dmd = shutil.which(cmd="dmd") or "dmd"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.d",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[dmd, "-of=main", "main.d"],
                failure_label="dmd error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
