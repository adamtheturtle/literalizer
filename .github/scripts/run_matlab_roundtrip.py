"""MATLAB JSON round-trip check (issue #2663).

Literalize the shared ``roundtrip_input.json`` document to a MATLAB
``myData = ...;`` assignment, append a line that prints
``jsonencode(myData)``, run the script, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``MATLAB roundtrip`` step of the
``lint-matlab`` job in ``.github/workflows/lint.yml``, because that job
is where the MATLAB toolchain is installed.  As with the ``Lint Matlab``
parse check, the toolchain is Octave (``gnuoctave/octave``), a practical
CI substitute for MATLAB; ``jsonencode`` is the built-in serializer
shared by both.  This script shares the same input and comparison logic
as the other per-language round-trip helpers.

One field is excluded from the comparison because MATLAB's number type
cannot represent it losslessly:

* ``biginteger`` -- MATLAB has only the IEEE-754 ``double`` numeric
  type, so the 26-digit literal is stored as a double and
  ``jsonencode`` re-emits it as ``1e26``.  The field is trimmed from the
  input *before* literalization so the generated program does not carry
  a value the round-trip would reject.
"""

import shutil

import roundtrip_common

from literalizer.languages import Matlab

_VAR_NAME = "myData"
_LABEL = "MATLAB"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable MATLAB program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Matlab(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    emit = f'printf("%s", jsonencode({_VAR_NAME}));'
    return f"{preamble}\n{result.code}\n{emit}\n"


def main() -> None:
    """Round-trip the shared document through the MATLAB backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    octave = shutil.which(cmd="octave") or "octave"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.m",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[octave, "--norc", "--no-gui", "main.m"],
                failure_label="octave runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
