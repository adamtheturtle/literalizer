"""Check syntax of a PureScript file using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_syntax_helpers import fail_on_error

_PRELUDE_PURS = """\
module Prelude where
foreign import negate :: forall a. a -> a
foreign import div :: forall a. a -> a -> a
infixl 7 div as /
"""

_PRELUDE_JS = """\
export const negate = x => -x;
export const div = x => y => x / y;
"""


def main() -> None:
    """Check syntax of a single PureScript file."""
    filename = sys.argv[1]
    purs_path: str = shutil.which(cmd="purs") or "purs"
    with tempfile.TemporaryDirectory() as tmpdir:
        prelude_purs = Path(tmpdir) / "Prelude.purs"
        prelude_js = Path(tmpdir) / "Prelude.js"
        prelude_purs.write_text(data=_PRELUDE_PURS, encoding="utf-8")
        prelude_js.write_text(data=_PRELUDE_JS, encoding="utf-8")
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
        fail_on_error(
            result=result,
            filename=filename,
            label="purs compile failed",
        )


if __name__ == "__main__":
    main()
