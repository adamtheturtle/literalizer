"""OCaml JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an OCaml
``let my_data : val_t = ...`` binding (with the generated tagged
``val_t`` algebraic type), append a hand-rolled
``val_to_json : val_t -> string`` recursive serializer, run it through
``ocaml``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-ocaml`` job in
``.github/workflows/lint.yml``, because that job is where the OCaml
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

OCaml's standard library has no JSON encoder, so the serializer is
hand-rolled rather than pulled in via an external opam package
(``yojson`` etc.) -- same shape as the Java setup.  The generated
``val_t`` algebraic type carries only the constructors needed for the
values that actually appear in the input, so ``val_to_json`` covers
exactly the six variants the shared input exercises (``OBool``,
``OInt``, ``OFloat``, ``OStr``, ``OList``, ``OMap``); a future
expansion of ``roundtrip_input.json`` adding a new scalar kind would
fail compilation here until the match is extended.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value exceeds OCaml's 63-bit native ``int``,
so the literalizer would raise rather than emit a literal for it.
Same shape as the Go, TypeScript, Swift, Zig, and Rust exclusions.
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

# Hand-rolled JSON encoder.  ``%.17g`` is the shortest fixed precision
# that round-trips any IEEE 754 double; the parser on the Python side
# only compares parsed values, so trailing-zero stripping (e.g. ``1.0``
# rendered as ``1``) and ``-0.0`` rendered as ``-0`` are both fine.
_VAL_TO_JSON = """\
let json_string s =
  let buf = Buffer.create (String.length s + 2) in
  Buffer.add_char buf '"';
  String.iter (fun c ->
    match c with
    | '"' -> Buffer.add_string buf "\\\\\\""
    | '\\\\' -> Buffer.add_string buf "\\\\\\\\"
    | '\\n' -> Buffer.add_string buf "\\\\n"
    | '\\r' -> Buffer.add_string buf "\\\\r"
    | '\\t' -> Buffer.add_string buf "\\\\t"
    | '\\b' -> Buffer.add_string buf "\\\\b"
    | '\\012' -> Buffer.add_string buf "\\\\f"
    | c when Char.code c < 0x20 ->
        Buffer.add_string buf (Printf.sprintf "\\\\u%04x" (Char.code c))
    | c -> Buffer.add_char buf c
  ) s;
  Buffer.add_char buf '"';
  Buffer.contents buf

let rec val_to_json (v : val_t) : string =
  match v with
  | OBool true -> "true"
  | OBool false -> "false"
  | OInt i -> string_of_int i
  | OFloat f -> Printf.sprintf "%.17g" f
  | OStr s -> json_string s
  | OList xs ->
      "[" ^ String.concat "," (List.map val_to_json xs) ^ "]"
  | OMap kvs ->
      "{" ^ String.concat ","
        (List.map (fun (k, v) -> json_string k ^ ":" ^ val_to_json v) kvs)
      ^ "}"

let () = print_string (val_to_json my_data)
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
    return f"{preamble}\n{result.code}\n{_VAL_TO_JSON}"


def main() -> None:
    """Round-trip the shared document through the OCaml backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ocaml = shutil.which(cmd="ocaml") or "ocaml"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        src = tmpdir / "main.ml"
        src.write_text(data=program, encoding="utf-8")
        run_result = subprocess.run(
            args=[ocaml, str(object=src)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: ocaml error\n{run_result.stdout}{run_result.stderr}",
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
