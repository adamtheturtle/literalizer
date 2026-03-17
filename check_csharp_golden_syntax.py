"""Check syntax of C# golden files using ``dotnet build``."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# A shared home directory persisted for the lifetime of this process.
#
# When ``dotnet`` runs, NuGet checks whether migrations have been
# applied by looking for state files under ``$HOME/.nuget/NuGet/``.
# If they haven't, it acquires a named mutex
# (``NuGet-Migrations``), runs migrations, and writes the state
# files.  Running ``dotnet`` a second time from the same script—
# once in ``_target_framework`` and once per golden file—makes
# both calls try to ``mkdir("/tmp/.dotnet/shm/session<hash>")``
# for the mutex; the second call fails with ``EEXIST`` because
# the directory was left behind by the first.
#
# Using a shared ``HOME`` means the migration state files written
# by the *first* invocation are visible to all later invocations,
# which therefore skip migrations entirely and never touch the
# mutex session directory.
_DOTNET_HOME: Path = Path(tempfile.mkdtemp(prefix="dotnet-home-"))


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
                "HOME": _DOTNET_HOME.as_posix(),
                "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
                "DOTNET_NOLOGO": "1",
                "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
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
    dotnet_path: str = shutil.which(cmd="dotnet") or "dotnet"
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
                    "HOME": _DOTNET_HOME.as_posix(),
                    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
                    "DOTNET_NOLOGO": "1",
                    "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
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
