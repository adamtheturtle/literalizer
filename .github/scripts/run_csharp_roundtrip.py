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

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import CSharp

_VAR_NAME = "myData"
_LABEL = "CSharp"
_EXCLUDED_KEYS = ("biginteger",)

# ``LangVersion 10`` matches ``CSharp.language_version`` in
# ``src/literalizer/languages/csharp.py`` and the ``LanguageVersion.CSharp10``
# pin in ``.github/scripts/lint-csharp/Program.cs``; keep them in sync.
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
    parsed: dict[str, object] = json.loads(s=json_text)
    for key in _EXCLUDED_KEYS:
        parsed.pop(key, None)
    trimmed_json = json.dumps(obj=parsed)
    result = literalize(
        source=trimmed_json,
        input_format=InputFormat.JSON,
        language=CSharp(sequence_format=CSharp.sequence_formats.ARRAY),
        pre_indent_level=2,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME),
        wrap_in_file=False,
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
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        (tmpdir / "Program.cs").write_text(data=program, encoding="utf-8")
        (tmpdir / "fixture.csproj").write_text(data=_CSPROJ, encoding="utf-8")
        run_result = subprocess.run(
            args=[dotnet, "run", "--project", "fixture.csproj", "--nologo"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
    if run_result.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: dotnet run error\n{run_result.stdout}"
            f"{run_result.stderr}",
        )
        sys.stderr.write(f"\nProgram:\n{program}\n")
        sys.exit(1)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=run_result.stdout,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
