"""Go JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Go
``myData := ...`` declaration, wrap it in a tiny ``main`` that prints
``json.Marshal(myData)``, run it with ``go run``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-go`` job in
``.github/workflows/lint.yml``, because that job is where the Go
toolchain is invoked.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows ``uint64`` (the widest Go integer literal
type the literalizer emits), so the program would not compile if the
field were kept.  Every other field round-trips through ``encoding/json``
losslessly under the parsed-value comparison in
:func:`roundtrip_common.verify`.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Go

_VAR_NAME = "myData"
_LABEL = "Go"
_EXCLUDED_KEYS = ("biginteger",)

# ``go 1.18`` matches ``Go.language_version`` in
# ``src/literalizer/languages/go.py`` and the ``go.mod`` written by the
# ``Check Go compilation and run`` step of ``lint-go``; keep them in
# sync.
_GO_MOD = "module fixture\n\ngo 1.18\n"


def _build_program(json_text: str) -> str:
    """Return a runnable Go program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Go(),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "\n"
        "import (\n"
        '\t"encoding/json"\n'
        '\t"fmt"\n'
        '\t"os"\n'
        ")\n"
        "\n"
        "func main() {\n"
        f"{result.code}\n"
        f"\tout, err := json.Marshal({_VAR_NAME})\n"
        "\tif err != nil {\n"
        "\t\tfmt.Fprintln(os.Stderr, err)\n"
        "\t\tos.Exit(1)\n"
        "\t}\n"
        "\tos.Stdout.Write(out)\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Go backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    go = shutil.which(cmd="go") or "go"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "main.go").write_text(data=program, encoding="utf-8")
        (tmpdir / "go.mod").write_text(data=_GO_MOD, encoding="utf-8")
        run_result = subprocess.run(
            args=[go, "run", "."],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: go run error\n{run_result.stdout}{run_result.stderr}",
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
