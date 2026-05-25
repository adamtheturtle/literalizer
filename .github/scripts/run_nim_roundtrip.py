"""Nim JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Nim
``var myData: JsonNode = %*(...)`` declaration via the
``json_type=JSON_NODE`` strategy, wrap it in a tiny program that prints
``$myData`` (Nim's ``$`` for :class:`json.JsonNode` emits JSON), compile
and run it under ``nim c -r``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Nim roundtrip`` step of the
``lint-nim`` job in ``.github/workflows/lint.yml``, because that job is
where the Nim toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The serializer is Nim's standard-library ``std/json`` module rather
than a hand-rolled encoder (matching the preference expressed in the
issue notes).

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows Nim's widest integer type, so the
literalizer rejects the value with
:class:`literalizer.exceptions.UnrepresentableIntegerError` before the
program is even produced.  Same shape as the Go, TypeScript, Zig,
Swift, Rust, D, and C++ exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import Nim

_VAR_NAME = "myData"
_LABEL = "Nim"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Nim program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Nim(json_type=Nim.json_types.JSON_NODE),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\nstdout.write(${_VAR_NAME})\n"


def main() -> None:
    """Round-trip the shared document through the Nim backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    nim = shutil.which(cmd="nim") or "nim"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.nim",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    nim,
                    "c",
                    "-r",
                    "--hints:off",
                    "--warnings:off",
                    "--nimcache:.",
                    "main.nim",
                ],
                failure_label="nim c -r error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
