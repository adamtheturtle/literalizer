"""Compiler benchmarks for compiling generated singleton arrays (#5264).

Source generation and compiler discovery are outside the measured section.
A probe before measurement records command deadlines without publishing
a completed compiler timing. Correctness belongs to the integration
golden suite.
"""

import json
import subprocess
from pathlib import Path

import pytest
from pytest_codspeed import BenchmarkFixture

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.languages import Cpp, Swift
from scripts.bounded_command import bounded_command


@pytest.mark.parametrize(
    argnames=("language", "compiler", "flags", "extension"),
    argvalues=[
        pytest.param(
            Cpp(module_name="main"),
            "clang++",
            ["-std=c++20", "-Werror", "-fsyntax-only"],
            "cpp",
            id="cpp",
        ),
        pytest.param(
            Swift(),
            "swiftc",
            ["-swift-version", "5", "-warnings-as-errors", "-typecheck"],
            "swift",
            id="swift",
        ),
    ],
)
@pytest.mark.parametrize(argnames="depth", argvalues=[0, 16, 20, 30])
@pytest.mark.benchmark(max_rounds=3, max_time=180)
def test_singleton_array_compiler_cost(
    *,
    benchmark: BenchmarkFixture,
    tmp_path: Path,
    language: Language,
    compiler: str,
    flags: list[str],
    extension: str,
    depth: int,
) -> None:
    """Measure syntax/type checking with a per-command 60-second
    deadline.
    """
    source = '{"deep":' + "[" * depth + "1" + "]" * depth + "}"
    program = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    ).code
    path = tmp_path / f"singleton-array.{extension}"
    _ = path.write_text(data=program, encoding="utf-8")
    version = subprocess.run(  # noqa: S603 - compiler is a fixed test parameter.
        args=[compiler, "--version"],
        shell=False,
        capture_output=True,
        check=True,
        timeout=10,
    )
    _ = (tmp_path / "compiler-version.txt").write_bytes(data=version.stdout)
    command = bounded_command(
        args=[compiler, *flags, path],
        fixture=f"{extension}-depth-{depth}",
        timeout_seconds=60,
    )
    _ = (tmp_path / "command.json").write_text(
        data=json.dumps(obj=command, indent=2) + "\n", encoding="utf-8"
    )
    stderr_path = tmp_path / "compiler.stderr"
    with (
        (tmp_path / "compiler.stdout").open(mode="wb") as stdout,
        stderr_path.open(mode="wb") as stderr,
    ):
        # Probe before entering CodSpeed so a known deadline produces no
        # benchmark sample. Errors during measured rounds fail the test.
        try:
            _ = subprocess.run(  # noqa: S603 - command uses fixed compiler flags.
                args=command,
                stdout=stdout,
                stderr=stderr,
                check=True,
                shell=False,
            )
        except subprocess.CalledProcessError as error:
            if (
                error.returncode in {124, 137}
                and b"sending signal KILL" in stderr_path.read_bytes()
            ):
                pytest.skip(
                    reason="Compiler command exceeded 60s; timing unavailable "
                    f"(see {stderr_path})"
                )
            raise
        _ = benchmark(
            subprocess.run,
            args=command,
            stdout=stdout,
            stderr=stderr,
            check=True,
            shell=False,
        )
