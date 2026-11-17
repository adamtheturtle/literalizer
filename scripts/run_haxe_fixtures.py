"""Share the warm Haxe compiler and include public default modules."""

import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command


def _stage(*, fixtures: list[Path], workspace: Path) -> list[str]:
    """Preserve source module identities and report every copied
    fixture.
    """
    names: list[str] = []
    for fixture in fixtures:
        stem = fixture.stem.rsplit(sep="@", maxsplit=1)[0]
        name = (
            "Main"
            if fixture.parent.name == "default_module_names"
            else f"Fixture_{fixture.parent.name}_{stem}"
        )
        destination = workspace / f"{name}.hx"
        _ = shutil.copyfile(src=fixture, dst=destination)
        click.echo(message=f"{destination.name} <- {fixture}")
        names.append(name)
    return names


def _validate(
    *, executable: str, names: list[str], workspace: Path, timeout: float
) -> None:
    """Interpret one driver that calls every unchanged consumer
    program.
    """
    source = (
        "class Driver {\n  public static function main() {\n"
        + "".join(f"    {name}.main();\n" for name in names)
        + "  }\n}\n"
    )
    _ = (workspace / "Driver.hx").write_text(data=source)
    run_bounded_command(
        args=[executable, "-p", workspace, "--main", "Driver", "--interp"],
        fixture="Haxe compile and execution",
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
        for path in root.rglob(pattern="*.hx")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Haxe fixtures.")
    executable = shutil.which(cmd="haxe")
    if executable is None:
        raise click.ClickException(message="The haxe executable is required.")
    with tempfile.TemporaryDirectory(suffix="-literalizer-haxe") as directory:
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
