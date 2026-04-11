"""Check syntax of a C# golden file using ``dotnet build``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_syntax_helpers import (
    DOTNET_ENV,
    dotnet_target_framework,
    fail_on_error,
)


def main() -> None:
    """Check syntax of the given C# golden file."""
    filename = sys.argv[1]
    dotnet_path: str = shutil.which(cmd="dotnet") or "dotnet"
    target_framework = dotnet_target_framework(dotnet_path=dotnet_path)
    content = Path(filename).read_text(encoding="utf-8")

    csproj = (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        "  <PropertyGroup>\n"
        "    <OutputType>Exe</OutputType>\n"
        f"    <TargetFramework>{target_framework}</TargetFramework>\n"
        "    <Nullable>disable</Nullable>\n"
        "    <ImplicitUsings>disable</ImplicitUsings>\n"
        "    <EnableDefaultCompileItems>false"
        "</EnableDefaultCompileItems>\n"
        "    <EnableDefaultEmbeddedResourceItems>false"
        "</EnableDefaultEmbeddedResourceItems>\n"
        "  </PropertyGroup>\n"
        "  <ItemGroup>\n"
        '    <Compile Include="Program.cs" />\n'
        "  </ItemGroup>\n"
        "</Project>\n"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        cs_path = Path(tmpdir) / "Program.cs"
        csproj_path = Path(tmpdir) / "check.csproj"
        cs_path.write_text(data=content, encoding="utf-8")
        csproj_path.write_text(data=csproj, encoding="utf-8")
        dotnet_tmp = Path(tmpdir) / "tmp"
        dotnet_tmp.mkdir()
        env = os.environ.copy()
        env.update(
            {
                "TMPDIR": dotnet_tmp.as_posix(),
                "HOME": dotnet_tmp.as_posix(),
                **DOTNET_ENV,
            }
        )
        result = subprocess.run(
            args=[dotnet_path, "build", csproj_path.as_posix()],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
    fail_on_error(
        result=result,
        filename=filename,
        label="dotnet build failed",
    )


if __name__ == "__main__":
    main()
