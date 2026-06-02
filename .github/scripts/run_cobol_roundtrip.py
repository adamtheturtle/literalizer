"""COBOL JSON round-trip check (issue #2790).

Literalize the shared ``roundtrip_input.json`` document to a COBOL
``cJSON *`` node tree via ``Cobol(json_type=CJSON)``, wrap it in a tiny
``CHECK`` program whose PROCEDURE DIVISION re-emits JSON with
``cJSON_PrintUnformatted``, ``cobc``-compile and run that program, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Cobol roundtrip`` step of the
``lint-cobol`` job in ``.github/workflows/lint.yml``, because that job
is where the pinned GnuCOBOL toolchain (and ``libcjson-dev``) is
installed; ``uv run`` (project mode, not ``--no-project``) is required
so ``import literalizer`` resolves.  It is deliberately not a pytest
test under ``tests/``.

The default record mode round-trip (issue #2643) used GnuCOBOL's
built-in ``JSON GENERATE``, which loses information as a JSON
encoder: keys are recovered out of mangled COBOL data names, booleans
and the empty string have no representation, floats are rejected, and
arrays / objects are dropped.  ``Cobol(json_type=CJSON)`` (issue #2790,
mirroring C's #2766 / #2767) instead builds the document directly as a
``cJSON`` node tree through COBOL's C ``CALL`` interface -- one
``cJSON_Create*`` CALL per node, composed with ``cJSON_AddItemTo*`` --
so arbitrary string keys, JSON booleans, real numbers, heterogeneous
arrays, nested objects, and the empty string all round-trip.  This
helper therefore no longer reverse-engineers the key mapping in Python:
it literalizes, prints, and compares, like the C / C++ / Haskell / Zig
scripts.

``wrap_in_file=True`` already yields the complete cJSON-building
``CHECK`` program (the WORKING-STORAGE pointer / literal items and the
PROCEDURE DIVISION ``CALL`` tree ending in ``SET my_data`` and ``STOP
RUN``), so the only surgery is splicing in the print storage and the
print statements -- no manual program template, and no reach into the
backend's private division-split marker.

Two fields are excluded from the comparison (the same two as the C
``cJSON`` round-trip):

* ``biginteger`` -- its 26-digit value overflows the signed 64-bit
  range (the widest integer literal the COBOL backend emits), so the
  literalizer raises
  :class:`literalizer.exceptions.UnrepresentableIntegerError`; trimmed
  before literalization.  Same shape as the C / Go / TypeScript / Zig
  exclusions.
* ``float_large_exponent`` -- cJSON's own ``print_number``
  (``snprintf("%1.15g", ...)`` with a 17-digit fallback) rounds
  ``1.7976931348623157e+308`` (DBL_MAX) to a value that parses as
  ``inf``, so cJSON emits the rounded form anyway.  The truncation
  happens inside cJSON's printer, not in the literalized tree -- a
  limitation inherited verbatim from the C round-trip, not a COBOL one.
"""

import shutil

import roundtrip_common

import literalizer
from literalizer.languages import Cobol

_VAR_NAME = "my_data"
_LABEL = "Cobol"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")

# The COBOL data name the binding pointer is declared under (the cJSON
# document root).
_DATA_NAME = _VAR_NAME.upper().replace("_", "-")

# The PROCEDURE DIVISION indent the backend emits.  Derived rather than
# hard-coded as ``"    "`` so a future ``Cobol.indent`` change relocates
# the ``STOP RUN`` anchor and the print statements together instead of
# silently de-syncing.
_INDENT = Cobol().indent

# Extra WORKING-STORAGE items the print step needs: the pointer
# ``cJSON_PrintUnformatted`` returns, its ``strlen`` (so the exact JSON
# bytes are displayed without the trailing spaces of a fixed-width PIC),
# and a BASED window over the returned C string.
_PRINT_STORAGE = (
    "01 JSON-PTR USAGE POINTER.\n"
    "01 JSON-LEN PIC 9(9) COMP-5.\n"
    "01 JSON-OUT PIC X(16000) BASED.\n"
)

_PRINT_STATEMENTS = (
    f'{_INDENT}CALL "cJSON_PrintUnformatted" USING BY VALUE '
    f"{_DATA_NAME} RETURNING JSON-PTR.\n"
    f"{_INDENT}SET ADDRESS OF JSON-OUT TO JSON-PTR.\n"
    f'{_INDENT}CALL "strlen" USING BY VALUE JSON-PTR RETURNING JSON-LEN.\n'
    f"{_INDENT}DISPLAY JSON-OUT(1:JSON-LEN).\n"
)


def _splice_once(*, program: str, anchor: str, replacement: str) -> str:
    """Return *program* with its sole occurrence of *anchor* replaced by
    *replacement*.

    Raise :class:`RuntimeError` naming the missing anchor if it does not
    occur exactly once, so a future change to the generated program's
    textual shape fails loudly here rather than as a confusing
    downstream compile / empty-output error.
    """
    count = program.count(anchor)
    if count != 1:
        msg = (
            f"Expected exactly one occurrence of anchor {anchor!r} in the "
            f"generated COBOL program to splice the print step into, but "
            f"found {count}; the backend's output shape has drifted."
        )
        raise RuntimeError(msg)
    return program.replace(anchor, replacement, 1)


def _build_program(*, json_text: str) -> str:
    """Return a runnable ``CHECK`` program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = literalizer.literalize(
        source=trimmed_json,
        input_format=literalizer.InputFormat.JSON,
        language=Cobol(json_type=Cobol.json_types.CJSON),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=literalizer.NewVariable(name=_VAR_NAME),
        wrap_in_file=True,
    )
    stop_run_anchor = f"{_INDENT}STOP RUN."
    with_storage = _splice_once(
        program=result.code,
        anchor="WORKING-STORAGE SECTION.\n",
        replacement=f"WORKING-STORAGE SECTION.\n{_PRINT_STORAGE}",
    )
    program = _splice_once(
        program=with_storage,
        anchor=stop_run_anchor,
        replacement=f"{_PRINT_STATEMENTS}{stop_run_anchor}",
    )
    return f"{program}\n"


def main() -> None:
    """Round-trip the shared document through the COBOL cJSON backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    cobc = shutil.which(cmd="cobc") or "cobc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="check.cob",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    cobc,
                    "-x",
                    "-free",
                    "check.cob",
                    "-o",
                    "check",
                    "-lcjson",
                ],
                failure_label="cobc error",
            ),
            roundtrip_common.Step(
                args=["./check"],
                failure_label="run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
