"""Erlang JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to an Erlang
``MyData = #{...},`` map binding, wrap it in an ``escript`` whose
``main/1`` normalizes Erlang charlist strings/keys to UTF-8 binaries
and prints ``json:encode(...)`` on standard output, run it under
``escript``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Erlang roundtrip`` step of the
``lint-erlang`` job in ``.github/workflows/lint.yml``, because that job
is where the Erlang/OTP toolchain is installed.  It shares the same
input and comparison logic as the other per-language round-trip helpers.

The serializer is OTP 27's built-in ``json`` module rather than a
hand-rolled encoder (matching the preference expressed in the issue
notes).  The default ``json`` encoder rejects Erlang charlists as map
keys and emits charlist string values as arrays of integers, so the
program first deep-normalizes the literalized data: charlist map keys
and printable charlist values become UTF-8 binaries, while non-printable
lists (e.g. ``[1, 2, 3]``) stay lists.  The non-empty guard on
``io_lib:printable_unicode_list/1`` keeps ``[]`` (an ``empty_array``)
from being mistakenly converted to ``<<>>``.
"""

import shutil

import roundtrip_common

from literalizer.languages import Erlang

_VAR_NAME = "myData"
_LABEL = "Erlang"

_NORMALIZE_AND_ENCODE = """\
    ok = io:setopts(standard_io, [{encoding, unicode}]),
    Json = json:encode(normalize(MyData)),
    ok = io:put_chars(Json).

normalize(M) when is_map(M) ->
    maps:from_list(
      [{to_binary_key(K), normalize(V)} || {K, V} <- maps:to_list(M)]);
normalize(L) when is_list(L) ->
    case L =/= [] andalso io_lib:printable_unicode_list(L) of
        true -> unicode:characters_to_binary(L);
        false -> [normalize(X) || X <- L]
    end;
normalize(X) -> X.

to_binary_key(K) when is_list(K) -> unicode:characters_to_binary(K);
to_binary_key(K) -> K.
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Erlang escript literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Erlang(),
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
        f"{_NORMALIZE_AND_ENCODE}"
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
