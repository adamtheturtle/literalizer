"""Check and execute Bash, Ruby and JavaScript fixtures locally or in
CI.
"""

import concurrent.futures
import dataclasses
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Backend:
    """The interpreter and syntax check used by an existing native job."""

    executable: str
    extension: str
    syntax_argument: str | None
    # Omitted parser names use the interpreter itself.
    syntax_executable: str | None = None  # noqa: NOD001
    arguments: tuple[str, ...] = ()  # noqa: NOD001 - omitted flags mean no prefix


_BACKENDS = {
    "raku": _Backend(
        executable="raku", extension=".raku", syntax_argument="-c"
    ),
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
    "tcl": _Backend(
        executable="tclsh", extension=".tcl", syntax_argument=None
    ),
    "wren": _Backend(
        executable="wren_cli", extension=".wren", syntax_argument=None
    ),
}


def _phase_executable(*, config: _Backend, executable: str, phase: str) -> str:
    """Resolve a separate syntax parser when the backend requires one."""
    if phase != "syntax" or config.syntax_executable is None:
        return executable
    parser = shutil.which(cmd=config.syntax_executable)
    if parser is None:
        raise click.ClickException(
            message=f"Missing parser: {config.syntax_executable}"
        )
    return parser


@click.command()
@click.argument("backend", type=click.Choice(choices=tuple(_BACKENDS)))
def main(backend: str) -> None:
    """Validate the selected BACKEND's fixtures, retaining every version.

    Syntax checks complete before execution starts. The independently
    authored assertions in consumer programs run unchanged.
    """
    jobs = os.cpu_count()
    timeout = 60.0
    config = _BACKENDS[backend]
    fixtures = fixture_paths(extension=config.extension)
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No {backend} fixtures.")
    executable = shutil.which(cmd=config.executable)
    if executable is None:
        raise click.ClickException(
            message=f"Missing interpreter: {config.executable}"
        )
    if backend == "bash":
        run_bounded_command(
            args=[
                executable,
                "-c",
                (
                    "(( BASH_VERSINFO[0] > 5 || "
                    "(BASH_VERSINFO[0] == 5 && BASH_VERSINFO[1] >= 1) )) "
                    "|| { echo 'Bash 5.1 or later is required' >&2; exit 1; }"
                ),
            ],
            fixture="Bash V5_1 interpreter floor",
            timeout_seconds=timeout,
            cwd=None,
        )
    syntax_arguments = (
        [] if config.syntax_argument is None else [config.syntax_argument]
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            if phase == "syntax" and config.syntax_argument is None:
                continue
            phase_executable = _phase_executable(
                config=config, executable=executable, phase=phase
            )
            futures = [
                executor.submit(
                    run_bounded_command,
                    args=[
                        phase_executable,
                        *config.arguments,
                        *(syntax_arguments if phase == "syntax" else []),
                        str(object=fixture),
                    ],
                    fixture=f"{backend} {phase}: {fixture}",
                    timeout_seconds=timeout,
                    cwd=None,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
