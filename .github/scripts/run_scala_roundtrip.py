"""Scala JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Scala
``val myData: io.circe.Json = ...`` declaration (via
``json_type=Scala.JsonTypes.CIRCE``), wrap it in a tiny ``@main`` that
prints ``myData.noSpaces``, run it with ``scala-cli``, and hand the
emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-scala`` job in
``.github/workflows/lint.yml``, because that job is where the Scala
toolchain (``scala-cli``) and the ``circe-core`` dependency are
configured.  It shares the same input and comparison logic as the other
per-language round-trip helpers.

Circe's ``Json.fromBigInt`` round-trips the 26-digit ``biginteger``
field losslessly via ``noSpaces``, so no top-level keys need excluding.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Scala

_VAR_NAME = "myData"
_LABEL = "Scala"
_CIRCE_DEP = "io.circe::circe-core:0.14.10"


def _build_program(json_text: str) -> str:
    """Return a runnable Scala program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Scala(json_type=Scala.JsonTypes.CIRCE),
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "\n"
        "@main def runRoundtrip(): Unit = {\n"
        f"{result.code}\n"
        f"    print({_VAR_NAME}.noSpaces)\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Scala backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    scala_cli = shutil.which(cmd="scala-cli") or "scala-cli"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "Main.scala").write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[
                scala_cli,
                "run",
                ".",
                "-S",
                "3",
                "--dep",
                _CIRCE_DEP,
                "--main-class",
                "runRoundtrip",
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: scala-cli run error\n"
            f"{run_result.stdout}{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
