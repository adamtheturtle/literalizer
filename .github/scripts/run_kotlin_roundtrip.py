"""Kotlin JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Kotlin
``val myData = ...`` declaration, wrap it in a tiny ``.kts`` script that
prints ``ObjectMapper().writeValueAsString(myData)`` to stdout, run it
with ``kotlin``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-kotlin`` job in
``.github/workflows/lint.yml``, because that job is where the Kotlin
toolchain and the Jackson jars are already installed (same
``LITERALIZER_LINT_CLASSPATH`` the per-fixture compile host reads).  It
shares the same input and comparison logic as the other per-language
round-trip helpers.

Jackson's ``ObjectMapper`` serializes the heterogeneous ``Any?`` tree
the literalizer emits, including the primitive-typed arrays
(``intArrayOf``, ``longArrayOf``, ...) the Kotlin backend uses for
homogeneous numeric lists, without a hand-rolled walker (issue #2709).

The shared input's ``biginteger`` field is excluded from the comparison
for parity with the Go, TypeScript, Swift, and Zig exclusions: those
backends collapse the 26-digit literal before serialization.  Kotlin
emits it as ``java.math.BigInteger("...")`` and Jackson serializes it as
an exact JSON number, but keeping the exclusion matches the other
``LongArray``-shaped backends.
"""

import os
import shutil
from pathlib import Path

import roundtrip_common

from literalizer.languages import Kotlin

_VAR_NAME = "myData"
_LABEL = "Kotlin"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Kotlin script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Kotlin(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "import com.fasterxml.jackson.databind.ObjectMapper\n"
        f"{preamble}\n"
        f"{result.code}\n"
        "\n"
        f"print(ObjectMapper().writeValueAsString({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Kotlin backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    kotlin = shutil.which(cmd="kotlin") or "kotlin"
    # ``LITERALIZER_LINT_CLASSPATH`` is set by the ``lint-kotlin`` job
    # to ``/tmp/jackson-jars/*`` for this round-trip step.  The
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
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
