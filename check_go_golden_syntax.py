"""Check syntax of Go golden files using gofmt."""

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Check syntax of each given Go golden file."""
    gofmt_path = shutil.which(cmd="gofmt") or "gofmt"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8").strip()
        wrapped = f"package main\n\nvar _ = {content}\n"
        result = subprocess.run(
            args=[gofmt_path, "-e"],
            input=wrapped,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: Go syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
