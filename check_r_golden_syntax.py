"""Check syntax of R golden files using ``Rscript``."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given R golden file."""
    rscript_path = shutil.which(cmd="Rscript")

    if rscript_path is None:
        return
    result = subprocess.run(
        args=[
            rscript_path,
            "-e",
            "for (f in commandArgs(trailingOnly=TRUE)) parse(file=f)",
            *sys.argv[1:],
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = f"R syntax error\n{result.stderr}"
        sys.stderr.write(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
