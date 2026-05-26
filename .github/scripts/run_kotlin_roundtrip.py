"""Kotlin JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Kotlin
``val myData: JsonElement = ...`` declaration under
``json_type=Kotlin.JsonTypes.KOTLINX_JSON_ELEMENT`` (so the binding is a
``kotlinx.serialization.json.JsonElement`` tree built via
``Json.parseToJsonElement``), wrap it in a tiny ``.kts`` script that
prints ``Json.encodeToString(JsonElement.serializer(), myData)`` to
stdout, run it with ``kotlin``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-kotlin`` job in
``.github/workflows/lint.yml``, because that job is where the Kotlin
toolchain and the ``kotlinx-serialization-json`` jars are already
installed (same ``LITERALIZER_LINT_CLASSPATH`` the per-fixture compile
host reads).  It shares the same input and comparison logic as the
other per-language round-trip helpers.

``kotlinx.serialization.json`` preserves numbers verbatim through
``parseToJsonElement``/``encodeToString``, so the shared input's
26-digit ``biginteger`` field needs no exclusion under this strategy
(superseding the hand-rolled Jackson walker from issue #2709).
"""

import os
import shutil
from pathlib import Path

import roundtrip_common

from literalizer.languages import Kotlin

_VAR_NAME = "myData"
_LABEL = "Kotlin"


def _build_program(json_text: str) -> str:
    """Return a runnable Kotlin script literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Kotlin(json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join(result.preamble)
    return (
        f"{preamble}\n"
        f"{result.code}\n"
        "print(Json.encodeToString("
        "JsonElement.serializer(), "
        f"{_VAR_NAME}"
        "))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Kotlin backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    kotlin = shutil.which(cmd="kotlin") or "kotlin"
    # ``LITERALIZER_LINT_CLASSPATH`` is set by the ``lint-kotlin`` job
    # to ``/tmp/kotlinx-jars/*`` for the per-fixture compile host.  The
    # ``kotlin`` script wrapper does not forward the JVM ``dir/*``
    # wildcard intact, so expand it here to an explicit jar list.
    classpath = ":".join(
        sorted(
            str(p)
            for entry in os.environ["LITERALIZER_LINT_CLASSPATH"].split(":")
            for p in (
                Path(entry.removesuffix("/*")).glob("*.jar")
                if entry.endswith("/*")
                else [Path(entry)]
            )
        ),
    )
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.kts",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[kotlin, "-classpath", classpath, "main.kts"],
                failure_label="kotlin run error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
