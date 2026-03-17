"""Check syntax of Swift golden files using swiftc."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Swift golden file."""
    swiftc_path = shutil.which(cmd="swiftc")

    if swiftc_path is None:
        return
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmpdir:
            swift_path = Path(tmpdir) / "check.swift"
            swift_path.write_text(data=content, encoding="utf-8")
            result = subprocess.run(
                args=[swiftc_path, "-typecheck", swift_path],
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
