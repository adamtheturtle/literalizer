"""Elm JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Elm
``myData : Val`` declaration, wrap it in a tiny ``port`` module that
walks the generated ``Val`` ADT into a ``Json.Encode.Value`` and ships
the serialized JSON back to a Node wrapper through a port, compile that
module with ``elm make``, run the emitted JavaScript under Node so the
port subscription writes the JSON to stdout, and hand the result to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-elm-run`` job in
``.github/workflows/lint.yml``, because that job is where the ``elm``
binary (from ``.github/npm-linters``) and Node 22 are already installed.
It shares the same input and comparison logic as the other per-language
round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows the Elm ``Int`` range (Elm ``Int`` is a JS
``Number`` underneath, so the 26-digit literal does not compile to a
finite ``Int``).  Same shape as the Go, TypeScript, Zig, and Rust
exclusions.

The literalized output uses the custom ``Val`` ADT defined in
``src/literalizer/languages/elm.py``; there is no off-the-shelf
serializer for it, so the ``valToJson`` walker below maps each
constructor to the matching ``Json.Encode`` call.  The standard
``elm/json`` library does the actual JSON formatting once the ADT has
been translated.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Elm

_VAR_NAME = "myData"
_LABEL = "Elm"
_EXCLUDED_KEYS = ("biginteger",)

# elm.json with ``elm/json`` promoted to a direct dependency so
# ``import Json.Encode`` resolves; the rest mirrors the shared
# ``ELM_JSON`` from ``elm_common.py``.
_ELM_JSON = json.dumps(
    obj={
        "type": "application",
        "source-directories": ["src"],
        "elm-version": "0.19.1",
        "dependencies": {
            "direct": {
                "elm/core": "1.0.5",
                "elm/json": "1.1.3",
            },
            "indirect": {},
        },
        "test-dependencies": {"direct": {}, "indirect": {}},
    },
)

# Node wrapper.  ``Elm.Main.init`` returns synchronously; the runtime
# processes the ``init`` ``Cmd`` (which calls ``output``) on the next
# tick, so the synchronous ``subscribe`` call below is registered before
# the port fires.
_RUN_JS = """\
const { Elm } = require('./main.js');
const app = Elm.Main.init();
app.ports.output.subscribe((s) => {
    process.stdout.write(s);
});
"""

# Encoder mapping each ``Val`` constructor to ``Json.Encode``.  Covers
# all eight constructors the Elm backend can emit, not just the ones
# present in the trimmed input, so the encoder stays valid if the
# fixture later grows ``ENull`` / ``ESet`` cases.
_VAL_TO_JSON = """\
valToJson : Val -> Encode.Value
valToJson v =
    case v of
        ENull ->
            Encode.null

        EBool b ->
            Encode.bool b

        EInt i ->
            Encode.int i

        EFloat f ->
            Encode.float f

        EStr s ->
            Encode.string s

        EList xs ->
            Encode.list valToJson xs

        EDict kvs ->
            Encode.object (List.map (\\( k, w ) -> ( k, valToJson w )) kvs)

        ESet xs ->
            Encode.list valToJson xs
"""

# Full ``Val`` type with every constructor.  Replaces the body_preamble
# the Elm backend would otherwise emit (which only lists the
# constructors actually used by the data) so ``valToJson`` above can
# pattern-match the full surface.
_VAL_TYPE = """\
type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
    | ESet (List Val)
"""

_MAIN_TEMPLATE = """\
port module Main exposing (main)

import Json.Encode as Encode
import Platform


{val_type}

{declaration}


{val_to_json}

port output : String -> Cmd msg


main : Program () () Never
main =
    Platform.worker
        {{ init = \\_ -> ( (), output (Encode.encode 0 (valToJson {var})) )
        , update = \\_ m -> ( m, Cmd.none )
        , subscriptions = \\_ -> Sub.none
        }}
"""


def _build_main(json_text: str) -> str:
    """Return a runnable Elm port module literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=Elm(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    # ``result.code`` for Elm starts with the body_preamble (the
    # ``type Val ...`` declaration restricted to used constructors);
    # strip it so the full ``_VAL_TYPE`` below is the sole definition.
    body_preamble_text = "\n".join(result.body_preamble)
    declaration = result.code
    if declaration.startswith(body_preamble_text):
        declaration = declaration[len(body_preamble_text) :].lstrip("\n")
    return _MAIN_TEMPLATE.format(
        val_type=_VAL_TYPE,
        declaration=declaration,
        val_to_json=_VAL_TO_JSON,
        var=_VAR_NAME,
    )


def main() -> None:
    """Round-trip the shared document through the Elm backend."""
    program = _build_main(json_text=roundtrip_common.read_input())
    elm = shutil.which(cmd="elm") or "elm"
    node = shutil.which(cmd="node") or "node"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src_dir = tmpdir / "src"
        src_dir.mkdir()
        (tmpdir / "elm.json").write_text(data=_ELM_JSON, encoding="utf-8")
        (src_dir / "Main.elm").write_text(data=program, encoding="utf-8")
        (tmpdir / "run.js").write_text(data=_RUN_JS, encoding="utf-8")
        compile_result = subprocess.run(
            args=[elm, "make", "src/Main.elm", "--output=main.js"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
            env={**os.environ},
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: elm make error\n"
                f"{compile_result.stdout}{compile_result.stderr}",
            )
            sys.stderr.write(f"\nProgram:\n{program}\n")
            sys.exit(1)
        run_result = subprocess.run(
            args=[node, "run.js"],
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
