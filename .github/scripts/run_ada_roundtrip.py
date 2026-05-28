"""Ada JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Ada
``my_data : A_Val := ...;`` declaration, wrap it in a tiny ``Main``
that prints ``A_Stub.To_JSON (my_data)``, compile that together with
the richer ``roundtrip_a_stub.{ads,adb}`` from this directory (copied
into the temp dir as ``a_stub.{ads,adb}`` so the literalized ``with
A_Stub;`` resolves), run it, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Ada roundtrip`` step of the
``lint-uv-scripts`` job in ``.github/workflows/lint.yml``, because
that is the job with the GNAT toolchain installed.

The ``A_Stub.To_JSON`` body walks the ``A_Val`` tree into a
``GNATCOLL.JSON.JSON_Value`` and lets ``GNATCOLL.JSON.Write`` produce
the output, so escaping and number formatting come from the library
rather than from a hand-rolled emitter.  Linking against GNATCOLL is
arranged through a small project file (``roundtrip_main.gpr``) that
``with``-clauses the apt-provided ``gnatcoll`` project; ``gprbuild
-P`` then resolves include and link paths automatically.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows ``Long_Long_Integer`` (what the Ada backend
emits ``AInt`` over), so the program would not compile if the field
were kept.  Same shape as the Go/Zig/TypeScript exclusions.

The shared input's ``float_large_exponent`` field
(``1.7976931348623157e+308``, ``Float64`` max) is also excluded:
``GNATCOLL.JSON.Write`` formats ``Long_Float`` with around 15 decimal
digits and offers no precision knob, so the rendered text rounds
slightly above ``DBL_MAX`` and Python's ``json.loads`` then parses it
as ``inf``.  Every smaller float in the shared input still
round-trips.

The shared input's ``empty_object`` field is also excluded: the Ada
backend's ``validate_spec_for_data`` raises
:class:`~literalizer.exceptions.UnrepresentableEmptyDictError` on
empty mappings (because the unified ``A_Val`` aggregate cannot
distinguish an empty ``AMap'[]`` from an empty ``AList'[]`` at run
time), so trimming the key keeps the roundtrip driver runnable.
Non-empty maps and lists are distinguished by whether their first
item is an ``AEntry``, so every other shape in the shared input
round-trips losslessly.
"""

import shutil
import textwrap
from pathlib import Path

import roundtrip_common

from literalizer.languages import Ada

_SCRIPT_DIR = Path(__file__).resolve().parent
_STUB_ADS_SRC = _SCRIPT_DIR / "roundtrip_a_stub.ads"
_STUB_ADB_SRC = _SCRIPT_DIR / "roundtrip_a_stub.adb"
_VAR_NAME = "my_data"
_LABEL = "Ada"
_EXCLUDED_KEYS = ("biginteger", "empty_object", "float_large_exponent")

# ``-gnat2022`` matches ``Ada.language_version`` in
# ``src/literalizer/languages/ada.py``; keep them in sync.  GNAT's
# default 8-bit source encoding is what we want here: the shared input's
# ``string_unicode`` value reaches the Ada ``String`` literal as raw
# UTF-8 bytes, ``GNATCOLL.JSON`` re-emits it byte-for-byte, and Python
# ``json.loads`` decodes the resulting UTF-8 back to the original text.
_PROJECT_FILE = """\
with "gnatcoll";
project Roundtrip_Main is
   for Source_Dirs use (".");
   for Object_Dir use ".";
   for Main use ("main.adb");
   package Builder is
      for Switches ("Ada") use ("-gnat2022");
   end Builder;
end Roundtrip_Main;
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Ada program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Ada(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    declarative = "\n".join((*result.body_preamble, result.code))
    indented = textwrap.indent(text=declarative, prefix="    ")
    return (
        "with A_Stub; use A_Stub;\n"
        "with Ada.Text_IO;\n"
        "procedure Main is\n"
        f"{indented}\n"
        "begin\n"
        f"    Ada.Text_IO.Put (A_Stub.To_JSON ({_VAR_NAME}));\n"
        "end Main;\n"
    )


def main() -> None:
    """Round-trip the shared document through the Ada backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    gprbuild = shutil.which(cmd="gprbuild") or "gprbuild"
    extras = {
        "a_stub.ads": _STUB_ADS_SRC.read_text(encoding="utf-8"),
        "a_stub.adb": _STUB_ADB_SRC.read_text(encoding="utf-8"),
        "roundtrip_main.gpr": _PROJECT_FILE,
    }
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.adb",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[gprbuild, "-q", "-P", "roundtrip_main.gpr"],
                failure_label="gprbuild error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="Ada runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        extra_files=extras,
    )


if __name__ == "__main__":
    main()
