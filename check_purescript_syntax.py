"""Check syntax of a PureScript file using ``purs compile``."""

import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


def main() -> None:
    """Check syntax of a single PureScript file."""
    prelude_purs_content = textwrap.dedent(
        text="""\
        module Prelude where
        foreign import negate :: forall a. a -> a
        foreign import div :: forall a. a -> a -> a
        infixl 7 div as /
        """,
    )
    prelude_js_content = textwrap.dedent(
        text="""\
        export const negate = x => -x;
        export const div = x => y => x / y;
        """,
    )
    filename = sys.argv[1]
    purs_path: str = shutil.which(cmd="purs") or "purs"
    with tempfile.TemporaryDirectory() as tmpdir:
        prelude_purs = Path(tmpdir) / "Prelude.purs"
        prelude_js = Path(tmpdir) / "Prelude.js"
        prelude_purs.write_text(data=prelude_purs_content, encoding="utf-8")
        prelude_js.write_text(data=prelude_js_content, encoding="utf-8")
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
