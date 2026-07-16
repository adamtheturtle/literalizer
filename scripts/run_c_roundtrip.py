"""C JSON round-trip check (issue #2641).

Literalize the shared ``roundtrip_input.json`` document to a C
``cJSON *my_data = ...;`` declaration via ``C(json_type=CJSON)``, wrap
it in a tiny ``main`` that prints ``cJSON_PrintUnformatted(my_data)`` to
stdout, compile with ``clang -std=c99 -lcjson``, run it, and hand the
emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``C roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job
is where the C toolchain (``clang``) is installed by the ``Lint C``
step; the ``libcjson-dev`` apt package is installed by the same job.
It shares the same input and comparison logic as the other
per-language round-trip helpers.

C ships no standard-library JSON encoder.  ``C(json_type=CJSON)``
(issue #2766) literalizes the document directly into a ``cJSON`` node
tree -- one ``cJSON_Create*`` call per node, composed with
``cJSON_AddItemToArray`` / ``cJSON_AddItemToObject`` -- so this helper
just calls ``cJSON_PrintUnformatted`` and no longer walks the parsed
JSON in Python (mirroring the C++ / Haskell / Zig / Crystal round-trip
scripts).

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
  tree; excluded from the comparison rather than fixed.
"""

import shutil

from literalizer.languages import C
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "C"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")


def _build_program(*, json_text: str) -> str:
    """Return a runnable C program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=C(json_type=C.json_types.CJSON),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "#include <stdio.h>\n"
        "#include <stdlib.h>\n"
        "int main(void) {\n"
        f"{result.code}\n"
        f"    char *out = cJSON_PrintUnformatted({_VAR_NAME});\n"
        "    fputs(out, stdout);\n"
        "    free(out);\n"
        f"    cJSON_Delete({_VAR_NAME});\n"
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
