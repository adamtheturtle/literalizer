"""Check syntax of a PureScript file using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from scripts.purescript_common import write_lint_environment


def check_fixture(filename: str, *, purs_path: str) -> bool:
    """Compile one fixture in a private workspace."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_purs_paths = write_lint_environment(tmpdir=Path(tmpdir))
        output_dir = Path(tmpdir) / "output"

        result = subprocess.run(
            args=bounded_command(
                args=[
                    purs_path,
                    "compile",
                    filename,
                    *(p.as_posix() for p in env_purs_paths),
                    "-o",
                    output_dir.as_posix(),
                ],
                fixture=filename,
                timeout_seconds=60,
            ),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = (
                f"{filename}: purs compile failed\n"
                f"{result.stderr}{result.stdout}"
            )
            _ = sys.stderr.write(msg)
            return False
    return True


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Check syntax of a single PureScript file."""
    purs_path = shutil.which(cmd="purs")
    if purs_path is None or purs_path == "":
        purs_path = "purs"
    if not check_fixture(filename=filename, purs_path=purs_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
