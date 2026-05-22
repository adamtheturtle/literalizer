"""Haskell JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Haskell
``myData = ...`` binding (with the generated tagged ``Val`` algebraic
type and the helper ``Num``/``Fractional`` instances that go with it),
wrap it in a tiny module that serializes ``myData`` back to JSON via a
hand-written ``toJson :: Val -> String``, compile and run it with GHC,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Haskell roundtrip`` step of the
``lint-haskell-family`` job in ``.github/workflows/lint.yml``, because
that job is where the GHC toolchain is installed.  It shares the same
input and comparison logic as the other per-language round-trip
helpers.

The literalized Haskell ``Val`` algebraic type only carries the
constructors needed for the values that actually appear in the input,
so ``toJson`` here covers exactly the six variants the shared input
exercises (``HBool``, ``HInt``, ``HFloat``, ``HStr``, ``HList``,
``HMap``).  If a future expansion of ``roundtrip_input.json`` adds a
new scalar kind, both this serializer and the Haskell backend's ``Val``
type would grow together.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Haskell

_VAR_NAME = "myData"
_LABEL = "Haskell"
_MODULE_NAME = "Main"

_TO_JSON = """\
toJson :: Val -> String
toJson (HBool True) = "true"
toJson (HBool False) = "false"
toJson (HInt n) = show n
toJson (HFloat d) = show d
toJson (HStr s) = encodeStr s
toJson (HList xs) = "[" ++ intercalate "," (map toJson xs) ++ "]"
toJson (HMap kvs) =
    "{" ++ intercalate "," (map kv kvs) ++ "}"
  where
    kv (k, v) = encodeStr k ++ ":" ++ toJson v

encodeStr :: String -> String
encodeStr s = "\\"" ++ concatMap escapeChar s ++ "\\""

escapeChar :: Char -> String
escapeChar '"' = "\\\\\\""
escapeChar '\\\\' = "\\\\\\\\"
escapeChar '\\n' = "\\\\n"
escapeChar '\\r' = "\\\\r"
escapeChar '\\t' = "\\\\t"
escapeChar c
    | ord c < 0x20 =
        let h = showHex (ord c) ""
        in "\\\\u" ++ replicate (4 - length h) '0' ++ h
    | otherwise = [c]
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Haskell program literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Haskell(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    # ``Haskell.literalize`` already inlines ``result.body_preamble``
    # (the ``data Val`` declaration and its instances) at the top of
    # ``result.code``, so we only join ``preamble`` (file-level pragmas)
    # with ``code`` here. Prepending ``body_preamble`` separately would
    # duplicate the ``Val`` type and break compilation.
    preamble = "\n".join(result.preamble)
    return (
        f"module {_MODULE_NAME} where\n"
        "import Data.Char (ord)\n"
        "import Data.List (intercalate)\n"
        "import Numeric (showHex)\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"{_TO_JSON}"
        "main :: IO ()\n"
        f"main = putStr (toJson {_VAR_NAME})\n"
    )


def main() -> None:
    """Round-trip the shared document through the Haskell backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ghc = shutil.which(cmd="ghc") or "ghc"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        source_path = tmpdir / f"{_MODULE_NAME}.hs"
        source_path.write_text(data=program, encoding="utf-8")
        binary_path = tmpdir / "run"
        # ``-XGHC2021`` matches ``Haskell.language_version``; ``-Wall
        # -Werror`` matches the policy of the ``Lint Haskell`` step.
        compile_result = subprocess.run(
            args=[
                ghc,
                "-XGHC2021",
                "-Wall",
                "-Werror",
                "-outputdir",
                str(tmpdir / "build"),
                "-o",
                str(binary_path),
                str(source_path),
            ],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: ghc compile error\n{compile_result.stdout}"
                f"{compile_result.stderr}",
            )
            sys.stderr.write(f"\nProgram:\n{program}\n")
            sys.exit(1)
        run_result = subprocess.run(
            args=[str(binary_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: runtime error\n{run_result.stdout}{run_result.stderr}",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
