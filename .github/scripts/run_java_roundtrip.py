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
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Java

_SCRIPT_DIR = Path(__file__).resolve().parent
_SERIALIZER_SRC = _SCRIPT_DIR / "JavaRoundtripSerializer.java"
_VAR_NAME = "myData"
_LABEL = "Java"


def _build_main(json_text: str) -> str:
    """Return a runnable ``Main`` program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Java(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
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
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "Main.java").write_text(data=program, encoding="utf-8")
        shutil.copy(src=_SERIALIZER_SRC, dst=tmpdir / _SERIALIZER_SRC.name)
        compile_result = subprocess.run(
            args=[javac, "Main.java", _SERIALIZER_SRC.name],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: javac error\n{compile_result.stdout}"
                f"{compile_result.stderr}",
            )
            sys.exit(1)
        run_result = subprocess.run(
            args=[java, "Main"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: java runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
