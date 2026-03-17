"""Check syntax of Ada golden files using ``gnatmake``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of each given Ada golden file."""
    gnatmake_path = shutil.which(cmd="gnatmake") or "gnatmake"
    for filename in sys.argv[1:]:
        src = Path(filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_src = Path(tmpdir) / "check.adb"
            content: str = src.read_text()
            tmp_src.write_text(data=content)
            try:
                result = subprocess.run(
                    args=[gnatmake_path, "-gnats", "check.adb"],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=tmpdir,
                )
            except FileNotFoundError:
                # gnatmake not installed - skip check
                continue
        if result.returncode != 0:
            msg = f"{filename}: Ada syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
