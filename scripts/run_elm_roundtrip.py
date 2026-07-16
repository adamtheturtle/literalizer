"""Elm JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Elm
``myData : Json.Encode.Value`` declaration via
``Elm(json_type=JSON_ENCODE_VALUE)``, wrap it in a tiny ``port`` module
that serializes ``myData`` straight through ``Json.Encode.encode`` and
ships the JSON to stdout via a port, compile that module with ``elm
make``, run the emitted JavaScript under Node so the port subscription
writes the JSON, and hand the result to :func:`roundtrip_common.verify`.

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

Under ``json_type=JSON_ENCODE_VALUE`` the literalized output is already
a :class:`Json.Encode.Value` built from idiomatic ``Json.Encode.*``
calls.  No ``Val`` ADT or walker is needed: ``Json.Encode.encode 0``
serializes the declared value directly.
"""

import shutil

from literalizer.languages import Elm
from scripts import roundtrip_common
from scripts.elm_common import ELM_JSON

_VAR_NAME = "myData"
_LABEL = "Elm"
_EXCLUDED_KEYS = ("biginteger",)

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

_MAIN_TEMPLATE = """\
port module Main exposing (main)

import Json.Encode
import Platform


{declaration}


port output : String -> Cmd msg


main : Program () () Never
main =
    Platform.worker
        {{ init = \\_ -> ( (), output (Json.Encode.encode 0 {var}) )
        , update = \\_ m -> ( m, Cmd.none )
        , subscriptions = \\_ -> Sub.none
        }}
"""


def _build_main(json_text: str) -> str:
    """Return a runnable Elm port module literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    # ``result.code`` for Elm starts with the body_preamble (the
    # ``import Json.Encode`` line under ``json_type``); strip it so the
    # template's single import is the only one.
    body_preamble_text = "\n".join(result.body_preamble)
    declaration = result.code
    if declaration.startswith(body_preamble_text):
        declaration = declaration[len(body_preamble_text) :].lstrip("\n")
    return _MAIN_TEMPLATE.format(
        declaration=declaration,
        var=_VAR_NAME,
    )


def main() -> None:
    """Round-trip the shared document through the Elm backend."""
    program = _build_main(json_text=roundtrip_common.read_input())
    elm = shutil.which(cmd="elm") or "elm"
    node = shutil.which(cmd="node") or "node"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="src/Main.elm",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[elm, "make", "src/Main.elm", "--output=main.js"],
                failure_label="elm make error",
            ),
            roundtrip_common.Step(
                args=[node, "run.js"],
                failure_label="node run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        extra_files={
            "elm.json": ELM_JSON,
            "run.js": _RUN_JS,
        },
    )


if __name__ == "__main__":
    main()
