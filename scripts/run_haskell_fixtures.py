"""Share the warm Haskell compiler and include public default modules."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _stage(*, fixtures: list[Path], workspace: Path) -> list[str]:
    """Preserve source module identities and report every copied
    fixture.
    """
    names: list[str] = []
    for fixture in fixtures:
        stem = fixture.stem.rsplit(sep="@", maxsplit=1)[0]
        name = (
            "Check"
            if fixture.parent.name == "default_module_names"
            else f"Fixture_{fixture.parent.name}_{stem}"
        )
        destination = workspace / f"{name}.hs"
        _ = shutil.copyfile(src=fixture, dst=destination)
        click.echo(message=f"{destination.name} <- {fixture}")
        names.append(name)
    return names


def _run(
    *, arguments: list[str | Path], label: str, workspace: Path, timeout: float
) -> None:
    """Bound the native command while retaining compiler diagnostics."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments, fixture=label, timeout_seconds=timeout
        ),
        cwd=workspace,
        check=True,
    )


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
    _run(
        arguments=[
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
        label="Haskell compile",
        workspace=workspace,
        timeout=timeout,
    )
    _run(
        arguments=[binary],
        label="Haskell execution",
        workspace=workspace,
        timeout=timeout,
    )


@click.command()
@click.option("--case", "case_name", type=str)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=600.0
)
def main(*, case_name: str | None, timeout: float) -> None:
    """Compile and run a case or the complete native fixture
    collection.
    """
    fixtures = sorted(
        path
        for root in (
            Path("tests/integration/cases"),
            Path("tests/integration/default_module_names"),
        )
        for path in root.rglob(pattern="*.hs")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No Haskell fixtures: {case_name!r}"
        )
    executable = shutil.which(cmd="ghc")
    if executable is None:
        raise click.ClickException(message="The ghc executable is required.")
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-haskell"
    ) as directory:
        workspace = Path(directory)
        names = _stage(fixtures=fixtures, workspace=workspace)
        _validate(
            executable=executable,
            names=names,
            workspace=workspace,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
