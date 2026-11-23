"""C# JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a C#
``var myData = ...;`` declaration, wrap it in a tiny ``Program`` whose
``Main`` prints ``System.Text.Json.JsonSerializer.Serialize(myData)``,
``dotnet run`` it, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

``System.Text.Json`` is part of the .NET base class library, so no
NuGet packages are needed; serializing through ``object`` dispatches on
the runtime type and walks ``IDictionary`` / array values
polymorphically.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value exceeds every C# integer literal type the literalizer
emits, so the program would not compile if the field were kept.

The same executable checks that mutating either nested occurrence of a
repeated bound JsonNode leaves the other occurrence and the original
unchanged, including after renaming the binding (issue #7217).

This lives here, driven by the ``CSharp roundtrip`` step of the
``lint-dotnet`` job in ``.github/workflows/lint.yml``, because that job
is where the .NET toolchain is installed; it is deliberately not a
pytest test under ``tests/``.
"""

import json
import shutil
from pathlib import Path

import click

from literalizer import InputFormat, ValueInput, literalize_call
from literalizer.languages import CSharp
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "CSharp"
_OWNERSHIP_CONSUMER_PATH = Path(__file__).parent / "JsonNodeOwnership.cs"
_EXCLUDED_KEYS = ("biginteger",)

# ``LangVersion 10`` matches ``CSharp.language_version`` in
# ``src/literalizer/languages/csharp.py`` and the ``LanguageVersion.CSharp10``
# pin in ``scripts/lint-csharp/Program.cs``; keep them in sync.
_CSPROJ = (
    '<Project Sdk="Microsoft.NET.Sdk">\n'
    "  <PropertyGroup>\n"
    "    <OutputType>Exe</OutputType>\n"
    "    <TargetFramework>net8.0</TargetFramework>\n"
    "    <RollForward>LatestMajor</RollForward>\n"
    "    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>\n"
    "    <Nullable>enable</Nullable>\n"
    "    <ImplicitUsings>disable</ImplicitUsings>\n"
    "    <LangVersion>10</LangVersion>\n"
    "  </PropertyGroup>\n"
    "</Project>\n"
)


def _ownership_case(*, binding: str, wrong_value: bool) -> str:
    """Render two uses of one binding or substitute one occurrence."""
    language = CSharp(json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE)
    bound_value = {"value": [1, 2]}
    declaration = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=json.dumps(obj=bound_value),
        var_name=binding,
        pre_indent_level=2,
    )
    reference = {"$ref": binding}
    copies: list[ValueInput] = [
        reference,
        {"value": [8, 2]} if wrong_value else reference,
    ]
    call = literalize_call(
        source=json.dumps(obj={"copies": copies}),
        input_format=InputFormat.JSON,
        language=language,
        target_function="Consume",
        parameter_names=["argument"],
        per_element=False,
        ref_key="$ref",
        ref_values={binding: bound_value},
    )
    return f"""
        {{
{declaration.code}
            for (var position = 0; position < 2; position++) {{
                {call.code}
                void Consume(JsonNode argument) =>
                    JsonNodeOwnership.Check(argument, {binding}!, position);
            }}
        }}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable C# program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=CSharp(
            sequence_format=CSharp.sequence_formats.ARRAY,
        ),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=2,
    )
    preamble = "\n".join(result.preamble)
    body_preamble = "\n".join(result.body_preamble)
    ownership_cases = _ownership_case(
        binding="shared", wrong_value=False
    ) + _ownership_case(binding="renamed", wrong_value=False)
    wrong_value = _ownership_case(binding="shared", wrong_value=True)
    return (
        f"{preamble}\n"
        "using System;\n"
        "using System.Text.Json;\n"
        "using System.Text.Json.Nodes;\n"
        f"{body_preamble}\n"
        "static class Program {\n"
        "    public static void Main() {\n"
        f"{result.code}\n"
        f'        if ({_VAR_NAME}["negative_zero"]\n'
        "            is not double negativeZero ||\n"
        "            BitConverter.DoubleToInt64Bits(negativeZero)\n"
        "                != long.MinValue) {\n"
        "            throw new InvalidOperationException(\n"
        '                "negative_zero lost its sign");\n'
        "        }\n"
        f"{ownership_cases}"
        "        JsonNodeOwnership.ExpectWrongValue(() => {\n"
        f"{wrong_value}"
        "        });\n"
        f"        Console.Write(JsonSerializer.Serialize({_VAR_NAME}));\n"
        "    }\n"
        "}\n"
    )


@click.command()
def main() -> None:
    """Round-trip the shared document through the C# backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=CSharp.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    dotnet = shutil.which(cmd="dotnet")
    if dotnet is None or dotnet == "":
        dotnet = "dotnet"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Program.cs",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    dotnet,
                    "run",
                    "--project",
                    "fixture.csproj",
                    "--nologo",
                ],
                failure_label="dotnet run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files={
            "fixture.csproj": _CSPROJ,
            _OWNERSHIP_CONSUMER_PATH.name: _OWNERSHIP_CONSUMER_PATH.read_text(
                encoding="utf-8",
            ),
        },
    )


if __name__ == "__main__":
    main()
