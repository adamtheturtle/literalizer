"""Nix JSON round-trip check (issue #2666).

Literalize the shared ``roundtrip_input.json`` document to a Nix
``let myData = {...}; in myData`` expression, write it to a ``main.nix``
file, evaluate it with ``nix-instantiate --eval --strict --json`` so
Nix's built-in JSON printer re-emits the value on stdout, and hand the
emitted JSON to :func:`roundtrip_common.verify`.

The JSON is produced by Nix's own ``--json`` evaluator output (the same
``printValueAsJSON`` machinery behind ``builtins.toJSON``) rather than a
hand-rolled walker, matching the issue's preference for a built-in JSON
dumper.  ``--strict`` forces the lazy attribute set and its nested lists
to be evaluated fully before serialization.

This lives here, driven by the ``Nix roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the ``nix-instantiate`` binary is installed (the ``Install Nix``
step).  It shares the same input and comparison logic as the other
per-language round-trip helpers.

Two fields of the shared input are trimmed before literalization and
excluded from the comparison:

``biginteger``
    The 26-digit value overflows Nix's signed 64-bit integers; the Nix
    backend materializes it as ``builtins.fromJSON "999..."``, which
    cannot represent the original magnitude on evaluation.

``float_large_exponent``
    ``1.7976931348623157e308`` sits at the edge of IEEE-754 double
    range; trimming it matches the Ada and C round-trip scripts and
    keeps the check independent of edge-of-range float printing.  The
    remaining ``float`` (``3.14``), ``negative_zero``, and
    container-nested doubles round-trip on Nix 2.12+ (which prints
    floats at full precision rather than the older six-significant-digit
    truncation).
"""

import shutil

from literalizer.languages import Nix
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Nix"

_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")


def _build_program(json_text: str) -> str:
    """Return a runnable Nix program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Nix(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    parts = (*result.preamble, *result.body_preamble, result.code)
    return "\n".join(parts) + "\n"


def main() -> None:
    """Round-trip the shared document through the Nix backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    nix_instantiate = shutil.which(cmd="nix-instantiate") or "nix-instantiate"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.nix",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    nix_instantiate,
                    "--eval",
                    "--strict",
                    "--json",
                    "./main.nix",
                ],
                failure_label="nix-instantiate error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
