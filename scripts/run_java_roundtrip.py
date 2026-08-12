"""Java JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Java
``var myData = ...;`` declaration, wrap it in a tiny ``Main`` whose
``main`` prints ``new ObjectMapper().writeValueAsString(myData)``,
compile that with Jackson on the classpath, run it, and hand the
emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Java roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the JDK toolchain and the Jackson jars (set up for the
``Java(json_type=...)`` lint pass via ``LITERALIZER_LINT_CLASSPATH``)
are installed; it is deliberately not a pytest test under ``tests/``.
"""

import os
import shutil

from literalizer.languages import Java
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Java"


def _build_main(json_text: str) -> str:
    """Return a runnable ``Main`` program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Java(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    imports = "\n".join(result.preamble)
    body_preamble = "\n".join(result.body_preamble)
    indented_decl = result.code.replace("\n", "\n        ")
    return (
        f"{imports}\n"
        "import com.fasterxml.jackson.databind.ObjectMapper;\n"
        f"{body_preamble}\n"
        "public class Main {\n"
        "    public static void main(String[] args) throws Exception {\n"
        f"        {indented_decl}\n"
        "        java.io.PrintStream out = new java.io.PrintStream(\n"
        '            System.out, true, "UTF-8");\n'
        "        out.print(new ObjectMapper().writeValueAsString(\n"
        f"            {_VAR_NAME}));\n"
        "        out.flush();\n"
        "    }\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Java backend."""
    program = _build_main(json_text=roundtrip_common.read_input())
    javac = shutil.which(cmd="javac") or "javac"
    java = shutil.which(cmd="java") or "java"
    classpath = os.environ["LITERALIZER_LINT_CLASSPATH"] + os.pathsep + "."
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Main.java",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[javac, "-cp", classpath, "Main.java"],
                failure_label="javac error",
            ),
            roundtrip_common.Step(
                args=[java, "-cp", classpath, "Main"],
                failure_label="java runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
