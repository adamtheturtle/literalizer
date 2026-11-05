"""Independent CI oracle for freshly generated canonical source."""

import difflib
import functools
import shutil
import subprocess
from pathlib import Path

from literalizer.languages import ALL_LANGUAGES

_PROFILE = Path(__file__).parents[1] / "objective-c.clang-format"
_ORACLE_VERSION = "23.1.3"


@functools.cache
def formatter_path() -> str:
    """Reject an accidentally upgraded or missing development
    formatter.
    """
    executable = shutil.which(cmd="clang-format")
    if executable is None:
        message = "Install the pinned source-format dependency group"
        raise FileNotFoundError(message)
    result = subprocess.run(  # noqa: S603 - fixed tool and arguments
        args=[executable, "--version"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.stdout.strip() != f"clang-format version {_ORACLE_VERSION}":
        message = f"Expected clang-format {_ORACLE_VERSION}: {result.stdout}"
        raise AssertionError(message)
    return executable


def has_canonical_profile(*, path: Path) -> bool:
    """Identify the owned profile through declared producer
    capabilities.
    """
    return any(
        language.supports_canonical_source_format
        and path.name.startswith(f"{language.__name__}_canonical")
        and path.suffix == language.extension
        for language in ALL_LANGUAGES
    )


def check_source_format(*, contents: str, path: Path) -> None:
    """Require byte equality without modifying the generated program."""
    executable = formatter_path()
    original = contents.rstrip("\n") + "\n"
    result = subprocess.run(  # noqa: S603 - fixed pinned oracle
        args=[
            executable,
            f"--style=file:{_PROFILE}",
            "--assume-filename=example.m",
        ],
        input=original,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.stdout != original:
        difference = "".join(
            difflib.unified_diff(
                a=original.splitlines(keepends=True),
                b=result.stdout.splitlines(keepends=True),
                fromfile=f"{path} (fresh canonical request)",
                tofile=f"clang-format {_ORACLE_VERSION}",
            )
        )
        message = (
            f"Canonical source changed under {_PROFILE}:\n{difference[:8000]}"
        )
        raise AssertionError(message)
