"""Check syntax of a PureScript file using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from scripts.purescript_common import write_lint_environment


def main() -> None:
    """Check syntax of a single PureScript file."""
    filename = sys.argv[1]
    purs_path: str = shutil.which(cmd="purs") or "purs"
    with tempfile.TemporaryDirectory() as tmpdir:
        env_purs_paths = write_lint_environment(tmpdir=Path(tmpdir))
        output_dir = Path(tmpdir) / "output"

        result = subprocess.run(
            args=[
                purs_path,
                "compile",
                filename,
                *(p.as_posix() for p in env_purs_paths),
                "-o",
                output_dir.as_posix(),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = (
                f"{filename}: purs compile failed\n"
                f"{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
