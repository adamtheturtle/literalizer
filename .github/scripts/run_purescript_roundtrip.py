"""PureScript JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a PureScript
``myData :: Val`` declaration, wrap it in a ``Check`` module whose
``toJson`` walker turns the generated ``Val`` ADT into a JSON string
(deferring scalar formatting to the JavaScript runtime's
``JSON.stringify`` through small foreign-import wrappers), compile that
module with
``purs compile``, run the emitted JavaScript under Node so a top-level
binding writes the JSON to stdout, and hand the result to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-haskell-family`` job in
``.github/workflows/lint.yml``, because that job is where the ``purs``
binary (from ``setup-purescript``) and Node are already installed.  It
shares the same input and comparison logic as the other per-language
round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows PureScript's ``Int`` (a 32-bit value on the
JavaScript backend) and the literalizer raises before it can be emitted,
so the field is dropped from the literalized document and from the
comparison.  Same shape as the Elm exclusion.

The literalized output uses the custom ``Val`` ADT defined in
``src/literalizer/languages/purescript.py``; there is no off-the-shelf
serializer for it, so the ``toJson`` walker below maps each constructor
to a JSON fragment.  Scalar formatting (numbers, strings) is delegated
to the runtime's built-in ``JSON.stringify`` via foreign imports, so
the round-trip
relies on the standard JSON formatter for the tricky bits (escapes,
negative zero, large exponents) rather than re-implementing them.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common
from purescript_common import PRELUDE_JS, PRELUDE_PURS

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import PureScript

_VAR_NAME = "myData"
_LABEL = "PureScript"
_EXCLUDED_KEYS = ("biginteger",)

# Full ``Val`` type with every constructor the PureScript backend can
# emit, not just the ones present in the trimmed input, so ``toJson``
# below stays exhaustive if the fixture later grows ``PNull`` / ``PSet``
# cases.  Replaces the body_preamble (which only lists the constructors
# actually used by the data).
_VAL_TYPE = """\
import Prelude

data Tuple a b = Tuple a b

data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PLong Number
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
    | PSet (Array Val)
"""

# Walker that turns ``Val`` into a JSON string.  Scalar formatting is
# delegated to the JavaScript runtime's ``JSON.stringify`` through the
# foreign imports below, so escapes, negative zero, and large exponents
# follow the standard JSON formatter rather than a hand-rolled one.
_TO_JSON = """\
foreign import append :: String -> String -> String
infixr 5 append as <>

foreign import stringifyBool :: Boolean -> String
foreign import stringifyInt :: Int -> String
foreign import stringifyNumber :: Number -> String
foreign import stringifyString :: String -> String
foreign import joinArray
    :: forall a. (a -> String) -> String -> Array a -> String
foreign import emit :: String -> Unit

toJson :: Val -> String
toJson v = case v of
    PNull -> "null"
    PBool b -> stringifyBool b
    PInt i -> stringifyInt i
    PLong n -> stringifyNumber n
    PFloat n -> stringifyNumber n
    PStr s -> stringifyString s
    PList xs -> "[" <> joinArray toJson "," xs <> "]"
    PDict kvs -> "{" <> joinArray entryToJson "," kvs <> "}"
    PSet xs -> "[" <> joinArray toJson "," xs <> "]"

entryToJson :: Tuple String Val -> String
entryToJson kv = case kv of
    Tuple k w -> stringifyString k <> ":" <> toJson w
"""

# Top-level ``result`` is strict in PureScript, so importing the
# compiled module forces ``emit (toJson myData)`` to run, writing the
# JSON to stdout.
_FOOTER = f"""\

result :: Unit
result = emit (toJson {_VAR_NAME})
"""

# FFI implementations for the foreign imports above.  ``JSON.stringify``
# handles the scalar formatting; the array/dict cases are walked in
# PureScript via ``joinArray``.
_CHECK_JS = """\
export const append = a => b => a + b;
export const stringifyBool = b => JSON.stringify(b);
export const stringifyInt = i => JSON.stringify(i);
export const stringifyNumber = n => JSON.stringify(n);
export const stringifyString = s => JSON.stringify(s);
export const joinArray = f => sep => xs => xs.map(x => f(x)).join(sep);
export const emit = s => { process.stdout.write(s); return {}; };
"""

# Dynamic import of the compiled ``Check`` module so Node evaluates its
# top-level bindings (including ``result``, whose RHS calls ``emit``).
# Mirrors the driver used by ``run_purescript.py``.
_NODE_DRIVER = (
    "import('./output/Check/index.js')"
    ".catch(e => {"
    " console.error(e && e.stack ? e.stack : e);"
    " process.exit(1);"
    " })"
)


def _build_check(json_text: str) -> str:
    """Return a runnable PureScript ``Check`` module from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=PureScript(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    body_preamble_text = "\n".join(result.body_preamble)
    declaration = result.code
    if declaration.startswith(body_preamble_text):
        declaration = declaration[len(body_preamble_text) :].lstrip("\n")
    return (
        "module Check where\n\n"
        f"{_VAL_TYPE}\n"
        f"{declaration}\n\n"
        f"{_TO_JSON}"
        f"{_FOOTER}"
    )


def main() -> None:
    """Round-trip the shared document through the PureScript backend."""
    program = _build_check(json_text=roundtrip_common.read_input())
    purs = shutil.which(cmd="purs") or "purs"
    node = shutil.which(cmd="node") or "node"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        prelude_purs = tmpdir / "Prelude.purs"
        prelude_js = tmpdir / "Prelude.js"
        prelude_purs.write_text(data=PRELUDE_PURS, encoding="utf-8")
        prelude_js.write_text(data=PRELUDE_JS, encoding="utf-8")
        check_purs = tmpdir / "Check.purs"
        check_js = tmpdir / "Check.js"
        check_purs.write_text(data=program, encoding="utf-8")
        check_js.write_text(data=_CHECK_JS, encoding="utf-8")
        output_dir = tmpdir / "output"
        compile_result = subprocess.run(
            args=[
                purs,
                "compile",
                check_purs.as_posix(),
                prelude_purs.as_posix(),
                "-o",
                output_dir.as_posix(),
            ],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: purs compile error\n"
                f"{compile_result.stdout}{compile_result.stderr}",
            )
            sys.stderr.write(f"\nProgram:\n{program}\n")
            sys.exit(1)
        run_result = subprocess.run(
            args=[node, "--input-type=module", "-e", _NODE_DRIVER],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: node run error\n"
            f"{run_result.stdout}{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
