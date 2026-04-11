"""Shared helpers for ``check_*_syntax.py`` scripts."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

DOTNET_ENV = {
    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
    "DOTNET_NOLOGO": "1",
}


def dotnet_target_framework(dotnet_path: str) -> str:
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
                **DOTNET_ENV,
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


def fail_on_error(
    result: subprocess.CompletedProcess[str],
    *,
    filename: str,
    label: str,
) -> None:
    """Write an error message and exit if *result* indicates failure."""
    if result.returncode != 0:
        msg = f"{filename}: {label}\n{result.stderr}{result.stdout}"
        sys.stderr.write(msg)
        sys.exit(1)
