"""OCaml JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an OCaml
``let my_data : Yojson.Safe.t = ...`` binding using the
``YOJSON_SAFE_T`` json_type, append a ``Yojson.Safe.to_string`` call,
compile with ``ocamlfind ocamlopt -package yojson -linkpkg``, run the
binary, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-ocaml`` job in
``.github/workflows/lint.yml``, because that job is where the OCaml
toolchain (and the ``yojson`` opam package installed by a sibling step)
is available.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

The ``YOJSON_SAFE_T`` mode emits the literal directly as a
``Yojson.Safe.t`` polymorphic variant, so this helper no longer needs
the hand-written ``val_to_yojson`` mapping from the generated
``val_t`` ADT --- the binding is already a ``Yojson.Safe.t`` and feeds
straight into ``Yojson.Safe.to_string``.  Arbitrary-precision
integers route through `` `Intlit "..." `` (Yojson's escape hatch for
values outside OCaml's native ``int`` range), so the shared input's
``biginteger`` field is no longer excluded.
"""

import shutil

from literalizer.languages import OCaml
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "OCaml"

_PRINT_JSON = """\
let () = print_string (Yojson.Safe.to_string my_data)
"""


def _build_program(json_text: str) -> str:
    """Return a runnable OCaml program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join(result.preamble)
    return f"{preamble}\n{result.code}\n{_PRINT_JSON}"


def main() -> None:
    """Round-trip the shared document through the OCaml backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ocamlfind = shutil.which(cmd="ocamlfind") or "ocamlfind"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.ml",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    ocamlfind,
                    "ocamlopt",
                    "-package",
                    "yojson",
                    "-linkpkg",
                    "main.ml",
                    "-o",
                    "main",
                ],
                failure_label="ocamlfind error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
