"""Shared pieces for the per-language JSON round-trip checks (#1867).

Every ``run_<lang>_roundtrip.py`` helper literalizes the SAME single
``roundtrip_input.json`` document to its language, compiles and runs the
result so it re-emits JSON on stdout, then calls :func:`verify` here to
assert the emitted JSON parses back to the original value.  Keeping the
input and the comparison in one module means a new language only has to
add the language-specific literalize + toolchain glue.

The shared document is deliberately ``null``-free: several backends drop
null map values or cannot infer the type of a bare ``null``.  Per-value
type coverage (wide ints, large-exponent / negative-zero floats, unicode
and escaped strings, empty/nested arrays and objects, heterogeneous
arrays) lives in that one file rather than in many small cases.
"""

import json
import sys
from pathlib import Path

INPUT_PATH = Path(__file__).resolve().parent / "roundtrip_input.json"


def read_input() -> str:
    """Return the shared round-trip JSON document as text."""
    return INPUT_PATH.read_text(encoding="utf-8")


def expected() -> dict[str, object]:
    """Return the parsed value the round-trip must reproduce.

    The shared ``roundtrip_input.json`` document is a top-level JSON
    object, so the parsed value is always a ``dict``.
    """
    parsed: dict[str, object] = json.loads(s=read_input())
    return parsed


def verify(
    label: str,
    produced_json: str,
    exclude_keys: tuple[str, ...],
) -> None:
    """Compare *produced_json* to :func:`expected`, exiting 1 on mismatch.

    *label* names the language for the diagnostic.  JSON object key order
    is irrelevant because the comparison is on parsed Python values.

    *exclude_keys* drops the named top-level object keys from both sides
    before comparing.  This is for languages whose JSON number type
    cannot represent a value in the shared input losslessly (e.g. the
    wide ``biginteger`` field in TypeScript, where the literalized
    program collapses the 26-digit literal to a JS ``number`` before
    serialization).  Pass ``()`` when no field needs to be skipped.
    """
    want = expected()
    try:
        got: dict[str, object] = json.loads(s=produced_json)
    except json.JSONDecodeError as exc:
        sys.stderr.write(
            f"{label}: produced invalid JSON ({exc})\n{produced_json!r}\n",
        )
        sys.exit(1)
    for key in exclude_keys:
        want.pop(key, None)
        got.pop(key, None)
    if got != want:
        sys.stderr.write(
            f"{label}: round-trip mismatch\n"
            f"  expected: {want!r}\n"
            f"  got:      {got!r}\n",
        )
        sys.exit(1)
