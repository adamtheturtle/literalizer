"""Haskell JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Haskell
``myData = ...`` binding (with the generated tagged ``Val`` algebraic
type and the helper ``Num``/``Fractional`` instances that go with it),
wrap it in a cabal-script ``Main`` that serializes ``myData`` back to
JSON via Aeson, run it through ``cabal run``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Haskell roundtrip`` step of the
``lint-haskell-family`` job in ``.github/workflows/lint.yml``, because
that job is where the GHC/cabal toolchain is installed.  It shares the
same input and comparison logic as the other per-language round-trip
helpers.

The generated Haskell ``Val`` algebraic type only carries the
constructors needed for the values that actually appear in the input,
so ``valToValue`` here covers exactly the six variants the shared input
exercises (``HBool``, ``HInt``, ``HFloat``, ``HStr``, ``HList``,
``HMap``).  ``-Wall -Werror`` plus exhaustive pattern matching means a
future expansion of ``roundtrip_input.json`` that adds a new scalar
kind would fail compilation here until ``valToValue`` is extended.
"""

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

# ``default-language: GHC2021`` matches ``Haskell.language_version`` in
# ``src/literalizer/languages/haskell.py``; keep them in sync.
_CABAL_HEADER = """\
{- cabal:
build-depends: base, aeson, bytestring
default-language: GHC2021
ghc-options: -Wall -Werror
-}
"""

# Go through Aeson's ``Encoding`` builder (not ``Value``) so HFloat
# routes through ``E.double``'s shortest-roundtrip formatter. Building
# ``A.Value`` would funnel HFloat through ``Scientific``, where (a) the
# encoder renders integer-valued Scientifics as plain digits regardless
# of magnitude (turning ``1.7976e308`` into a 309-digit integer) and
# (b) ``Scientific.fromFloatDigits (-0.0)`` collapses the sign.
_VAL_TO_ENCODING = """\
valToEncoding :: Val -> E.Encoding
valToEncoding (HBool b) = E.bool b
valToEncoding (HInt n) = E.integer n
valToEncoding (HFloat d) = E.double d
valToEncoding (HStr s) = E.string s
valToEncoding (HList xs) = E.list valToEncoding xs
valToEncoding (HMap kvs) =
    E.pairs (mconcat [E.pair (K.fromString k) (valToEncoding v)
                      | (k, v) <- kvs])
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Haskell cabal-script program for *json_text*."""
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
        f"{_CABAL_HEADER}"
        f"module {_MODULE_NAME} where\n"
        "import qualified Data.Aeson.Encoding as E\n"
        "import qualified Data.Aeson.Key as K\n"
        "import qualified Data.ByteString.Lazy as BL\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"{_VAL_TO_ENCODING}"
        "main :: IO ()\n"
        "main = BL.putStr (E.encodingToLazyByteString"
        f" (valToEncoding {_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Haskell backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        source_path = tmpdir / f"{_MODULE_NAME}.hs"
        source_path.write_text(data=program, encoding="utf-8")
        # ``--verbose=0`` keeps cabal's progress chatter off stdout so
        # only the program's encoded JSON reaches ``run_result.stdout``.
        run_result = subprocess.run(
            args=["cabal", "run", "--verbose=0", str(source_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: cabal run error\n"
            f"{run_result.stdout}{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
