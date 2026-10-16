"""Measure issue #5264 with the public API and bounded compiler commands.

Run from a pinned toolchain environment; see the deep-compiler-cost workflow.
Timeouts are measurements, not syntax failures or whole-job cancellations.
Generated sources, commands, diagnostics and tool versions remain in --output.
"""

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import NotRequired, TypedDict

import literalizer
from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Cpp, Swift
from scripts.bounded_command import bounded_command


class _Options(argparse.Namespace):
    """Arguments validated and populated by argparse."""

    language: str
    compiler: str
    revision: str
    output: Path
    depths: list[int]
    timeout: float


class _CommandResult(TypedDict):
    """A command outcome retained in the JSON report."""

    command: list[str]
    elapsed_seconds: float
    returncode: int
    outcome: str


class _Measurement(TypedDict):
    """A depth's compiler and runtime measurements."""

    depth: int
    syntax: _CommandResult
    build: NotRequired[_CommandResult]
    run: NotRequired[_CommandResult]


def _program(*, language: str, depth: int) -> tuple[str, str]:
    """Generate the public API workload and its value check."""
    source = '{"deep":' + "[" * depth + "1" + "]" * depth + "}"
    spec = Cpp(module_name="main") if language == "cpp" else Swift()
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=spec,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    if language == "swift":
        expected_type = (
            "Swift.Dictionary<Swift.String, "
            + "Swift.Array<" * depth
            + "Swift.Int"
            + ">" * depth
            + ">"
        )
        program = (
            "import Foundation\n"
            f"{result.code}\n"
            "precondition(String(reflecting: type(of: my_data)) == "
            f'"{expected_type}")\n'
            "let encoded = try JSONSerialization.data(\n"
            "    withJSONObject: my_data)\n"
            "FileHandle.standardOutput.write(encoded)\n"
        )
    else:
        checks = ['const auto& level0 = my_data.at("deep");']
        for level in range(depth):
            checks.extend(
                (
                    f"if (level{level}.size() != 1) {{ return 1; }}",
                    f"const auto& level{level + 1} = level{level}.at(0);",
                )
            )
        checks.append(f"return level{depth} != 1;")
        # Insert the value check before the public main wrapper closes.
        body, closer = result.code.rsplit(sep="}", maxsplit=1)
        program = body + "\n".join(checks) + "\n}" + closer
    return program, source


def _measure(
    *, args: list[str], label: str, timeout: float, output: Path
) -> _CommandResult:
    """Retain one bounded command's outcome without losing later
    depths.
    """
    command = bounded_command(
        args=args, fixture=label, timeout_seconds=timeout
    )
    start = time.monotonic()
    completed = subprocess.run(args=command, capture_output=True, check=False)
    elapsed_seconds = time.monotonic() - start
    _ = output.with_suffix(suffix=".stdout").write_bytes(data=completed.stdout)
    _ = output.with_suffix(suffix=".stderr").write_bytes(data=completed.stderr)
    outcome = "success"
    if completed.returncode != 0:
        outcome = "command_error"
        if (
            completed.returncode in {124, 137}
            and b"sending signal KILL" in completed.stderr
        ):
            outcome = "command_deadline"
    return {
        "command": command,
        "elapsed_seconds": elapsed_seconds,
        "returncode": completed.returncode,
        "outcome": outcome,
    }


def main() -> None:
    """Write measurements and value-check results for each requested depth."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--language", choices=("cpp", "swift"), required=True
    )
    _ = parser.add_argument("--compiler", required=True)
    _ = parser.add_argument("--revision", required=True)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--depths", type=int, nargs="+", required=True)
    _ = parser.add_argument("--timeout", type=float, required=True)
    options = parser.parse_args(namespace=_Options())
    if options.timeout <= 0 or any(depth < 0 for depth in options.depths):
        parser.error(
            message="timeout must be positive and depths non-negative"
        )
    options.output.mkdir(parents=True, exist_ok=False)
    version = subprocess.run(
        args=[options.compiler, "--version"],
        capture_output=True,
        check=True,
        timeout=10,
    )
    measurements: list[_Measurement] = []
    report = {
        "revision": options.revision,
        "library_path": literalizer.__file__,
        "platform": platform.platform(),
        "compiler_version": version.stdout.decode(),
        "timeout_seconds": options.timeout,
        "measurements": measurements,
    }
    for depth in options.depths:
        name = f"{options.language}-depth-{depth}"
        program, expected = _program(language=options.language, depth=depth)
        path = options.output / f"{name}.{options.language}"
        _ = path.write_text(data=program, encoding="utf-8")
        executable = options.output / name
        flags = ["-std=c++20", "-Werror"]
        syntax = ["-fsyntax-only"]
        if options.language == "swift":
            flags = ["-swift-version", "5", "-warnings-as-errors"]
            syntax = ["-typecheck"]
        measurement: _Measurement = {
            "depth": depth,
            "syntax": _measure(
                args=[options.compiler, *flags, *syntax, str(object=path)],
                label=name,
                timeout=options.timeout,
                output=options.output / f"{name}-syntax",
            ),
        }
        measurements.append(measurement)
        if measurement["syntax"]["outcome"] == "success":
            measurement["build"] = _measure(
                args=[
                    options.compiler,
                    *flags,
                    str(object=path),
                    "-o",
                    str(object=executable),
                ],
                label=name,
                timeout=options.timeout,
                output=options.output / f"{name}-build",
            )
            if measurement["build"]["outcome"] == "success":
                measurement["run"] = _measure(
                    args=[str(object=executable.resolve())],
                    label=name,
                    timeout=options.timeout,
                    output=options.output / f"{name}-run",
                )
                if (
                    options.language == "swift"
                    and measurement["run"]["outcome"] == "success"
                ):
                    actual = (
                        options.output / f"{name}-run.stdout"
                    ).read_text()
                    if json.loads(s=actual) != json.loads(s=expected):
                        measurement["run"]["outcome"] = "value_mismatch"
        _ = (options.output / "report.json").write_text(
            data=json.dumps(obj=report, indent=2) + "\n", encoding="utf-8"
        )
        _ = sys.stdout.write(
            f"{name}: {measurement['syntax']['outcome']}, "
            f"{measurement['syntax']['elapsed_seconds']:.3f}s\n"
        )
        _ = sys.stdout.flush()

    if any(
        step["outcome"] not in {"success", "command_deadline"}
        for measurement in measurements
        for step in (
            measurement["syntax"],
            measurement.get("build"),
            measurement.get("run"),
        )
        if step is not None
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
