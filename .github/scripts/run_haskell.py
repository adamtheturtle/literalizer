"""Compile and run a Haskell golden fixture via GHC.

Every fixture defines its own ``main`` entry point under a
``module Fixture_<case>_<variant> where`` declaration, so each is
compiled with ``-main-is <module>`` using the declared module name.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def _module_name(*, src: Path) -> str:
    """Return the module name from the ``module … where`` declaration line."""
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("module "):
            return line.split()[1]
    return src.stem


def main() -> None:
    """Compile and run the given Haskell golden file."""
    filename = sys.argv[1]
    src = Path(filename)
    mod = _module_name(src=src)

    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)

        compile_args = [
            "ghc",
            "-Wall",
            "-Werror",
            "-main-is",
            mod,
            "-outputdir",
            str(object=tmpdir),
            "-o",
            str(object=tmpdir / "run"),
            str(object=src),
        ]

        compile_result = subprocess.run(
            args=compile_args,
            capture_output=True,
            text=True,
            check=False,
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{filename}: GHC compile error\n{compile_result.stdout}"
                f"{compile_result.stderr}",
            )
            sys.exit(1)

        run_result = subprocess.run(
            args=[str(object=tmpdir / "run")],
            capture_output=True,
            text=True,
            check=False,
        )

    if run_result.returncode != 0:
        sys.stderr.write(
            f"{filename}: Haskell runtime error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
