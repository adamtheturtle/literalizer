"""Check syntax of Groovy golden files using ``groovyc``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Groovy golden file."""
    groovyc_path: str = shutil.which(cmd="groovyc") or "groovyc"
    for filename in sys.argv[1:]:
        path = Path(filename).resolve()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                args=[groovyc_path, "-d", tmpdir, path.as_posix()],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: Groovy syntax error\n"
                f"{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
