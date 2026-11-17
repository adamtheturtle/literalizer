"""Check and execute Bash, Ruby and JavaScript fixtures locally or in
CI.
"""

import concurrent.futures
import dataclasses
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

_CASES_DIR = Path("tests/integration/cases")


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Backend:
    """The interpreter and syntax check used by an existing native job."""

    executable: str
    extension: str
    syntax_argument: str
    # Omitted parser names use the interpreter itself.
    syntax_executable: str | None = None  # noqa: NOD001
    arguments: tuple[str, ...] = ()  # noqa: NOD001 - omitted flags mean no prefix


_BACKENDS = {
    "lua": _Backend(
        executable="lua",
        extension=".lua",
        syntax_argument="-p",
        syntax_executable="luac",
    ),
    "bash": _Backend(executable="bash", extension=".sh", syntax_argument="-n"),
    "php": _Backend(executable="php", extension=".php", syntax_argument="-l"),
    "perl": _Backend(
        executable="perl",
        extension=".pl",
        syntax_argument="-c",
        arguments=("-Mstrict=subs",),
    ),
    "ruby": _Backend(executable="ruby", extension=".rb", syntax_argument="-c"),
    "javascript": _Backend(
        executable="node", extension=".js", syntax_argument="--check"
    ),
}


def _run(*, arguments: list[str], label: str, timeout: float) -> None:
    """Report the fixture, phase and command, with a process deadline."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments, fixture=label, timeout_seconds=timeout
        ),
        check=True,
    )


@click.command()
@click.argument("backend", type=click.Choice(choices=tuple(_BACKENDS)))
@click.option(
    "--case", "case_name", type=str, help="Select one case directory."
)
@click.option(
    "--check",
    "check_kind",
    type=click.Choice(choices=("all", "syntax", "execution")),
    default="all",
    show_default=True,
)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout",
    type=click.FloatRange(min=0, min_open=True),
    default=60.0,
    show_default=True,
    help="Deadline in seconds for each native command.",
)
def main(
    backend: str,
    case_name: str | None,
    check_kind: str,
    jobs: int,
    timeout: float,
) -> None:
    """Validate the selected BACKEND's fixtures, retaining every version.

    Syntax checks complete before execution starts. The independently
    authored assertions in consumer programs run unchanged.
    """
    config = _BACKENDS[backend]
    fixtures = sorted(
        path
        for path in _CASES_DIR.rglob(pattern=f"*{config.extension}")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No {backend} fixtures: {case_name!r}"
        )
    executable = shutil.which(cmd=config.executable)
    if executable is None:
        raise click.ClickException(
            message=f"Missing interpreter: {config.executable}"
        )
    if backend == "bash":
        _run(
            arguments=[
                executable,
                "-c",
                (
                    "(( BASH_VERSINFO[0] > 5 || "
                    "(BASH_VERSINFO[0] == 5 && BASH_VERSINFO[1] >= 1) )) "
                    "|| { echo 'Bash 5.1 or later is required' >&2; exit 1; }"
                ),
            ],
            label="Bash V5_1 interpreter floor",
            timeout=timeout,
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            if check_kind not in ("all", phase):
                continue
            phase_executable = executable
            if phase == "syntax" and config.syntax_executable is not None:
                parser = shutil.which(cmd=config.syntax_executable)
                if parser is None:
                    raise click.ClickException(
                        message=f"Missing parser: {config.syntax_executable}"
                    )
                phase_executable = parser
            futures = [
                executor.submit(
                    _run,
                    arguments=[
                        phase_executable,
                        *config.arguments,
                        *(
                            [config.syntax_argument]
                            if phase == "syntax"
                            else []
                        ),
                        str(object=fixture),
                    ],
                    label=f"{backend} {phase}: {fixture}",
                    timeout=timeout,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
