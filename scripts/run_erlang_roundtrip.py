"""Erlang JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Erlang
``MyData = #{...},`` map binding using the ``OTP_JSON`` json_type so
every string, ISO date / datetime / time, and base64-encoded bytes
value renders as a UTF-8 binary literal (``<<"..."/utf8>>``) and
``null`` is the bare atom ``null``.  Wrap the binding in an
``escript`` whose ``main/1`` prints ``json:encode(MyData)`` on
standard output, run it under ``escript``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Erlang roundtrip`` step of the
``lint-erlang`` job in ``.github/workflows/lint.yml``, because that job
is where the Erlang/OTP toolchain is installed.  It shares the same
input and comparison logic as the other per-language round-trip helpers.

The serializer is OTP 27's built-in ``json`` module rather than a
hand-rolled encoder (matching the preference expressed in the issue
notes).  Under ``OTP_JSON`` the rendered value is already in the shape
``json:encode/1`` accepts (binary keys, binary string values, ``null``
atom), so no normalization walker is needed.
"""

import shutil

from literalizer.languages import Erlang
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Erlang"

_ENCODE = """\
    ok = io:setopts(standard_io, [{encoding, unicode}]),
    Json = json:encode(MyData),
    ok = io:put_chars(Json).
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Erlang escript literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Erlang(json_type=Erlang.json_types.OTP_JSON),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    indented_decl = result.code.replace("\n", "\n    ")
    return (
        "#!/usr/bin/env escript\n"
        "%% -*- coding: utf-8 -*-\n"
        "\n"
        "main(_) ->\n"
        f"    {indented_decl}\n"
        f"{_ENCODE}"
    )


def main() -> None:
    """Round-trip the shared document through the Erlang backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    escript = shutil.which(cmd="escript") or "escript"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.erl",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[escript, "main.erl"],
                failure_label="escript error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
