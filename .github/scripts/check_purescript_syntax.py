"""Check syntax of a PureScript file using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from purescript_common import PRELUDE_JS, PRELUDE_PURS


def main() -> None:
    """Check syntax of a single PureScript file."""
    filename = sys.argv[1]
    purs_path: str = shutil.which(cmd="purs") or "purs"
    with tempfile.TemporaryDirectory() as tmpdir:
        prelude_purs = Path(tmpdir) / "Prelude.purs"
        prelude_js = Path(tmpdir) / "Prelude.js"
        prelude_purs.write_text(data=PRELUDE_PURS, encoding="utf-8")
        prelude_js.write_text(data=PRELUDE_JS, encoding="utf-8")
        output_dir = Path(tmpdir) / "output"

        result = subprocess.run(
            args=[
                purs_path,
                "compile",
                filename,
                prelude_purs.as_posix(),
                "-o",
                output_dir.as_posix(),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = (
                f"{filename}: purs compile failed\n"
                f"{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
