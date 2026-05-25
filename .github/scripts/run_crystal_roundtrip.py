"""Crystal JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Crystal
``my_data = JSON.parse(%(...))`` assignment via
``Crystal(json_type=JSON_ANY)``, append a ``print my_data.to_json``
statement, compile and run the resulting program with ``crystal run``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-crystal`` job in
``.github/workflows/lint.yml``, because that job is where the Crystal
toolchain is already installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value overflows the ``Int64`` integer node
that Crystal's ``JSON.parse`` exposes, same shape as the Go,
TypeScript, Zig, Swift, Rust, D and C++ exclusions.  The
``string_escapes`` field is excluded because the
``Crystal(json_type=JSON_ANY)`` backend rejects literal backslashes and
double quotes inside string values: they would be reinterpreted by the
``%(...)`` percent literal before the JSON parser sees them.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Crystal

_VAR_NAME = "my_data"
_LABEL = "Crystal"
_EXCLUDED_KEYS = ("biginteger", "string_escapes")


def _build_program(json_text: str) -> str:
    """Return a runnable Crystal program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Crystal(json_type=Crystal.json_types.JSON_ANY),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\nprint {_VAR_NAME}.to_json\n"


def main() -> None:
    """Round-trip the shared document through the Crystal backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    crystal = shutil.which(cmd="crystal") or "crystal"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.cr"
        src.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[crystal, "run", str(object=src)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: crystal run error\n"
            f"{run_result.stdout}{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
