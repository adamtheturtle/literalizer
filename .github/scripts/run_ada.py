"""Compile and run an Ada golden file against the ``A_Stub`` package.

The fixtures declare ``my_data : A_Val := <literal>;`` using container
aggregate syntax that depends on the stub's Ada 2022 ``Aggregate``
aspect. ``gnatmake`` resolves the ``with A_Stub;`` clause against the
``a_stub.ads`` / ``a_stub.adb`` pair copied alongside each fixture.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
_STUB_SOURCES = ("a_stub.ads", "a_stub.adb")


def main() -> None:
    """Compile and run the given Ada golden file."""
    filename = sys.argv[1]
    gnatmake_path = shutil.which(cmd="gnatmake") or "gnatmake"
    src = Path(filename)
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        tmp_src = tmpdir / "check.adb"
        tmp_src.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        for stub_name in _STUB_SOURCES:
            shutil.copy(src=_REPO_ROOT / stub_name, dst=tmpdir / stub_name)
        # `-gnat2022` matches `Ada.language_version` in
        # `src/literalizer/languages/ada.py`; keep them in sync.
        compile_result = subprocess.run(
            args=[gnatmake_path, "-gnat2022", "check.adb"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{filename}: Ada compile error\n{compile_result.stdout}"
                f"{compile_result.stderr}",
            )
            sys.exit(1)
        run_result = subprocess.run(
            args=[tmpdir / "check"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{filename}: Ada runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
