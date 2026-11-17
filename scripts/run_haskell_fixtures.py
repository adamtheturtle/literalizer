"""Share the warm Haskell compiler and include public default modules."""

import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from scripts.fixture_staging import stage_fixture_modules


def _validate(
    *, executable: str, names: list[str], workspace: Path, timeout: float
) -> None:
    """Build all modules once with the existing strict language
    settings.
    """
    source = (
        "module Main where\n"
        + "".join(f"import qualified {name}\n" for name in names)
        + "main :: IO ()\nmain = do\n"
        + "".join(f"  {name}.main\n" for name in names)
    )
    _ = (workspace / "Main.hs").write_text(data=source)
    output = workspace / "build"
    output.mkdir()
    binary = output / "run"
    run_bounded_command(
        args=[
            executable,
            "-XGHC2021",
            "-Wall",
            "-Werror",
            "-j",
            "-outputdir",
            output,
            "-o",
            binary,
            "Main.hs",
        ],
        fixture="Haskell compile",
        timeout_seconds=timeout,
        cwd=workspace,
    )
    run_bounded_command(
        args=[binary],
        fixture="Haskell execution",
        timeout_seconds=timeout,
        cwd=workspace,
    )


@click.command()
def main() -> None:
    """Compile and run the complete native fixture collection."""
    timeout = 600.0
    fixtures = sorted(
        path
        for root in (
            Path("tests/integration/cases"),
            Path("tests/integration/default_module_names"),
        )
        for path in root.rglob(pattern="*.hs")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Haskell fixtures.")
    executable = shutil.which(cmd="ghc")
    if executable is None:
        raise click.ClickException(message="The ghc executable is required.")
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-haskell"
    ) as directory:
        workspace = Path(directory)
        names = stage_fixture_modules(
            fixtures=fixtures, workspace=workspace, default_module_name="Check"
        )
        _validate(
            executable=executable,
            names=names,
            workspace=workspace,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
