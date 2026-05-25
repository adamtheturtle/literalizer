"""Lua JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Lua
``local my_data = ...`` assignment, wrap it in a tiny script that prints
``dkjson.encode(my_data)``, run it under ``lua``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Lua roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the Lua toolchain is installed and the ``dkjson`` rock is
provisioned (``LUA_PATH``/``LUA_CPATH`` are exported there so
``require "dkjson"`` resolves).  It shares the same input and comparison
logic as the other per-language round-trip helpers.

Lua has no standard-library JSON serializer; ``dkjson`` is the pure-Lua
library option, preferred over hand-rolling one per the issue brief.

Three top-level keys are excluded from the comparison:

* ``biginteger`` — its 26-digit value overflows Lua's 64-bit integer so
  the literalized program parses the literal as a ``double`` (``1e+26``),
  same shape as the Go, TypeScript, Zig, Swift, Rust, D, and C++
  exclusions.
* ``float_large_exponent`` — Lua 5.4's default float-to-string format
  is ``%.14g``, which rounds ``1.7976931348623157e+308`` down to
  ``1.7976931348623e+308`` and loses the trailing significant digits;
  ``dkjson`` uses ``tostring`` for number encoding so it inherits that
  precision floor.
* ``empty_object`` — Lua represents both arrays and objects as bare
  tables and an empty ``{}`` is genuinely ambiguous, so ``dkjson``
  serializes the empty-object value as ``[]`` instead of ``{}``.  Same
  shape as the R exclusion.
"""

import shutil

import roundtrip_common

from literalizer.languages import Lua

_VAR_NAME = "my_data"
_LABEL = "Lua"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent", "empty_object")


def _build_program(json_text: str) -> str:
    """Return a runnable Lua program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Lua(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        'local json = require "dkjson"\n'
        f"{preamble}\n"
        f"{result.code}\n"
        f"io.write(json.encode({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Lua backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    lua = shutil.which(cmd="lua") or "lua"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.lua",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[lua, "main.lua"],
                failure_label="lua runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
