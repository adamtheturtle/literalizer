"""Check syntax of Scala golden files using scalac."""

import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    """Check syntax of each given Scala golden file."""
    scalac_path = shutil.which(cmd="scalac")
    if scalac_path is None:
        return
    for filename in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                args=[scalac_path, "-d", tmpdir, filename],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode != 0:
            msg = f"{filename}: Scala syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
