"""Probe bounded Python sibling, binding and reference invariants (#5491).

Use ``python -m scripts.discover_rendering_invariants --output /tmp/probe``
Each program executes in a fresh bounded subprocess. The fixed JSON corpus
isolates ordering and naming from random value selection. Artifacts include
the source, reference context, expected value, program and subprocess logs.
"""

import argparse
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from time import monotonic

from pydantic import JsonValue, TypeAdapter

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python
from scripts.bounded_command import bounded_command


@dataclass(frozen=True)
class Probe:
    """One transformation with its independently specified value
    relation.
    """

    name: str
    source: JsonValue
    expected: JsonValue
    references: dict[str, JsonValue]
    binding: str


_MAX_BUDGET_SECONDS = 600


def probes() -> list[Probe]:
    """Keep empty/null siblings, permutations and reference renames
    separate.
    """
    seeds: list[list[JsonValue]] = [
        [[], [1, 2]],
        [[None, None], [1, 2]],
        [{"items": []}, {"items": [1, 2]}],
        [{"value": 1}, {"value": "text"}],
        [[1], ["text"]],
        [{}, {"value": 1}],
    ]
    result: list[Probe] = []
    for index, seed in enumerate(iterable=seeds):
        for reverse in (False, True):
            data = list(reversed(seed)) if reverse else list(seed)
            result.extend(
                Probe(
                    name=f"siblings-{index}-{reverse}-{binding}",
                    source=data,
                    expected=data,
                    references={},
                    binding=binding,
                )
                for binding in ("result_data", "renamed_result")
            )
    result.extend(
        Probe(
            name=f"reused-reference-{name}",
            source=[{"$ref": name}, {"nested": {"$ref": name}}],
            expected=[[1, 2], {"nested": [1, 2]}],
            references={name: [1, 2]},
            binding="result_data",
        )
        for name in ("payload", "renamed_payload")
    )
    return result


def _same(*, expected: JsonValue, actual: JsonValue) -> bool:
    """Compare JSON values without equating booleans and numbers."""
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


def main() -> None:
    """Run every fixed relation within an explicit overall time budget."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--budget-seconds", type=int, default=60)
    args = parser.parse_args()
    if not 1 <= args.budget_seconds <= _MAX_BUDGET_SECONDS:
        parser.error(message="budget must be 1..600 seconds")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    deadline = monotonic() + args.budget_seconds
    observations: list[dict[str, object]] = []
    failed = False
    for index, probe in enumerate(iterable=probes()):
        remaining = deadline - monotonic()
        if remaining <= 0:
            observations.append({"result": "budget-exhausted"})
            failed = True
            break
        case = output / f"{index:03d}"
        case.mkdir()
        context = {
            "source": probe.source,
            "expected": probe.expected,
            "bound_refs": probe.references,
            "binding": probe.binding,
        }
        _ = (case / "context.json").write_text(
            data=json.dumps(obj=context, indent=2) + "\n", encoding="utf-8"
        )
        result = literalize(
            source=json.dumps(obj=probe.source),
            input_format=InputFormat.JSON,
            language=Python(
                sequence_format=Python.sequence_formats.LIST,
                variable_type_hints=Python.variable_type_hints_formats.NEVER,
            ),
            variable_form=NewVariable(
                name=probe.binding, modifiers=frozenset()
            ),
            ref_key="$ref",
            bound_refs=probe.references,
            wrap_in_file=True,
        )
        program = (
            result.code
            + "\nimport json\nimport sys\n"
            + f"sys.stdout.write(json.dumps({probe.binding}))\n"
        )
        _ = (case / "main.py").write_text(data=program, encoding="utf-8")
        command = [sys.executable, "-I", "main.py"]
        completed = subprocess.run(
            args=bounded_command(
                args=command,
                fixture=probe.name,
                timeout_seconds=min(5, remaining),
            ),
            cwd=case,
            capture_output=True,
            text=True,
            check=False,
        )
        _ = (case / "stdout.txt").write_text(
            data=completed.stdout, encoding="utf-8"
        )
        _ = (case / "stderr.txt").write_text(
            data=completed.stderr, encoding="utf-8"
        )
        outcome = "runtime-failure"
        if completed.returncode == 0:
            actual = TypeAdapter(type=JsonValue).validate_json(
                completed.stdout
            )
            outcome = (
                "pass"
                if _same(expected=probe.expected, actual=actual)
                else "value-mismatch"
            )
        elif completed.returncode in {124, 137}:
            outcome = "command-timeout"
        failed |= outcome != "pass"
        observations.append(
            {"probe": probe.name, "result": outcome, "command": command}
        )
    report = {
        "python": platform.python_version(),
        "budget_seconds": args.budget_seconds,
        "scope": (
            "Python list representation, default heterogeneous "
            "strategy, no type hints"
        ),
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
