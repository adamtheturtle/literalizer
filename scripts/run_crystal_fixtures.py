"""Build one warm compiler driver from the selected native sources."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


@click.command()
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=600.0
)
def main(*, timeout: float) -> None:
    """Compile and execute fixtures without rewriting their module
    names.
    """
    roots = (
        Path("tests/integration/cases"),
        Path("tests/integration/default_module_names"),
    )
    fixtures = sorted(
        fixture for root in roots for fixture in root.rglob(pattern="*.cr")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Crystal fixtures.")
    compiler = shutil.which(cmd="crystal")
    if compiler is None:
        raise click.ClickException(
            message="The crystal executable is required."
        )
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-crystal"
    ) as temporary:
        directory = Path(temporary)
        imports: list[str] = []
        for fixture in fixtures:
            stem = fixture.stem.rsplit(sep="@", maxsplit=1)[0]
            name = f"Fixture_{fixture.parent.name}_{stem}"
            _ = shutil.copyfile(src=fixture, dst=directory / f"{name}.cr")
            imports.append(f'require "./{name}"')
            click.echo(message=f"{name}.cr <- {fixture}")
        driver = directory / "run_all.cr"
        _ = driver.write_text(data="\n".join(imports) + "\n", encoding="utf-8")
        _ = subprocess.run(
            args=bounded_command(
                args=[compiler, "run", "--error-on-warnings", driver],
                fixture=f"Crystal: {len(fixtures)} fixtures",
                timeout_seconds=timeout,
            ),
            check=True,
        )


if __name__ == "__main__":
    main()
