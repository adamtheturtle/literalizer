"""Check syntax of a V golden file using ``v fmt``.

``v fmt`` parses the file and rewrites it in canonical form.  If parsing
fails the exit code is non-zero, which we treat as a syntax error.
We deliberately do **not** use ``v fmt -verify`` because the
literalizer's output style (trailing commas in maps, no colon
alignment) differs from V's canonical formatting while still being
syntactically valid.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    """Check syntax of the given V golden file."""
    filename = sys.argv[1]
    v_path = shutil.which(cmd="v") or "v"
    src = Path(filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / src.name
        target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = subprocess.run(
            args=[v_path, "fmt", target],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: v fmt failed\n{result.stderr}{result.stdout}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
