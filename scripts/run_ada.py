"""Compile and run an Ada golden file against the ``A_Stub`` package.

The fixtures declare ``my_data : A_Val := <literal>;`` using container
aggregate syntax that depends on the Ada 2022 ``Aggregate``
aspect. ``gnatmake`` resolves the ``with A_Stub;`` clause against the
``a_stub.ads`` / ``a_stub.adb`` pair copied alongside each fixture.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from scripts.fixture_staging import stage_ada_fixture

_REPO_ROOT = Path(__file__).resolve().parent
_STUB_SOURCES = ("a_stub.ads", "a_stub.adb")


def check_fixture(*, fixture: Path, gnatmake_path: str) -> bool:
    """Compile and execute one Ada fixture with its support files."""
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        tmp_src = stage_ada_fixture(fixture=fixture, workspace=tmpdir)
        for stub_name in _STUB_SOURCES:
            _ = shutil.copy(src=_REPO_ROOT / stub_name, dst=tmpdir / stub_name)
        # `-gnat2022` matches `Ada.language_version` in
        # `src/literalizer/languages/ada.py`; keep them in sync.
        compile_result = subprocess.run(
            args=bounded_command(
                args=[
                    gnatmake_path,
                    "-gnat2022",
                    "-gnatwe",
                    "-Werror",
                    tmp_src.name,
                ],
                fixture=str(object=fixture),
                timeout_seconds=60,
            ),
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
        if compile_result.returncode != 0:
            _ = sys.stderr.write(
                f"{fixture}: Ada compile error\n{compile_result.stdout}"
                f"{compile_result.stderr}",
            )
            return False
        run_result = subprocess.run(
            args=bounded_command(
                args=[tmp_src.with_suffix(suffix="")],
                fixture=str(object=fixture),
                timeout_seconds=60,
            ),
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
    if run_result.returncode != 0:
        _ = sys.stderr.write(
            f"{fixture}: Ada runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        return False

    return True


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Compile and run the given Ada golden file."""
    gnatmake_path = shutil.which(cmd="gnatmake")
    if gnatmake_path is None or gnatmake_path == "":
        gnatmake_path = "gnatmake"
    if not check_fixture(fixture=Path(filename), gnatmake_path=gnatmake_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
