"""Java JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Java
``var myData = ...;`` declaration, wrap it in a tiny ``Main`` whose
``main`` prints ``JavaRoundtripSerializer.toJson(myData)``, compile that
together with ``JavaRoundtripSerializer.java`` (copied from this
directory, the same ``run_ada.py`` + ``a_stub.*`` pattern), run it, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Java roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the JDK toolchain is installed; it is deliberately not a pytest
test under ``tests/``.  It is the template for further per-language
``run_<lang>_roundtrip.py`` helpers sharing one input document.
"""

import shutil
from pathlib import Path

import roundtrip_common

from literalizer.languages import Java

_SCRIPT_DIR = Path(__file__).resolve().parent
_SERIALIZER_SRC = _SCRIPT_DIR / "JavaRoundtripSerializer.java"
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
        f"{body_preamble}\n"
        "public class Main {\n"
        "    public static void main(String[] args) throws Exception {\n"
        f"        {indented_decl}\n"
        "        java.io.PrintStream out = new java.io.PrintStream(\n"
        '            System.out, true, "UTF-8");\n'
        "        out.print(JavaRoundtripSerializer.toJson(\n"
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
    serializer_text = _SERIALIZER_SRC.read_text(encoding="utf-8")
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Main.java",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[javac, "Main.java", _SERIALIZER_SRC.name],
                failure_label="javac error",
            ),
            roundtrip_common.Step(
                args=[java, "Main"],
                failure_label="java runtime error",
            ),
        ],
        excluded_keys=(),
        extra_files={_SERIALIZER_SRC.name: serializer_text},
    )


if __name__ == "__main__":
    main()
