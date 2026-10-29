"""Run a small seeded JSON discovery pilot outside ordinary PR CI (#5493).

Use ``python -m scripts.discover_generated_roundtrips --output /tmp/pilot``
The retained base corpus is extended, never replaced. Node, Go and Ruby
reuse existing corpora, literalization helpers and representation exclusions.
Every input, source, command and result is retained for reproduction.
"""

import argparse
import json
import platform
import random
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from time import monotonic

from pydantic import JsonValue

from literalizer import RoundTripCapability
from literalizer.languages import Go, JavaScript, Ruby
from scripts import roundtrip_common
from scripts.bounded_command import bounded_command


@dataclass(frozen=True)
class Backend:
    """An explicit pilot adapter, not a golden participation selector."""

    name: str
    executable: str
    version_args: tuple[str, ...]
    filename: str
    run_args: tuple[str, ...]
    excluded: tuple[str, ...]
    build: Callable[[str], str]
    capabilities: frozenset[RoundTripCapability]


def _javascript_program(source: str) -> str:
    """Host the public literal result in a small Node JSON consumer."""
    result = roundtrip_common.literalize_new_variable(
        language=JavaScript(),
        json_text=source,
        var_name="myData",
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n{result.code}\n"
        "process.stdout.write(JSON.stringify(myData));\n"
    )


def _go_program(source: str) -> str:
    """Compile the public literal against Go's standard JSON consumer."""
    result = roundtrip_common.literalize_new_variable(
        language=Go(),
        json_text=source,
        var_name="myData",
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        'import ("encoding/json"; "fmt")\n'
        "func main() {\n"
        f"{result.code}\n"
        "out, err := json.Marshal(myData)\n"
        "if err != nil { panic(err) }\n"
        "fmt.Print(string(out))\n}\n"
    )


def _ruby_program(source: str) -> str:
    """Host the public literal with Ruby's standard JSON consumer."""
    result = roundtrip_common.literalize_new_variable(
        language=Ruby(),
        json_text=source,
        var_name="myData",
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "require 'json'\n" + f"{preamble}\n{result.code}\n"
        "STDOUT.write(JSON.generate(myData))\n"
    )


_BACKENDS = (
    Backend(
        name="JavaScript",
        executable="node",
        version_args=("--version",),
        filename="main.js",
        run_args=("main.js",),
        excluded=("biginteger",),
        build=_javascript_program,
        capabilities=JavaScript.variant_metadata.round_trip_capabilities,
    ),
    Backend(
        name="Go",
        executable="go",
        version_args=("version",),
        filename="main.go",
        run_args=("run", "main.go"),
        excluded=("biginteger",),
        build=_go_program,
        capabilities=Go.variant_metadata.round_trip_capabilities,
    ),
    Backend(
        name="Ruby",
        executable="ruby",
        version_args=("--version",),
        filename="main.rb",
        run_args=("main.rb",),
        excluded=(),
        build=_ruby_program,
        capabilities=Ruby.variant_metadata.round_trip_capabilities,
    ),
)

_MAX_BUDGET_SECONDS = 600
_MAX_EXAMPLES = 64


def _value(*, rng: random.Random, depth: int) -> JsonValue:
    """Generate at most forty nodes with small safe JSON numeric
    ranges.
    """
    kinds = ("integer", "float", "boolean", "string", "list", "mapping")
    kind = rng.choice(seq=kinds if depth > 0 else kinds[:4])
    if kind == "integer":
        return rng.randrange(start=-1000000, stop=1000001)
    if kind == "float":
        return rng.randrange(start=-1000, stop=1001) + 0.25
    if kind == "boolean":
        return bool(rng.randrange(start=0, stop=2))
    if kind == "string":
        return "".join(
            rng.choice(seq='abé中\n\t"\\')
            for _ in range(rng.randrange(start=0, stop=13))
        )
    if kind == "list":
        return [
            _value(rng=rng, depth=depth - 1)
            for _ in range(rng.randrange(start=0, stop=4))
        ]
    return {
        f"key_{i}": _value(rng=rng, depth=depth - 1)
        for i in range(rng.randrange(start=0, stop=4))
    }


def _same(*, expected: JsonValue, actual: JsonValue) -> bool:
    """Keep booleans distinct from numbers while allowing JSON numeric
    coercion.
    """
    if isinstance(expected, bool) or isinstance(actual, bool):
        return type(expected) is type(actual) and expected == actual
    if isinstance(expected, dict) and isinstance(actual, dict):
        return expected.keys() == actual.keys() and all(
            _same(expected=value, actual=actual[key])
            for key, value in expected.items()
        )
    if isinstance(expected, list) and isinstance(actual, list):
        return len(expected) == len(actual) and all(
            _same(expected=left, actual=right)
            for left, right in zip(expected, actual, strict=True)
        )
    return expected == actual


