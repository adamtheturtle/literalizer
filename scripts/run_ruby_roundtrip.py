"""Ruby JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Ruby
``myData = ...`` assignment, wrap it in a tiny script that prints
``JSON.generate(myData)``, run it with Ruby, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Ruby roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the Ruby toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.
"""

import shutil

from literalizer.languages import Ruby
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Ruby"


def _build_program(json_text: str) -> str:
    """Return a runnable Ruby program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Ruby(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "# frozen_string_literal: true\n"
        "\n"
        "require 'json'\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"STDOUT.write(JSON.generate({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Ruby backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ruby = shutil.which(cmd="ruby") or "ruby"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rb",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[ruby, "main.rb"],
                failure_label="ruby runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
