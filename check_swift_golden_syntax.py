"""Check syntax of Swift golden files using swiftc."""

import shutil
import subprocess
import sys


def main() -> None:
    """Check syntax of each given Swift golden file."""
    swiftc_path = shutil.which(cmd="swiftc") or "swiftc"
    for filename in sys.argv[1:]:
        result = subprocess.run(
            args=[swiftc_path, "-typecheck", filename],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: Swift syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
