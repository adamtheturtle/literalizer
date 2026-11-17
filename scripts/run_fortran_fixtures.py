"""Validate versioned compiler fixtures in isolated temporary
directories.
"""

import concurrent.futures
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _check(
    *,
    fixture: Path,
    version: str,
    phase: str,
    compiler: str,
    timeout: float,
) -> None:
    """Keep module files private to one compiler invocation."""
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-fortran"
    ) as temporary:
        output = Path(temporary) / "run"
        arguments = [
            compiler,
            "-Werror",
            f"-std=f{version[1:]}",
            str(object=fixture.resolve()),
        ]
        arguments.extend(
            ["-fsyntax-only"]
            if phase == "syntax"
            else ["-o", str(object=output)]
        )
        _ = subprocess.run(
            args=bounded_command(
                args=arguments,
                fixture=f"Fortran {version} {phase}: {fixture}",
                timeout_seconds=timeout,
            ),
            cwd=temporary,
            check=True,
        )
        if phase == "execution":
            _ = subprocess.run(
                args=bounded_command(
                    args=[output],
                    fixture=f"Fortran {version} execution: {fixture}",
                    timeout_seconds=timeout,
                ),
                cwd=temporary,
                check=True,
            )


@click.command()
@click.option(
    "--version",
    "versions",
    type=click.Choice(choices=("v2003", "v2008")),
    multiple=True,
    default=("v2003", "v2008"),
)
def main(*, versions: tuple[str, ...]) -> None:
    """Check fixtures at their declared language standards."""
    jobs = os.cpu_count()
    timeout = 60.0
    roots = (
        Path("tests/integration/cases"),
        Path("tests/integration/default_module_names"),
    )
    fixtures = sorted(
        fixture for root in roots for fixture in root.rglob(pattern="*.f90")
    )
    selections = {
        version: tuple(
            fixture
            for fixture in fixtures
            if fixture.name.endswith(f"@{version}.f90")
        )
        for version in versions
    }
    for version, selected in selections.items():
        if len(selected) == 0:
            raise click.ClickException(
                message=f"No Fortran {version} fixtures."
            )
    compiler = shutil.which(cmd="gfortran")
    if compiler is None:
        raise click.ClickException(
            message="The gfortran executable is required."
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            futures = [
                executor.submit(
                    _check,
                    fixture=fixture,
                    version=version,
                    phase=phase,
                    compiler=compiler,
                    timeout=timeout,
                )
                for version, selected in selections.items()
                for fixture in selected
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
