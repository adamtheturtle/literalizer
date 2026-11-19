"""Syntax-check, link and execute Objective-C fixtures with Apple
Clang.
"""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.fixture_names import is_default_module_fixture
from tests.integration.list_fixtures import fixture_paths

_HEADER = Path(__file__).with_name(name="lint-objc-pch.h").resolve()
_CALLER = "int Module(void);\nint main(void) { return Module(); }\n"


def _execute(*, fixture: Path, compiler: str, pch: Path) -> None:
    """Use a private executable, with a caller for the default entry point."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-objc") as temporary:
        directory = Path(temporary)
        sources = [fixture]
        if is_default_module_fixture(path=fixture):
            caller = directory / "main.m"
            _ = caller.write_text(data=_CALLER, encoding="utf-8")
            sources.append(caller)
        binary = directory / "out"
        run_bounded_command(
            args=[
                compiler,
                "-fobjc-arc",
                "-framework",
                "Foundation",
                "-Werror",
                "-include-pch",
                pch,
                *sources,
                "-o",
                binary,
            ],
            fixture=f"Objective-C V2 link: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )
        run_bounded_command(
            args=[binary],
            fixture=f"Objective-C V2 execution: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Check every Objective-C 2.0 fixture and keep warnings fatal."""
    compiler = shutil.which(cmd="clang")
    if compiler is None:
        raise click.ClickException(message="Apple clang is required.")
    fixtures = fixture_paths(
        extension=".m",
        language="ObjectiveC",
        include_default_module_names=True,
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Objective-C fixtures.")
    with (
        tempfile.TemporaryDirectory(
            suffix="-literalizer-objc-pch"
        ) as temporary,
        concurrent.futures.ThreadPoolExecutor(
            max_workers=os.cpu_count()
        ) as executor,
    ):
        # Reuse the parsed Foundation header in both compiler passes.
        pch = Path(temporary) / "foundation.pch"
        run_bounded_command(
            args=[
                compiler,
                "-fobjc-arc",
                "-x",
                "objective-c-header",
                _HEADER,
                "-o",
                pch,
            ],
            fixture="Objective-C V2 Foundation precompiled header",
            timeout_seconds=60.0,
            cwd=None,
        )
        syntax_checks = [
            executor.submit(
                run_bounded_command,
                args=[
                    compiler,
                    "-fobjc-arc",
                    "-fsyntax-only",
                    "-Werror",
                    "-include-pch",
                    pch,
                    fixture,
                ],
                fixture=f"Objective-C V2 syntax: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for check in syntax_checks:
            check.result()
        executions = [
            executor.submit(
                _execute, fixture=fixture, compiler=compiler, pch=pch
            )
            for fixture in fixtures
        ]
        for execution in executions:
            execution.result()


if __name__ == "__main__":
    main()
