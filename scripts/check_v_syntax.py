"""Check a V golden file using ``v fmt`` and ``v -check``.

``v fmt`` parses the file and rewrites it in canonical form.  If parsing
fails the exit code is non-zero, which we treat as a syntax error.
We deliberately do **not** use ``v fmt -verify`` because the
literalizer's output style (trailing commas in maps, no colon
alignment) differs from the canonical formatting while still being
syntactically valid.

``v -check`` additionally type-checks the source without linking it.
This catches invalid interface conversions such as a generated
heterogeneous collection whose elements cannot inhabit ``IVal``.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def check_fixture(*, fixture: Path, v_path: str) -> bool:
    """Check the syntax and types of one staged V fixture."""
    src = fixture
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / src.name
        _ = target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = subprocess.run(
            args=bounded_command(
                args=[v_path, "fmt", target],
                fixture=str(object=fixture),
                timeout_seconds=60,
            ),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{fixture}: v fmt failed\n{result.stderr}{result.stdout}"
            _ = sys.stderr.write(msg)
            return False
        result = subprocess.run(
            args=bounded_command(
                args=[v_path, "-W", "-check", target],
                fixture=str(object=fixture),
                timeout_seconds=60,
            ),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{fixture}: v -check failed\n{result.stderr}{result.stdout}"
            _ = sys.stderr.write(msg)
            return False

    return True


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Check syntax of the given V golden file."""
    v_path = shutil.which(cmd="v")
    if v_path is None or v_path == "":
        v_path = "v"
    if not check_fixture(fixture=Path(filename), v_path=v_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
