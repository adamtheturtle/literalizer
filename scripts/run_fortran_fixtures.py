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
@click.option("--case", "case_name", type=str)
@click.option(
    "--version",
    "versions",
    type=click.Choice(choices=("v2003", "v2008")),
    multiple=True,
    default=("v2003", "v2008"),
)
@click.option(
    "--check",
    "check_kind",
    type=click.Choice(choices=("all", "syntax", "execution")),
    default="all",
)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(
    *,
    case_name: str | None,
    versions: tuple[str, ...],
    check_kind: str,
    jobs: int,
    timeout: float,
) -> None:
    """Check selected cases at their declared language standards."""
    roots = (
        Path("tests/integration/cases"),
        Path("tests/integration/default_module_names"),
    )
    fixtures = sorted(
        fixture
        for root in roots
        for fixture in root.rglob(pattern="*.f90")
        if case_name is None or fixture.parent.name == case_name
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
                message=f"No Fortran {version} fixtures: {case_name!r}"
            )
    compiler = shutil.which(cmd="gfortran")
    if compiler is None:
        raise click.ClickException(
            message="The gfortran executable is required."
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            if check_kind not in ("all", phase):
                continue
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
