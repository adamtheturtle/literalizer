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

# String present in dotnet stderr when the NuGet mutex race occurs.
# Used to distinguish infrastructure noise from real compilation errors.
_NUGET_MUTEX_MARKER = "NuGet-Migrations"

# Number of times to retry a dotnet invocation that failed only because of
# the shared-memory mutex race condition (not a real C# error).
_MUTEX_RETRY_LIMIT = 3


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


def _build(
    dotnet_path: str,
    csproj_path: Path,
) -> subprocess.CompletedProcess[str]:
    """Run ``dotnet build``, retrying on transient NuGet mutex failures.

    Returns the last result, which callers should inspect for success or
    failure.
    """
    remaining = _MUTEX_RETRY_LIMIT
    while True:
        result = subprocess.run(
            args=[dotnet_path, "build", str(csproj_path)],  # type: ignore[call-overload]
            capture_output=True,
            text=True,
            check=False,
            env=_DOTNET_ENV,
        )
        remaining -= 1
        if result.returncode == 0:
            # Successful build — no need to retry.
            return result
        if _NUGET_MUTEX_MARKER not in result.stderr:
            # Genuine C# compilation error, not a transient mutex race.
            return result
        if remaining == 0:
            # All retries exhausted; propagate the last (mutex) failure.
            return result
        # The failure is the NuGet shared-memory mutex race (errno==EEXIST).
        # Retry in case the next attempt avoids the contention.


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
            result = _build(
                dotnet_path=dotnet_path,
                csproj_path=csproj_path,
            )
        if result.returncode != 0:
            msg = (
                f"{filename}: C# syntax error\n{result.stderr}{result.stdout}"
            )
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
