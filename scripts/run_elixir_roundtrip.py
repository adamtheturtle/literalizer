"""Elixir JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Elixir
``my_data = %{...}`` binding, wrap it in a tiny ``.exs`` script that
prints ``JSON.encode!(my_data)`` on standard output, run it under
``elixir``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Elixir roundtrip`` step of the
``lint-elixir`` job in ``.github/workflows/lint.yml``, because that job
is where the Elixir toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.

The serializer is Elixir 1.18's built-in ``JSON`` module rather than a
hand-rolled encoder (matching the preference expressed in the issue
notes).  ``JSON.encode!/1`` natively handles arbitrary-precision
integers, IEEE 754 doubles, booleans, ``nil``, lists and
string-keyed maps, which is everything the shared input carries.
"""

import shutil

from literalizer.languages import Elixir
from scripts import roundtrip_common

_VAR_NAME = "my_data"
_LABEL = "Elixir"


def _build_program(json_text: str) -> str:
    """Return a runnable Elixir script literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Elixir(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\nIO.write(JSON.encode!({_VAR_NAME}))\n"


def main() -> None:
    """Round-trip the shared document through the Elixir backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    elixir = shutil.which(cmd="elixir") or "elixir"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.exs",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[elixir, "main.exs"],
                failure_label="elixir runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
