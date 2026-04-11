"""Check syntax of an Ada golden file using ``gnatmake``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_syntax_helpers import fail_on_error


def main() -> None:
    """Check syntax of the given Ada golden file."""
    filename = sys.argv[1]
    gnatmake_path = shutil.which(cmd="gnatmake") or "gnatmake"
    src = Path(filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = Path(tmpdir) / "check.adb"
        content: str = src.read_text(encoding="utf-8")
        tmp_src.write_text(data=content, encoding="utf-8")
        result = subprocess.run(
            args=[gnatmake_path, "-gnats", "check.adb"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
        )
    fail_on_error(
        result=result,
        filename=filename,
        label="Ada syntax error",
    )


if __name__ == "__main__":
    main()
