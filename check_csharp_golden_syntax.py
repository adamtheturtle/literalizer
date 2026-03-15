"""Check syntax of C# golden files using ``dotnet build``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Environment variables that suppress dotnet's first-time initialization.
# Without these, dotnet tries to create a shared-memory mutex directory
# (/tmp/.dotnet/shm/sessionN) during NuGet migration.  In CI environments
# multiple parallel jobs race to create that directory; the loser gets
# errno == EEXIST and raises an IOException, causing a false "C# syntax
# error" even when the source is perfectly valid.
_DOTNET_ENV: dict[str, str] = {
    **os.environ,
    # Skip NuGet migration and telemetry on first run.
    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
    # Suppress the dotnet welcome/logo banner written to stderr.
    "DOTNET_NOLOGO": "1",
    # Skip downloading NuGet XML documentation files.
    "NUGET_XMLDOC_MODE": "skip",
}


def _target_framework(dotnet_path: str) -> str:
    """Return the target framework moniker for the installed
    ``dotnet``.
    """
    result = subprocess.run(
        args=[dotnet_path, "--version"],
        capture_output=True,
        text=True,
        check=False,
        env=_DOTNET_ENV,
    )
    version = result.stdout.strip()
    major_minor = ".".join(version.split(sep=".")[:2])
    return f"net{major_minor}"


def main() -> None:
    """Check syntax of each given C# golden file."""
    dotnet_path = shutil.which(cmd="dotnet") or "dotnet"
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
            result = subprocess.run(
                args=[dotnet_path, "build", str(csproj_path)],  # type: ignore[call-overload]
                capture_output=True,
                text=True,
                check=False,
                env=_DOTNET_ENV,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: C# syntax error\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
