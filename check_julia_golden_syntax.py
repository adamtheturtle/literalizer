"""Check syntax of Julia golden files using Julia."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given Julia golden file."""
    julia_path = shutil.which(cmd="julia") or "julia"
    for filename in sys.argv[1:]:
        result = subprocess.run(
            args=[
                julia_path,
                "--startup-file=no",
                "-e",
                "Meta.parseall(read(ARGS[1], String))",
                "--",
                filename,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: Julia syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
