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

import roundtrip_common

from literalizer.languages import Scala

_VAR_NAME = "myData"
_LABEL = "Scala"
_CIRCE_DEP = "io.circe::circe-core:0.14.10"


def _build_program(json_text: str) -> str:
    """Return a runnable Scala program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Scala(json_type=Scala.json_types.CIRCE),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=1,
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
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Main.scala",
        program=program,
        steps=[
            roundtrip_common.Step(
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
                failure_label="scala-cli run error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
