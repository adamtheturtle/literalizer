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

The helpers below collapse the boilerplate shared across the per-language
scripts: :func:`trim_keys` drops the language-specific lossy fields from
the input JSON before re-serialization, :func:`literalize_new_variable`
wraps the one ``literalize`` shape every script uses, and
:func:`execute` writes the assembled program to a tmpdir, runs a chain
of :class:`Step` subprocesses (compile then run, or just run), and hands
the final stdout to :func:`verify`.
"""

import json
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from literalizer import (
    InputFormat,
    Language,
    LiteralizeResult,
    NewVariable,
    literalize,
)

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


def trim_keys(json_text: str, excluded_keys: tuple[str, ...]) -> str:
    """Return *json_text* with *excluded_keys* removed at the top level.

    Mirrors the round-trip ``verify`` exclusion: scripts whose backend
    cannot represent a particular field losslessly trim it *before*
    literalization so the generated program does not need to carry a
    value the toolchain would reject (e.g. an integer that overflows
    the target's widest literal type).
    """
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in excluded_keys:
        parsed.pop(key, None)
    return json.dumps(obj=parsed)


def literalize_new_variable(
    *,
    language: Language,
    json_text: str,
    var_name: str,
    pre_indent_level: int,
) -> LiteralizeResult:
    """Literalize *json_text* into a ``NewVariable(var_name)`` binding.

    Wraps the single ``literalize(...)`` shape every per-language
    round-trip script uses: JSON input, ``include_delimiters=True``,
    ``wrap_in_file=False`` so the caller can splice the declaration
    into its own ``main``/module template.
    """
    return literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=True,
        variable_form=NewVariable(name=var_name),
        wrap_in_file=False,
    )


@dataclass(frozen=True)
class Step:
    """A subprocess to run inside the per-script tmpdir.

    *args* is the argv (cwd is always the tmpdir).  *failure_label* is
    the short phrase :func:`execute` prefixes to stderr when the step's
    exit code is non-zero (e.g. ``"rustc error"``, ``"go run error"``).
    """

    args: Sequence[str]
    failure_label: str


def execute(
    *,
    label: str,
    source_filename: str,
    program: str,
    steps: Sequence[Step],
    excluded_keys: tuple[str, ...],
    extra_files: Mapping[str, str] | None = None,
) -> None:
    """Run *program* through *steps* and verify the final stdout.

    Writes *program* to ``<tmpdir>/<source_filename>`` (parent dirs
    created on demand) and each ``extra_files`` entry under the same
    tmpdir, then runs each :class:`Step` with cwd set to that tmpdir.
    The first non-zero exit aborts with a diagnostic that includes the
    failing step's stdout/stderr and a dump of *program*.

    On success, the *last* step's stdout is passed to :func:`verify`
    with *label* and *excluded_keys*, and a ``"{label} round-trip OK"``
    line is written to stdout.  Callers do not need to emit that line
    themselves.
    """
    extras = extra_files or {}
    last_stdout = ""
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        source_path = tmpdir / source_filename
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(data=program, encoding="utf-8")
        for rel_path, content in extras.items():
            extra_path = tmpdir / rel_path
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(data=content, encoding="utf-8")
        for step in steps:
            result = subprocess.run(
                args=list(step.args),
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
                encoding="utf-8",
            )
            if result.returncode != 0:
                sys.stderr.write(
                    f"{label}: {step.failure_label}\n"
                    f"{result.stdout}{result.stderr}",
                )
                sys.stderr.write(f"\nProgram:\n{program}\n")
                sys.exit(1)
            last_stdout = result.stdout
    verify(
        label=label,
        produced_json=last_stdout,
        exclude_keys=excluded_keys,
    )
    sys.stdout.write(f"{label} round-trip OK\n")
