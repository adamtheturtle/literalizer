"""Check and execute D fixtures with the same commands locally and in
CI.
"""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command


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
        run_bounded_command(
            args=[*arguments, *sources],
            fixture=f"D {'compile'}: {fixture}",
            timeout_seconds=timeout,
            cwd=root,
        )
        if phase == "execution":
            run_bounded_command(
                args=[root / "run"],
                fixture=f"D {phase}: {fixture}",
                timeout_seconds=timeout,
                cwd=root,
            )


@click.command()
@click.option("--compiler", type=str, default="dmd", envvar="DC")
def main(*, compiler: str) -> None:
    """Validate selected fixtures with isolated temporary compiler
    output.
    """
    jobs = os.cpu_count()
    timeout = 60.0
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
