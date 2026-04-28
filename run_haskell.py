"""Compile and run a Haskell golden fixture via GHC.

Most fixtures declare only ``my_data`` with no ``main``; for those we
compile a generated ``Main.hs`` wrapper that forces evaluation of it.
Call fixtures (stem ending ``_call``) define their own ``main`` and are
compiled directly with ``-main-is <module>``.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

_MAIN_TEMPLATE = """\
module Main where

import {mod}

main :: IO ()
main = seq {mod}.my_data (return ())
"""


def main() -> None:
    """Compile and run the given Haskell golden file."""
    filename = sys.argv[1]
    src = Path(filename)
    mod = src.stem
    is_call = mod.endswith("_call")

    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)

        if is_call:
            compile_args = [
                "ghc",
                "-Wall",
                "-Werror",
                "-main-is",
                mod,
                "-outputdir",
                str(tmpdir),
                "-o",
                str(tmpdir / "run"),
                str(src),
            ]
        else:
            main_hs = tmpdir / "Main.hs"
            main_hs.write_text(
                data=_MAIN_TEMPLATE.format(mod=mod),
                encoding="utf-8",
            )
            compile_args = [
                "ghc",
                "-Wall",
                "-Werror",
                "-outputdir",
                str(tmpdir),
                "-o",
                str(tmpdir / "run"),
                str(main_hs),
                str(src),
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
            args=[str(tmpdir / "run")],
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
