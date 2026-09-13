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

``negative_zero`` is excluded too: ``JSON.stringify`` writes ``0`` for
``-0``, so the sign cannot survive the encode this driver performs, and
the value is refused up front (issue #4543).

Under ``json_type=JSON_ENCODE_VALUE`` the literalized output is already
a :class:`Json.Encode.Value` built from idiomatic ``Json.Encode.*``
calls.  No ``Val`` ADT or walker is needed: ``Json.Encode.encode 0``
serializes the declared value directly.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from literalizer.languages import Elm
from scripts import roundtrip_common
from scripts.elm_common import ELM_JSON, NOINDEX_SUFFIX, run_elm_make

_VAR_NAME = "myData"
_LABEL = "Elm"
_EXCLUDED_KEYS = ("biginteger", "negative_zero")

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
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Elm.variant_metadata.round_trip_capabilities,
    )
    program = _build_main(json_text=json_text)
    elm = shutil.which(cmd="elm")
    if elm is None or elm == "":
        elm = "elm"
    node = shutil.which(cmd="node")
    if node is None or node == "":
        node = "node"
    with tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src_dir = tmpdir / "src"
        src_dir.mkdir()
        _ = (src_dir / "Main.elm").write_text(
            data=program,
            encoding="utf-8",
        )
        _ = (tmpdir / "elm.json").write_text(data=ELM_JSON, encoding="utf-8")
        _ = (tmpdir / "run.js").write_text(data=_RUN_JS, encoding="utf-8")
        compile_result = run_elm_make(
            args=[elm, "make", "src/Main.elm", "--output=main.js"],
            cwd=tmpdir,
            env=os.environ,
        )
        if compile_result.returncode != 0:
            _ = sys.stderr.write(
                f"{_LABEL}: elm make error\n"
                f"{compile_result.stdout}{compile_result.stderr}"
                f"\nProgram:\n{program}\n",
            )
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
        _ = sys.stderr.write(
            f"{_LABEL}: node run error\n"
            f"{run_result.stdout}{run_result.stderr}"
            f"\nProgram:\n{program}\n",
        )
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
    )
    _ = sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
