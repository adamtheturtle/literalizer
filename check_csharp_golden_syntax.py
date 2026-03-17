"""Check syntax of C# golden files using ``dotnet build``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_DOTNET_ENV = {
    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
    "DOTNET_NOLOGO": "1",
}


def _target_framework(dotnet_path: str) -> str:
    """Return the target framework moniker for the installed
    ``dotnet``.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        dotnet_tmp = Path(tmpdir) / "tmp"
        dotnet_tmp.mkdir()
        env = os.environ.copy()
        env.update(
            {
                "TMPDIR": dotnet_tmp.as_posix(),
                "HOME": dotnet_tmp.as_posix(),
                **_DOTNET_ENV,
            }
        )
        result = subprocess.run(
            args=[dotnet_path, "--version"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
    version = result.stdout.strip()
    major_minor = ".".join(version.split(sep=".")[:2])
    return f"net{major_minor}"


def main() -> None:
    """Check syntax of each given C# golden file."""
    dotnet_path = shutil.which(cmd="dotnet")

    if dotnet_path is None:
        return
    target_framework = _target_framework(dotnet_path=dotnet_path)
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8")

        csproj = (
            '<Project Sdk="Microsoft.NET.Sdk">\n'
            "  <PropertyGroup>\n"
            "    <OutputType>Exe</OutputType>\n"
            f"    <TargetFramework>{target_framework}</TargetFramework>\n"
            "    <Nullable>disable</Nullable>\n"
            "    <ImplicitUsings>enable</ImplicitUsings>\n"
            "  </PropertyGroup>\n"
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
                    **_DOTNET_ENV,
                }
            )
            result = subprocess.run(
                args=[dotnet_path, "build", csproj_path.as_posix()],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: C# syntax error\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
