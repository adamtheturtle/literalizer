"""Share the warm Haxe compiler and include public default modules."""

import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from scripts.fixture_staging import stage_fixture_modules
from tests.integration.list_fixtures import fixture_paths


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
    fixtures = fixture_paths(
        extension=".hx", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Haxe fixtures.")
    executable = shutil.which(cmd="haxe")
    if executable is None:
        raise click.ClickException(message="The haxe executable is required.")
    with tempfile.TemporaryDirectory(suffix="-literalizer-haxe") as directory:
        workspace = Path(directory)
        names = stage_fixture_modules(
            fixtures=fixtures, workspace=workspace, default_module_name="Main"
        )
        _validate(
            executable=executable,
            names=names,
            workspace=workspace,
            timeout=timeout,
        )


if __name__ == "__main__":
    main()
