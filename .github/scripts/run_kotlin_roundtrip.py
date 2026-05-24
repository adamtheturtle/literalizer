"""Kotlin JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Kotlin
``val myData = ...`` declaration, wrap it in a tiny ``.kts`` script
that walks the generated ``Any?`` value into a
``kotlinx.serialization.json.JsonElement`` and prints
``Json.encodeToString(...)`` to stdout, run it with ``kotlin``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-kotlin`` job in
``.github/workflows/lint.yml``, because that job is where the Kotlin
toolchain and the ``kotlinx-serialization-json`` jars are already
installed (same ``LITERALIZER_LINT_CLASSPATH`` the per-fixture compile
host reads).  It shares the same input and comparison logic as the
other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value is emitted as ``java.math.BigInteger("...")`` which
``kotlinx.serialization.json`` has no first-class ``JsonPrimitive``
overload for, same shape as the Go, TypeScript and Zig exclusions.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Kotlin

_VAR_NAME = "myData"
_LABEL = "Kotlin"
_EXCLUDED_KEYS = ("biginteger",)

# Recursive ``Any?`` -> ``JsonElement`` walker.  The Kotlin backend
# emits primitive-typed arrays (``intArrayOf``, ...) for homogeneous
# numeric lists, so each primitive-array shape needs its own branch
# before the generic ``List<*>`` arm.  ``Map<*, *>`` covers both
# ``mapOf<String, Any?>`` and the narrower homogeneous-value maps the
# backend emits for inner objects.
_TO_JSON_ELEMENT = r"""
fun toJsonElement(v: Any?): JsonElement = when (v) {
    null -> JsonNull
    is Boolean -> JsonPrimitive(v)
    is Number -> JsonPrimitive(v)
    is String -> JsonPrimitive(v)
    is IntArray -> JsonArray(v.map { JsonPrimitive(it) })
    is LongArray -> JsonArray(v.map { JsonPrimitive(it) })
    is DoubleArray -> JsonArray(v.map { JsonPrimitive(it) })
    is BooleanArray -> JsonArray(v.map { JsonPrimitive(it) })
    is List<*> -> JsonArray(v.map(::toJsonElement))
    is Map<*, *> -> JsonObject(
        v.entries.associate { (k, vv) -> k.toString() to toJsonElement(vv) }
    )
    else -> error("unhandled type: " + v::class)
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Kotlin script literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Kotlin(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "import kotlinx.serialization.json.Json\n"
        "import kotlinx.serialization.json.JsonArray\n"
        "import kotlinx.serialization.json.JsonElement\n"
        "import kotlinx.serialization.json.JsonNull\n"
        "import kotlinx.serialization.json.JsonObject\n"
        "import kotlinx.serialization.json.JsonPrimitive\n"
        f"{preamble}\n"
        f"{_TO_JSON_ELEMENT}"
        "\n"
        f"{result.code}\n"
        "\n"
        "print(Json.encodeToString("
        "JsonElement.serializer(), "
        f"toJsonElement({_VAR_NAME})"
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
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "main.kts").write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[kotlin, "-classpath", classpath, "main.kts"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: kotlin run error\n"
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
