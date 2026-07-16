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

This lives here, driven by the ``CSharp roundtrip`` step of the
``lint-dotnet`` job in ``.github/workflows/lint.yml``, because that job
is where the .NET toolchain is installed; it is deliberately not a
pytest test under ``tests/``.
"""

import shutil

from literalizer.languages import CSharp
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "CSharp"
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
    "    <Nullable>disable</Nullable>\n"
    "    <ImplicitUsings>disable</ImplicitUsings>\n"
    "    <LangVersion>10</LangVersion>\n"
    "  </PropertyGroup>\n"
    "</Project>\n"
)


def _build_program(json_text: str) -> str:
    """Return a runnable C# program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=CSharp(sequence_format=CSharp.sequence_formats.ARRAY),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=2,
    )
    preamble = "\n".join(result.preamble)
    body_preamble = "\n".join(result.body_preamble)
    return (
        f"{preamble}\n"
        "using System;\n"
        "using System.Text.Json;\n"
        f"{body_preamble}\n"
        "static class Program {\n"
        "    public static void Main() {\n"
        f"{result.code}\n"
        f"        Console.Write(JsonSerializer.Serialize({_VAR_NAME}));\n"
        "    }\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the C# backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dotnet = shutil.which(cmd="dotnet") or "dotnet"
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
        extra_files={"fixture.csproj": _CSPROJ},
    )


if __name__ == "__main__":
    main()
