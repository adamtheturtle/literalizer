"""OCaml JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an OCaml
``let my_data : val_t = ...`` binding (with the generated tagged
``val_t`` algebraic type), append a small ``val_to_yojson`` mapping into
``Yojson.Safe.t`` plus a ``Yojson.Safe.to_string`` call, compile with
``ocamlfind ocamlopt -package yojson -linkpkg``, run the binary, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-ocaml`` job in
``.github/workflows/lint.yml``, because that job is where the OCaml
toolchain (and the ``yojson`` opam package installed by a sibling step)
is available.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

OCaml's standard library has no JSON encoder, so we route through the
de-facto ``yojson`` package rather than hand-roll a serializer -- same
preference expressed in the issue notes.  The generated ``val_t``
algebraic type carries only the constructors needed for the values
that actually appear in the input, so ``val_to_yojson`` covers exactly
the six variants the shared input exercises (``OBool``, ``OInt``,
``OFloat``, ``OStr``, ``OList``, ``OMap``); a future expansion of
``roundtrip_input.json`` adding a new scalar kind would fail compilation
here until the match is extended.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value exceeds OCaml's 63-bit native ``int``,
so the literalizer would raise rather than emit a literal for it.
Same shape as the Go, TypeScript, Swift, Zig, Rust, and D exclusions.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import OCaml

_VAR_NAME = "my_data"
_LABEL = "OCaml"
_EXCLUDED_KEYS = ("biginteger",)

_VAL_TO_YOJSON = """\
let rec val_to_yojson (v : val_t) : Yojson.Safe.t =
  match v with
  | OBool b -> `Bool b
  | OInt i -> `Int i
  | OFloat f -> `Float f
  | OStr s -> `String s
  | OList xs -> `List (List.map val_to_yojson xs)
  | OMap kvs ->
      `Assoc (List.map (fun (k, v) -> (k, val_to_yojson v)) kvs)

let () = print_string (Yojson.Safe.to_string (val_to_yojson my_data))
"""


def _build_program(json_text: str) -> str:
    """Return a runnable OCaml program literalized from *json_text*."""
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=OCaml(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
    )
    # ``OCaml.literalize`` already inlines ``result.body_preamble``
    # (the ``type val_t`` declaration) at the top of ``result.code``,
    # so we only join ``preamble`` (currently empty) with ``code``
    # here. Prepending ``body_preamble`` separately would duplicate
    # the ``val_t`` type and break compilation.
    preamble = "\n".join(result.preamble)
    return f"{preamble}\n{result.code}\n{_VAL_TO_YOJSON}"


def main() -> None:
    """Round-trip the shared document through the OCaml backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ocamlfind = shutil.which(cmd="ocamlfind") or "ocamlfind"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.ml"
        src.write_text(data=program, encoding="utf-8")
        binary = tmpdir / "main"
        compile_result = subprocess.run(
            args=[
                ocamlfind,
                "ocamlopt",
                "-package",
                "yojson",
                "-linkpkg",
                str(object=src),
                "-o",
                str(object=binary),
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
        if compile_result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: ocamlfind error\n"
                f"{compile_result.stdout}{compile_result.stderr}",
            )
            sys.stderr.write(f"\nProgram:\n{program}\n")
            sys.exit(1)
        run_result = subprocess.run(
            args=[str(object=binary)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: run error\n{run_result.stdout}{run_result.stderr}",
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
