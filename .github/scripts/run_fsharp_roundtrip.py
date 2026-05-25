r"""F# JSON round-trip check (issue #2653).

Literalize the shared ``roundtrip_input.json`` document to an F#
``let my_data : Val = ...`` binding (with the generated tagged ``Val``
discriminated union), append a small ``writeVal`` mapping that walks
each constructor into the built-in :class:`System.Text.Json.Utf8JsonWriter`,
evaluate the script under ``dotnet fsi``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-dotnet`` job in
``.github/workflows/lint.yml``, because that job is where the .NET
toolchain (which ships ``dotnet fsi`` and ``System.Text.Json``) is
already provisioned.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

F#'s standard environment ships ``System.Text.Json`` (no NuGet install
required), so we route through that rather than hand-rolling a JSON
encoder, matching the issue brief's preference for built-in libraries.
``Utf8JsonWriter`` has no automatic mapping for the generated ``Val``
discriminated union, so a tiny ``writeVal`` ``match`` translates each
constructor into the writer's ``WriteBooleanValue`` / ``WriteNumberValue``
/ ``WriteStringValue`` / ``WriteStartArray`` / ``WriteStartObject`` calls.
``JavaScriptEncoder.UnsafeRelaxedJsonEscaping`` disables the default
HTML-safe ``\\u00xx`` escapes so non-ASCII strings round-trip as their
literal UTF-8 bytes.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value exceeds F#'s 64-bit ``int64``, so the literalizer
would emit a ``bigint`` literal that ``Utf8JsonWriter.WriteNumberValue``
has no overload for.  Same shape as the Go, OCaml, TypeScript, Swift,
Zig, Rust, and D exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import FSharp

_VAR_NAME = "my_data"
_LABEL = "FSharp"
_EXCLUDED_KEYS = ("biginteger",)

_WRITE_VAL = """\
open System.IO
open System.Text.Json

let rec writeVal (writer: Utf8JsonWriter) (v: Val) =
    match v with
    | FBool b -> writer.WriteBooleanValue(b)
    | FInt i -> writer.WriteNumberValue(i)
    | FFloat f -> writer.WriteNumberValue(f)
    | FStr s -> writer.WriteStringValue(s)
    | FList xs ->
        writer.WriteStartArray()
        for x in xs do writeVal writer x
        writer.WriteEndArray()
    | FMap kvs ->
        writer.WriteStartObject()
        for (k, v) in kvs do
            writer.WritePropertyName(k)
            writeVal writer v
        writer.WriteEndObject()

let _stream = new MemoryStream()
let _opts =
    JsonWriterOptions(
        Encoder =
            System.Text.Encodings.Web
                .JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    )
let _writer = new Utf8JsonWriter(_stream, _opts)
writeVal _writer my_data
_writer.Flush()
let _stdout = System.Console.OpenStandardOutput()
_stream.WriteTo(_stdout)
_stdout.Flush()
"""


def _build_program(json_text: str) -> str:
    """Return a runnable F# script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=FSharp(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    # ``FSharp.literalize`` already inlines ``result.body_preamble``
    # (the ``type Val`` declaration) at the top of ``result.code``,
    # so we only join ``preamble`` (currently empty) with ``code``
    # here. Prepending ``body_preamble`` separately would duplicate
    # the ``Val`` type and break compilation.
    preamble = "\n".join(result.preamble)
    return f"{preamble}\n{result.code}\n{_WRITE_VAL}"


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
