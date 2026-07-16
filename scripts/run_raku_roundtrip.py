"""Raku JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Raku
``my $my_data = ...;`` declaration, wrap it in a tiny script that prints
``to-json($my_data)``, run it under ``raku``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Raku roundtrip`` step of the
``lint-raku`` job in ``.github/workflows/lint.yml``, because that job is
where the pinned Rakudo toolchain is installed and the ``JSON::Fast``
module is provisioned via ``zef``.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

``JSON::Fast`` is the standard Raku JSON library, preferred over
hand-rolling one per the issue brief.  Rakudo Int is arbitrary
precision so the 26-digit ``biginteger`` value round-trips without an
exclusion (same shape as the Erlang case), and Hash and Array are
distinct types so ``empty_object`` ``{}`` survives the round-trip.
"""

import shutil

from literalizer.languages import Raku
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "Raku"


def _build_program(json_text: str) -> str:
    """Return a runnable Raku program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Raku(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "use v6.d;\n"
        "use JSON::Fast;\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"print to-json(${_VAR_NAME}, :!pretty);\n"
    )


def main() -> None:
    """Round-trip the shared document through the Raku backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    raku = shutil.which(cmd="raku") or "raku"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.raku",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[raku, "main.raku"],
                failure_label="raku runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
