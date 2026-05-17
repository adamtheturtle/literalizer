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


def expected() -> object:
    """Return the parsed value the round-trip must reproduce."""
    return json.loads(s=read_input())


def verify(label: str, produced_json: str) -> None:
    """Compare *produced_json* to :func:`expected`, exiting 1 on mismatch.

    *label* names the language for the diagnostic.  JSON object key order
    is irrelevant because the comparison is on parsed Python values.
    """
    want = expected()
    try:
        got = json.loads(s=produced_json)
    except json.JSONDecodeError as exc:
        sys.stderr.write(
            f"{label}: produced invalid JSON ({exc})\n{produced_json!r}\n",
        )
        sys.exit(1)
    if got != want:
        sys.stderr.write(
            f"{label}: round-trip mismatch\n"
            f"  expected: {want!r}\n"
            f"  got:      {got!r}\n",
        )
        sys.exit(1)
