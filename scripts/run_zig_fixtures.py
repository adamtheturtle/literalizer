"""Compile and execute Zig fixtures together in one warm driver."""

import re
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
@click.argument("version", type=click.Choice(choices=("v0_12",)))
def main(version: str) -> None:
    """Compile and execute every fixture for VERSION in a single batch."""
    compiler = shutil.which(cmd="zig")
    if compiler is None:
        raise click.ClickException(message="The zig executable is required.")
    fixtures = fixture_paths(extension=".zig", version=version)
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Zig {version} fixtures.")
    with tempfile.TemporaryDirectory(suffix="-literalizer-zig") as temporary:
        directory = Path(temporary)
        imports: list[str] = []
        calls: list[str] = []
        for index, fixture in enumerate(iterable=fixtures):
            name = f"fixture_{index}.zig"
            # Give each main function a name the driver can call.
            source = re.sub(
                pattern=rb"^pub fn main\(",
                repl=f"pub fn fixture{index}(".encode(),
                string=fixture.read_bytes(),
                flags=re.MULTILINE,
            )
            _ = (directory / name).write_bytes(data=source)
            imports.append(f'const fix{index} = @import("{name}");')
            calls.append(f"    fix{index}.fixture{index}();")
            click.echo(message=f"{name} <- {fixture}")
        driver = directory / "main.zig"
        _ = driver.write_text(
            data="\n".join(
                [*imports, "pub fn main() void {", *calls, "}", ""]
            ),
            encoding="utf-8",
        )
        run_bounded_command(
            args=[compiler, "run", driver],
            fixture=(
                f"Zig {version} compile/execution: {len(fixtures)} fixtures"
            ),
            timeout_seconds=600.0,
            cwd=None,
        )


if __name__ == "__main__":
    main()