def _write_program(*, case: Path, backend: Backend, source: str) -> None:
    """Retain the exact source and build context before executing anything."""
    _ = (case / "input.json").write_text(data=source, encoding="utf-8")
    program = backend.build(source)
    _ = (case / backend.filename).write_text(data=program, encoding="utf-8")
    _ = (case / "go.mod").write_text(
        data="module discovery\n\ngo 1.18\n", encoding="utf-8"
    )


def _arguments() -> argparse.Namespace:
    """Validate finite input and execution budgets."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--seed", type=int, default=5493)
    _ = parser.add_argument("--examples", type=int, default=8)
    _ = parser.add_argument("--budget-seconds", type=int, default=120)
    _ = parser.add_argument("--command-seconds", type=int, default=15)
    args = parser.parse_args()
    if (
        not 1 <= args.examples <= _MAX_EXAMPLES
        or not 1
        <= args.command_seconds
        <= args.budget_seconds
        <= _MAX_BUDGET_SECONDS
    ):
        parser.error(
            message="examples: 1..64; budgets: 1 <= command <= total <= 600"
        )
    return args


def main() -> None:
    """Persist reproducible observations within explicit process and run
    budgets.
    """
    args = _arguments()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    rng = random.Random(x=args.seed)  # noqa: S311 - reproducible discovery, not cryptography
    generated = [_value(rng=rng, depth=3) for _ in range(args.examples)]
    deadline = monotonic() + args.budget_seconds
    observations: list[dict[str, object]] = []
    failed = False
    for backend in _BACKENDS:
        executable = shutil.which(cmd=backend.executable)
        if executable is None:
            observations.append(
                {"backend": backend.name, "result": "missing-tool"}
            )
            failed = True
            continue
        version = subprocess.run(
            args=bounded_command(
                args=[executable, *backend.version_args],
                fixture=f"{backend.name} version",
                timeout_seconds=5,
            ),
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        for index in range(args.examples):
            remaining = deadline - monotonic()
            if remaining <= 0:
                observations.append(
                    {"backend": backend.name, "result": "budget-exhausted"}
                )
                failed = True
                break
            case = output / f"{backend.name.lower()}-{index:03d}"
            case.mkdir()
            document = roundtrip_common.json_object_from_text(
                text=roundtrip_common.input_for_capabilities(
                    capabilities=backend.capabilities
                )
            )
            document["generated"] = generated[index]
            source = roundtrip_common.trim_keys(
                json_text=json.dumps(obj=document, ensure_ascii=False),
                excluded_keys=backend.excluded,
            )
            _write_program(case=case, backend=backend, source=source)
            command = [executable, *backend.run_args]
            started = monotonic()
            result = subprocess.run(
                args=bounded_command(
                    args=command,
                    fixture=str(object=case),
                    timeout_seconds=min(args.command_seconds, remaining),
                ),
                cwd=case,
                capture_output=True,
                text=True,
                check=False,
            )
            _ = (case / "stdout.txt").write_text(
                data=result.stdout, encoding="utf-8"
            )
            _ = (case / "stderr.txt").write_text(
                data=result.stderr, encoding="utf-8"
            )
            outcome = "compile-or-runtime-failure"
            if result.returncode == 0:
                try:
                    actual = roundtrip_common.json_object_from_text(
                        text=result.stdout
                    )
                    want = roundtrip_common.json_object_from_text(text=source)
                    outcome = (
                        "pass"
                        if _same(expected=want, actual=actual)
                        else "value-mismatch"
                    )
                except ValueError:
                    outcome = "invalid-json"
            elif result.returncode in {124, 137}:
                outcome = "command-timeout"
            failed |= outcome != "pass"
            observations.append(
                {
                    "backend": backend.name,
                    "example": index,
                    "tool_version": version,
                    "command": command,
                    "seconds": monotonic() - started,
                    "result": outcome,
                    "excluded_keys": backend.excluded,
                }
            )
    report = {
        "seed": args.seed,
        "python": platform.python_version(),
        "examples_per_backend": args.examples,
        "limits": "JSON transport alone does not establish a zero sign.",
        "budget_seconds": args.budget_seconds,
        "observations": observations,
    }
    _ = (output / "report.json").write_text(
        data=json.dumps(obj=report, indent=2) + "\n", encoding="utf-8"
    )
    _ = sys.stdout.write(json.dumps(obj=report, indent=2) + "\n")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
