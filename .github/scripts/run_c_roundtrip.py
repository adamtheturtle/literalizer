"""C JSON round-trip check (issue #2641).

Literalize the shared ``roundtrip_input.json`` document to a C
``CVal my_data = ((CVal){.m = (CKV[]){...}});`` declaration, wrap it
in a tiny ``main`` that builds a parallel ``cJSON`` tree from
``my_data`` and prints it via ``cJSON_PrintUnformatted``, compile with
``clang -std=c99 -lcjson``, run it, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``C roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job
is where the C toolchain (``clang``) is installed by the ``Lint C``
step; the ``libcjson-dev`` apt package is installed by the same job.
It shares the same input and comparison logic as the other
per-language round-trip helpers.

C ships no standard-library JSON encoder.  The literalizer's ``CVal``
is also an *untagged* union -- the run-time carries no discriminator
that would let a generic walker decide which member of ``.b`` /
``.i`` / ``.f`` / ``.s`` / ``.a`` / ``.m`` is live.  So the *shape*
of the round-trip document is encoded into the generated ``main`` by
walking the parsed JSON in Python (same pattern as the Forth / Tcl
helpers) and emitting one ``cJSON_Create*`` call per node that reads
the slot matching the original JSON type.  Leaf escaping and number
formatting are then handled by cJSON itself.

This shape-driven walk is the consequence of ``CVal`` being untagged
rather than of cJSON: any encoder (hand-rolled or otherwise) would
need the same per-node dispatch.  Issue #2763 tracks adding a
``C(json_type=...)`` knob that literalizes directly to a cJSON tree,
which would let this helper drop the walker and just call
``cJSON_PrintUnformatted`` (mirroring the C++ / Haskell / Zig /
Crystal round-trip scripts).

Two fields are excluded from the comparison:

* ``biginteger`` -- its 26-digit value overflows the unsigned 64-bit
  range (the widest C literal the literalizer emits, via a ``ULL``
  suffix), so the literalizer raises
  :class:`literalizer.exceptions.UnrepresentableIntegerError`; trimmed
  before literalization so ``clang`` is not asked to compile an
  oversize literal.  Same shape as the Go, TypeScript, Zig, Swift,
  Rust, D, C++, Crystal and Odin exclusions.
* ``float_large_exponent`` -- cJSON's ``print_number`` uses
  ``snprintf("%1.15g", ...)`` with a 17-digit fallback that rejects
  any value whose rounded form lies outside the input's exact bits.
  For ``1.7976931348623157e+308`` (DBL_MAX) the 15-digit rounding
  yields ``1.79769313486232e+308``, which parses as ``inf`` (it
  exceeds DBL_MAX) and trips the fallback test, so cJSON emits the
  rounded value anyway and the round-trip sees ``inf``.  The
  truncation happens inside cJSON's printer, not in the literalized
  literal; excluded from the comparison rather than fixed.
"""

import json
import shutil

import roundtrip_common

from literalizer.languages import C

# ``json.loads`` returns this recursive shape; typing the walker
# against it lets ``isinstance`` narrow cleanly under pyright,
# pyrefly, and ty without ``cast``.
type JsonValue = (
    None
    | bool
    | int
    | float
    | str
    | list["JsonValue"]
    | dict[str, "JsonValue"]
)

_VAR_NAME = "my_data"
_LABEL = "C"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")


def _scalar_create(*, value: bool | float | str, access: str) -> str:
    """Return a ``cJSON_Create*(...)`` expression for the *value* leaf.

    ``bool`` is checked before ``int`` because Python treats ``True``
    / ``False`` as ``int`` instances; both share the integer storage
    slot in ``CVal`` but reach for different union members.  All
    numbers go through ``cJSON_CreateNumber``, which takes a
    ``double``; the integer ``access.i`` is widened explicitly so the
    cast is visible in the generated source.
    """
    if isinstance(value, bool):
        return f"cJSON_CreateBool({access}.b)"
    if isinstance(value, int):
        return f"cJSON_CreateNumber((double){access}.i)"
    if isinstance(value, float):
        return f"cJSON_CreateNumber({access}.f)"
    return f"cJSON_CreateString({access}.s)"


def _walk(
    *,
    value: JsonValue,
    access: str,
    name: str,
    lines: list[str],
) -> None:
    """Append C statements that build a cJSON node from *access*.

    The generated statements declare a fresh ``cJSON *<name>`` for
    *value* and, for containers, recursively build each child with a
    suffixed name before attaching it.  *access* is a C expression
    evaluating to the ``CVal`` slot for *value*; the walker descends
    through ``.a[i]`` for arrays and ``.m[i].v`` for objects, matching
    the literalizer's ``(CVal[]){...}`` / ``(CKV[]){...}`` shape.
    ``roundtrip_input`` is deliberately null-free.
    """
    if isinstance(value, list):
        lines.append(f"cJSON *{name} = cJSON_CreateArray();")
        for index, element in enumerate(value):
            child = f"{name}_{index}"
            _walk(
                value=element,
                access=f"{access}.a[{index}]",
                name=child,
                lines=lines,
            )
            lines.append(f"cJSON_AddItemToArray({name}, {child});")
        return
    if isinstance(value, dict):
        lines.append(f"cJSON *{name} = cJSON_CreateObject();")
        for index, sub in enumerate(value.values()):
            child = f"{name}_{index}"
            _walk(
                value=sub,
                access=f"{access}.m[{index}].v",
                name=child,
                lines=lines,
            )
            lines.append(
                f"cJSON_AddItemToObject({name}, "
                f"{access}.m[{index}].k, {child});",
            )
        return
    if value is None:
        message = "unsupported JSON null in round-trip input"
        raise TypeError(message)
    lines.append(
        f"cJSON *{name} = {_scalar_create(value=value, access=access)};",
    )


def _build_program(*, json_text: str) -> str:
    """Return a runnable C program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=C(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    parsed: JsonValue = json.loads(s=trimmed_json)
    build_lines: list[str] = []
    _walk(value=parsed, access=_VAR_NAME, name="root", lines=build_lines)
    build_body = "\n    ".join(build_lines)
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "#include <stdio.h>\n"
        "#include <stdlib.h>\n"
        "#include <cjson/cJSON.h>\n"
        "int main(void) {\n"
        f"{result.code}\n"
        f"    {build_body}\n"
        "    char *out = cJSON_PrintUnformatted(root);\n"
        "    fputs(out, stdout);\n"
        "    free(out);\n"
        "    cJSON_Delete(root);\n"
        "    return 0;\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the C backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    clang = shutil.which(cmd="clang") or "clang"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.c",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[clang, "-std=c99", "main.c", "-lcjson", "-o", "main"],
                failure_label="clang error",
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
