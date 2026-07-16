"""Visual Basic (.NET) JSON round-trip check (issue #2682).

Literalize the shared ``roundtrip_input.json`` document to a VB.NET
``Dim myData = ...`` binding, wrap it in a tiny ``Module Program``
whose ``Sub Main`` prints
``System.Text.Json.JsonSerializer.Serialize(myData)``, ``dotnet run``
it, and hand the emitted JSON to :func:`roundtrip_common.verify`.

``System.Text.Json`` is part of the .NET base class library, so no
NuGet packages are needed; serializing through ``Object`` dispatches
on the runtime type and walks ``IDictionary`` / array values
polymorphically.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value exceeds every VB.NET integer literal type the
literalizer emits, so the program would not compile if the field were
kept.  Same shape as the C# exclusion.

This lives here, driven by the ``VisualBasic roundtrip`` step of the
``lint-dotnet`` job in ``.github/workflows/lint.yml``, because that job
is where the .NET toolchain is installed; it is deliberately not a
pytest test under ``tests/``.
"""

import shutil

from literalizer.languages import VisualBasic
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "VisualBasic"
_EXCLUDED_KEYS = ("biginteger",)

# ``LangVersion 16.9`` matches ``VisualBasic.language_version`` in
# ``src/literalizer/languages/vb.py`` and the
# ``LanguageVersion.VisualBasic16_9`` pin in
# ``scripts/lint-vb/Program.cs``; keep them in sync.
_VBPROJ = (
    '<Project Sdk="Microsoft.NET.Sdk">\n'
    "  <PropertyGroup>\n"
    "    <OutputType>Exe</OutputType>\n"
    "    <TargetFramework>net8.0</TargetFramework>\n"
    "    <RollForward>LatestMajor</RollForward>\n"
    "    <OptionStrict>Off</OptionStrict>\n"
    "    <OptionInfer>On</OptionInfer>\n"
    "    <LangVersion>16.9</LangVersion>\n"
    "  </PropertyGroup>\n"
    "</Project>\n"
)


def _build_program(json_text: str) -> str:
    """Return a runnable VB.NET program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=VisualBasic(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=2,
    )
    preamble = "\n".join(result.preamble)
    body_preamble = "\n".join(result.body_preamble)
    return (
        f"{preamble}\n"
        "Imports System\n"
        "Imports System.Text.Json\n"
        f"{body_preamble}\n"
        "Module Program\n"
        "    Sub Main()\n"
        f"{result.code}\n"
        f"        Console.Write(JsonSerializer.Serialize({_VAR_NAME}))\n"
        "    End Sub\n"
        "End Module\n"
    )


def main() -> None:
    """Round-trip the shared document through the VB.NET backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    dotnet = shutil.which(cmd="dotnet") or "dotnet"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Program.vb",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    dotnet,
                    "run",
                    "--project",
                    "fixture.vbproj",
                    "--nologo",
                ],
                failure_label="dotnet run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        extra_files={"fixture.vbproj": _VBPROJ},
    )


if __name__ == "__main__":
    main()
