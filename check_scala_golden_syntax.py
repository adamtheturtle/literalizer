"""Check syntax of Scala golden files using ``scalac``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Scala golden file."""
    scalac_path: str = shutil.which(cmd="scalac") or "scalac"
    for filename in sys.argv[1:]:
        path = Path(filename).resolve()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                args=[scalac_path, str(path)],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: Scala syntax error\n"
                f"{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
