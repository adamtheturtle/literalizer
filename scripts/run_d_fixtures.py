"""Check and execute D fixtures with the same commands locally and in
CI.
"""

import concurrent.futures
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _command(
    *,
    arguments: list[str | Path],
    fixture: Path,
    phase: str,
    timeout: float,
    directory: Path | None,
) -> None:
    """Report the original fixture and retain native diagnostics."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments,
            fixture=f"D {phase}: {fixture}",
            timeout_seconds=timeout,
        ),
        cwd=directory,
        check=True,
    )


def _run(
    *,
    fixture: Path,
    phase: str,
    tools: dict[str, str],
    timeout: float,
    compiler: str,
) -> None:
    """Compile in private directories and call public function
    defaults.
    """
    with tempfile.TemporaryDirectory(suffix="-literalizer-d") as directory:
        root = Path(directory)
        _ = shutil.copyfile(src=fixture, dst=root / "check.d")
        sources = ["check.d"]
        if fixture.parent.name == "default_module_names":
            _ = (root / "driver.d").write_text(
                data="import check; void main() { check.Module(); }\n"
            )
            sources.append("driver.d")
        arguments: list[str | Path] = [tools[compiler], "-w"]
        if phase == "syntax":
            arguments += ["-o-", "-c"]
        else:
            arguments += [f"-of={root / 'run'}", f"-od={root}"]
        _command(
            arguments=[*arguments, *sources],
            fixture=fixture,
            phase="compile",
            timeout=timeout,
            directory=root,
        )
        if phase == "execution":
            _command(
                arguments=[root / "run"],
                fixture=fixture,
                phase=phase,
                timeout=timeout,
                directory=root,
            )


@click.command()
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
@click.option("--compiler", type=str, default="dmd", envvar="DC")
def main(
    *,
    check_kind: str,
    jobs: int,
    timeout: float,
    compiler: str,
) -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    fixtures = sorted(
        path
        for root in (
            Path("tests/integration/cases"),
            Path("tests/integration/default_module_names"),
        )
        for path in root.rglob(pattern="*.d")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No D fixtures.")
    tools: dict[str, str] = {}
    for name in (compiler,):
        executable = shutil.which(cmd=name)
        if executable is None:
            raise click.ClickException(
                message=f"Missing required tool: {name}"
            )
        tools[name] = executable
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for phase in ("syntax", "execution"):
            if check_kind not in {"all", phase}:
                continue
            futures = [
                executor.submit(
                    _run,
                    fixture=fixture,
                    phase=phase,
                    tools=tools,
                    timeout=timeout,
                    compiler=compiler,
                )
                for fixture in fixtures
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
