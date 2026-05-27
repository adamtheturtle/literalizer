r"""F# JSON round-trip check (issue #2653).

Literalize the shared ``roundtrip_input.json`` document to an F#
``let my_data : JsonNode = ...`` binding using
:class:`FSharp.json_types.SYSTEM_TEXT_JSON_NODE` so the rendered value
is a ``System.Text.Json.Nodes.JsonNode`` tree backed by the built-in
``System.Text.Json`` library, append the small ``ToJsonString()``
serialization tail, evaluate the script under ``dotnet fsi``, and hand
the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-dotnet`` job in
``.github/workflows/lint.yml``, because that job is where the .NET
toolchain (which ships ``dotnet fsi`` and ``System.Text.Json``) is
already provisioned.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value exceeds F#'s 64-bit ``int64`` (and the ``ulong``
overload of ``JsonValue.Create``), so the literalizer would emit a
literal that ``JsonValue.Create`` has no overload for.  Same shape as
the Go, OCaml, TypeScript, Swift, Zig, Rust, and D exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import FSharp

_VAR_NAME = "my_data"
_LABEL = "FSharp"
_EXCLUDED_KEYS = ("biginteger",)

_SERIALIZE_TAIL = """\
let _stdout = System.Console.OpenStandardOutput()
let _bytes =
    System.Text.Encoding.UTF8.GetBytes(
        my_data.ToJsonString(
            System.Text.Json.JsonSerializerOptions(
                Encoder =
                    System.Text.Encodings.Web
                        .JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            )
        )
    )
_stdout.Write(_bytes, 0, _bytes.Length)
_stdout.Flush()
"""


def _build_program(json_text: str) -> str:
    """Return a runnable F# script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=FSharp(
            json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE,
        ),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join(result.preamble)
    return f"{preamble}\n{result.code}\n{_SERIALIZE_TAIL}"


def main() -> None:
    """Round-trip the shared document through the F# backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dotnet = shutil.which(cmd="dotnet") or "dotnet"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.fsx",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    dotnet,
                    "fsi",
                    "--nologo",
                    "--langversion:8.0",
                    "--exec",
                    "main.fsx",
                ],
                failure_label="dotnet fsi error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
