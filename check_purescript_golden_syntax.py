"""Check syntax of PureScript golden files using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_DATA_TUPLE_STUB = """\
module Data.Tuple where

data Tuple a b = Tuple a b
"""


def main() -> None:
    """Check syntax of each given PureScript golden file."""
    purs_path = shutil.which(cmd="purs") or "purs"
    with tempfile.TemporaryDirectory() as tmpdir:
        stub_path = Path(tmpdir) / "DataTuple.purs"
        stub_path.write_text(data=_DATA_TUPLE_STUB, encoding="utf-8")
        for filename in sys.argv[1:]:
            src = Path(filename)
            target = Path(tmpdir) / "Check.purs"
            target.write_text(
                data=src.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = subprocess.run(
                args=[
                    purs_path,
                    "compile",
                    "Check.purs",
                    "DataTuple.purs",
                ],
                capture_output=True,
                text=True,
                check=False,
                cwd=tmpdir,
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
