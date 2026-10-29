"""Retain a bounded C++ singleton-depth compiler reproduction (#5264).

Use ``python -m scripts.measure_cpp_singleton_depth --output /tmp/probe``
This manual investigation retains inputs, generated sources, exact commands,
compiler versions, diagnostics and elapsed time. It changes no renderer or
ordinary PR workload and reports deadlines separately from compiler errors.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from time import monotonic

from pydantic import JsonValue

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import LiteralizerError
from literalizer.languages import Cpp
from scripts.bounded_command import bounded_command

_MAX_BUDGET_SECONDS = 600
_MAX_DEPTH = 48
_MAX_NODES = 128


def _shape(*, depth: int, kind: str) -> JsonValue:
    """Build a narrow spine whose node count grows linearly with depth."""
    value: JsonValue = 1
    for level in range(depth):
        if level == 0 and kind == "floating":
            value = 1.25
        value = [value]
    return value


def _nodes(*, value: JsonValue) -> int:
    """Count containers and values before paying any compiler cost."""
    if isinstance(value, list):
        return 1 + sum(_nodes(value=child) for child in value)
    if isinstance(value, dict):
        return 1 + sum(_nodes(value=child) for child in value.values())
    return 1


def _arguments() -> argparse.Namespace:
    """Validate finite input and execution budgets."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--compiler", default="clang++")
    _ = parser.add_argument(
        "--depths", nargs="+", type=int, default=[2, 4, 8, 16, 30]
    )
    _ = parser.add_argument("--command-seconds", type=float, default=5.0)
    _ = parser.add_argument("--budget-seconds", type=float, default=60.0)
    args = parser.parse_args()
    if (
        any(not 1 <= depth <= _MAX_DEPTH for depth in args.depths)
        or not 0
        < args.command_seconds
        <= args.budget_seconds
        <= _MAX_BUDGET_SECONDS
    ):
        parser.error(
            message="depths: 1..48; budgets: 0 < command <= total <= 600"
        )
    return args


def main() -> None:
    """Measure inferred declarations and safe type hints under identical
    controls.
    """
    args = _arguments()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    compiler = shutil.which(cmd=str(object=args.compiler))
    if compiler is None:
        raise FileNotFoundError(str(object=args.compiler))
    deadline = monotonic() + args.budget_seconds
    version = subprocess.run(
        args=bounded_command(
            args=[compiler, "--version"],
            fixture="compiler version",
            timeout_seconds=min(5, args.budget_seconds),
        ),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    rows: list[dict[str, object]] = []
    failed = False
    for depth in args.depths:
        for kind in ("integer", "floating"):
            data = _shape(depth=depth, kind=kind)
            node_count = _nodes(value=data)
            if node_count > _MAX_NODES:
                msg = "generated input exceeds the explicit 128-node cap"
                raise ValueError(msg)
            for mode in ("inferred", "safe-hints"):
                remaining = deadline - monotonic()
                if remaining <= 0:
                    rows.append({"result": "budget-exhausted"})
                    failed = True
                    break
                case = output / f"{kind}-{depth}-{mode}"
                case.mkdir()
                source = json.dumps(obj=data)
                _ = (case / "input.json").write_text(
                    data=source, encoding="utf-8"
                )
                hints = (
                    Cpp.variable_type_hints_formats.NEVER
                    if mode == "inferred"
                    else Cpp.variable_type_hints_formats.SAFE
                )
                language = Cpp(variable_type_hints=hints)
                try:
                    result = literalize(
                        source=source,
                        input_format=InputFormat.JSON,
                        language=language,
                        variable_form=NewVariable(
                            name="my_data", modifiers=frozenset()
                        ),
                        wrap_in_file=True,
                    )
                except LiteralizerError as exc:
                    rows.append(
                        {
                            "shape": kind,
                            "depth": depth,
                            "mode": mode,
                            "result": "renderer-rejection",
                            "error": str(object=exc),
                        }
                    )
                    failed = True
                    continue
                _ = (case / "main.cpp").write_text(
                    data=result.code, encoding="utf-8"
                )
                command = [
                    compiler,
                    "-std=c++14",
                    "-fsyntax-only",
                    "-Werror",
                    "main.cpp",
                ]
                started = monotonic()
                completed = subprocess.run(
                    args=bounded_command(
                        args=command,
                        fixture=str(object=case),
                        timeout_seconds=min(args.command_seconds, remaining),
                    ),
                    cwd=case,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                _ = (case / "stdout.txt").write_text(
                    data=completed.stdout, encoding="utf-8"
                )
                _ = (case / "stderr.txt").write_text(
                    data=completed.stderr, encoding="utf-8"
                )
                outcome = (
                    "pass" if completed.returncode == 0 else "compiler-error"
                )
                if completed.returncode in {124, 137}:
                    outcome = "deadline-or-signal"
                failed |= outcome != "pass"
                rows.append(
                    {
                        "shape": kind,
                        "depth": depth,
                        "nodes": node_count,
                        "mode": mode,
                        "result": outcome,
                        "command": command,
                        "returncode": completed.returncode,
                        "seconds": monotonic() - started,
                    }
                )
    report = {
        "compiler_version": version,
        "budget_seconds": args.budget_seconds,
        "command_seconds": args.command_seconds,
        "observations": rows,
        "limits": "Type-checking cost only; acceptance does not prove values. "
        "No representation improvement is claimed by this probe.",
    }
    _ = (output / "report.json").write_text(
        data=json.dumps(obj=report, indent=2) + "\n", encoding="utf-8"
    )
    _ = sys.stdout.write(json.dumps(obj=report, indent=2) + "\n")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
