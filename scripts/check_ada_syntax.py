"""Check syntax of an Ada golden file using ``gnatmake``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of the given Ada golden file."""
    filename = sys.argv[1]
    gnatmake_path = shutil.which(cmd="gnatmake") or "gnatmake"
    src = Path(filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = Path(tmpdir) / "check.adb"
        content: str = src.read_text(encoding="utf-8")
        tmp_src.write_text(data=content, encoding="utf-8")
        # `-gnat2022` matches `Ada.language_version` in
        # `src/literalizer/languages/ada.py`; keep them in sync.
        result = subprocess.run(
            args=[gnatmake_path, "-gnat2022", "-gnats", "check.adb"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
    if result.returncode != 0:
        msg = f"{filename}: Ada syntax error\n{result.stderr}"
        sys.stderr.write(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
