"""Forth JSON round-trip check (issue #2651, reworked for #2744).

Literalize the shared ``roundtrip_input.json`` document to a Forth
``: myData ... ;`` colon definition, wrap it in a ``gforth`` script that
loads the shipped visitor prelude
(``src/literalizer/languages/forth_prelude.fs``), executes ``myData`` to
drive the prelude's Forth Foundation Library (FFL) ``jos``
JSON-output-stream bindings, prints the accumulated JSON, and hands it
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Forth roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the ``gforth`` apt package (pinned by the ``Install apt packages``
step) and the FFL checkout (pinned by the ``Install FFL`` step that
sets ``LITERALIZER_FFL_PATH``) are provisioned.  It shares the same
input and comparison logic as the other per-language round-trip
helpers.

Since issue #2744 the Forth backend emits a *structured visitor stream*
(``+obj``/``+arr``/``+key``/``+int``/``+float``/``+str``/``+bool``/
``+null``): the literalized ``myData`` preserves the document structure
on its own, so this script no longer walks the input shape on the Python
side.  It mirrors the Lua/Wren shape -- literalize, splice into a tiny
runner template, run, compare -- with the only Forth-specific glue being
the FFL search path and the prelude include.  The prelude is the default
binding shipped to users; rebinding any of the visitor words would emit
a different format, but here the default ``jos`` JSON writer is exactly
what the round-trip needs.

Two top-level keys are excluded from the comparison:

* ``biginteger`` -- its 26-digit value overflows the 64-bit cell that
  ``gforth`` uses on the Ubuntu runner; same shape as the Go, TypeScript,
  Lua, Zig, Swift, Rust, D, C++, and Wren exclusions.
* ``float_large_exponent`` -- ``Forth.float_format`` is
  ``format_float_scientific``, which uses Python's ``f"{value:e}"``
  (six fractional digits) and emits ``1.797693e308``, losing the
  trailing significant digits of ``1.7976931348623157e+308``; the
  truncation happens at literalize time before the Forth toolchain
  ever sees the value, so the field is excluded from the round-trip.
"""

import os
import shutil
from pathlib import Path

from literalizer.languages import Forth
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Forth"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")

# The shipped default visitor prelude (FFL `jos` JSON writer).  Included
# by absolute path so the round-trip exercises the exact file users get.
_PRELUDE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "literalizer"
    / "languages"
    / "forth_prelude.fs"
)

# Header template for the generated gforth program.  ``fpath+`` adds the
# FFL checkout to gforth's source-search path so the bare
# ``include ffl/jos.fs`` inside the prelude resolves; the path is filled
# in from the ``LITERALIZER_FFL_PATH`` environment variable that the
# ``Install FFL`` step in ``.github/workflows/lint.yml`` exports.
# ``17 set-precision`` is the maximum precision that FFL's
# ``tos-write-float`` honors (``precision 80 min`` in ``tos.fs``) and is
# enough to round-trip every IEEE-754 double through the emitted
# ``[-]0.dddddddddddddddddE[-]N`` form.
_HEADER_TEMPLATE = """\
fpath+ {ffl_path}
include {prelude_path}
17 set-precision
"""

# Execute the literalized definition to drive the prelude's `jos`
# bindings, then print the accumulated JSON document.
_FOOTER = f"""\
{_VAR_NAME} json-out str-get type bye
"""


def _build_program(*, json_text: str, ffl_path: str) -> str:
    """Return a runnable gforth script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Forth(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    header = _HEADER_TEMPLATE.format(
        ffl_path=ffl_path,
        prelude_path=_PRELUDE_PATH,
    )
    return f"{header}\n{preamble}\n{result.code}\n\n{_FOOTER}"


def main() -> None:
    """Round-trip the shared document through the Forth backend."""
    # ``LITERALIZER_FFL_PATH`` points at the FFL checkout (the
    # ``Install FFL`` step in ``.github/workflows/lint.yml`` exports
    # it); the generated program prepends that to gforth's source
    # search path via ``fpath+`` so the prelude's bare
    # ``include ffl/jos.fs`` resolves there.
    ffl_path = os.environ["LITERALIZER_FFL_PATH"]
    program = _build_program(
        json_text=roundtrip_common.read_input(),
        ffl_path=ffl_path,
    )
    gforth = shutil.which(cmd="gforth") or "gforth"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.fth",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[gforth, "main.fth"],
                failure_label="gforth runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
