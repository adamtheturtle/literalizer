"""Check syntax of an Ada golden file using ``gnatmake``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from scripts.fixture_staging import stage_ada_fixture


def check_fixture(*, fixture: Path, gnatmake_path: str) -> bool:
    """Check syntax of one staged Ada fixture."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = stage_ada_fixture(fixture=fixture, workspace=Path(tmpdir))
        # `-gnat2022` matches `Ada.language_version` in
        # `src/literalizer/languages/ada.py`; keep them in sync.
        result = subprocess.run(
            args=bounded_command(
                args=[
                    gnatmake_path,
                    "-gnat2022",
                    "-gnatwe",
                    "-Werror",
                    "-gnats",
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
    if result.returncode != 0:
        msg = f"{fixture}: Ada syntax error\n{result.stderr}"
        _ = sys.stderr.write(msg)
        return False

    return True


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Check syntax of the given Ada golden file."""
    gnatmake_path = shutil.which(cmd="gnatmake")
    if gnatmake_path is None or gnatmake_path == "":
        gnatmake_path = "gnatmake"
    if not check_fixture(fixture=Path(filename), gnatmake_path=gnatmake_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
