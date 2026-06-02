"""COBOL JSON round-trip check (issue #2643).

Literalize the shared ``roundtrip_input.json`` document to a COBOL
``01 MY-DATA.`` group (WORKING-STORAGE level items), wrap it in a tiny
``CHECK`` program whose PROCEDURE DIVISION re-emits JSON with the
standard ``JSON GENERATE`` statement, ``cobc``-compile and run that
program, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Cobol roundtrip`` step of the
``lint-cobol`` job in ``.github/workflows/lint.yml``, because that job
is where the pinned GnuCOBOL toolchain is installed; ``uv run`` (project
mode, not ``--no-project``) is required so ``import literalizer``
resolves.  It is deliberately not a pytest test under ``tests/``.

GnuCOBOL ships ``JSON GENERATE`` as its standard JSON encoder, so this
helper uses it rather than hand-rolling a serializer (the issue's
prefer-a-library rule).  ``JSON GENERATE`` constrains what can be
re-emitted, which is why the shared input is heavily trimmed before
literalization (see ``_EXCLUDED_KEYS``):

* The literalizer mangles each JSON key to a COBOL data name (``int`` ->
  ``F-INT``); the ``NAME OF`` clause below renames each item back to its
  original key, so only top-level scalars whose data name is recoverable
  participate.
* Booleans are stored as ``PIC X(5)`` strings (``"TRUE"`` / ``"FALSE"``)
  and would re-emit as JSON strings, not JSON booleans.
* Floats are stored as ``COMP-2``; GnuCOBOL's ``JSON GENERATE`` does not
  implement floating-point items ("attempt to use non-implemented JSON
  I/O").
* Sequences and sets are stored as groups of ``FILLER`` items, which
  ``JSON GENERATE`` omits, so arrays cannot be reconstructed.
* Nested objects re-emit fine structurally but their keys are likewise
  mangled, and there is no per-element ``NAME OF`` target for items
  nested below the top level, so they are excluded too.
* ``string_empty`` is stored as ``PIC X(1)`` (a single space), so it
  cannot represent the empty string: a COBOL ``PIC X`` item has a
  one-byte minimum and that byte holds a space, not nothing.
* ``biginteger`` overflows COBOL's widest integer literal, so the
  literalizer raises
  :class:`literalizer.exceptions.UnrepresentableIntegerError` before any
  source is produced (same exclusion shape as the Go / TypeScript / C
  scripts).

Every remaining top-level scalar -- signed integers, the 32-bit-
overflowing ``long``, and plain / escaped / unicode strings -- round-
trips losslessly through ``JSON GENERATE`` (the ``PIC X`` items are
sized by UTF-8 byte length, so multibyte values are no longer
truncated).
"""

import json
import re
import shutil

import roundtrip_common

from literalizer.languages import Cobol

_VAR_NAME = "my_data"
_LABEL = "Cobol"
_EXCLUDED_KEYS = (
    "biginteger",
    "float",
    "float_large_exponent",
    "negative_zero",
    "bool_true",
    "bool_false",
    "string_empty",
    "empty_array",
    "int_array",
    "double_array",
    "bool_array",
    "mixed_array",
    "nested_array",
    "empty_object",
    "flat_object",
    "nested_object",
)

# The literalized group opens ``01 MY-DATA.`` followed by one
# ``05 F-... PIC ...`` elementary item per surviving key, in document
# order.  Pull those data names out so each can be renamed back to its
# original JSON key in the ``NAME OF`` clause; matching against the
# emitted code (rather than reimplementing the key-to-name mangling)
# keeps this in step with the COBOL backend.
_DATA_NAME_RE = re.compile(
    pattern=r"^\s*05\s+(F-[A-Z0-9-]+)\s",
    flags=re.MULTILINE,
)


def _build_program(*, json_text: str) -> str:
    """Return a runnable ``CHECK`` program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Cobol(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    keys = list(json.loads(s=trimmed_json).keys())
    data_names = _DATA_NAME_RE.findall(string=result.code)
    if len(data_names) != len(keys):
        message = (
            f"{_LABEL}: expected one COBOL data name per key, "
            f"got {data_names!r} for {keys!r}"
        )
        raise RuntimeError(message)
    rename_lines = "\n".join(
        f'             {name} IS "{key}"'
        for name, key in zip(data_names, keys, strict=True)
    )
    # ``result.code`` already prepends any ``body_preamble`` lines ahead
    # of the declaration, which is exactly where they belong inside
    # WORKING-STORAGE; COBOL defines none, so this is just the group.
    group = result.code
    return (
        "IDENTIFICATION DIVISION.\n"
        "PROGRAM-ID. CHECK.\n"
        "DATA DIVISION.\n"
        "WORKING-STORAGE SECTION.\n"
        f"{group}\n"
        "01 JSON-OUT PIC X(4000).\n"
        "01 JSON-LEN PIC 9(9) COMP.\n"
        "PROCEDURE DIVISION.\n"
        "    JSON GENERATE JSON-OUT FROM MY-DATA COUNT IN JSON-LEN\n"
        "        NAME OF MY-DATA IS OMITTED\n"
        f"{rename_lines}\n"
        "    END-JSON.\n"
        "    DISPLAY JSON-OUT(1:JSON-LEN).\n"
        "    STOP RUN.\n"
    )


def main() -> None:
    """Round-trip the shared document through the COBOL backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    cobc = shutil.which(cmd="cobc") or "cobc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="check.cob",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[cobc, "-x", "-free", "check.cob", "-o", "check"],
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
