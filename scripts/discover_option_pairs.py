"""Exercise a bounded, reproducible Python option-pair pilot (#5490).

Run ``python -m scripts.discover_option_pairs --output /tmp/pairs``.
Scope: both sequence formats, all type-hint policies, both annotation
policies and both layouts at the default supported Python version. A
deterministic greedy cover includes every pair in that declared scope.
This manual discovery tool does not expand the ordinary golden matrix.
"""

import argparse
import itertools
import json
import platform
import subprocess
import sys
from pathlib import Path
from time import monotonic

from pydantic import JsonValue, TypeAdapter

from literalizer import CollectionLayout, InputFormat, NewVariable, literalize
from literalizer.languages import Python
from scripts.bounded_command import bounded_command

type Configuration = tuple[str, str, str, str]
type Pair = tuple[int, str, int, str]

_SOURCE = (
    '{"rows":[{"name":"a","values":[1,2]},'
    '{"name":"b","values":[]}],"flags":[true,false]}'
)

_MAX_BUDGET_SECONDS = 600


def pairs(*, configuration: Configuration) -> set[Pair]:
    """Identify a pair by factor positions as well as selected values."""
    return {
        (left, configuration[left], right, configuration[right])
        for left, right in itertools.combinations(iterable=range(4), r=2)
    }


def covering_sample() -> tuple[list[Configuration], set[Pair]]:
    """Cover every pair without enumerating a permanent Cartesian test
    matrix.
    """
    candidates = list(
        itertools.product(
            tuple(Python.sequence_formats.__members__),
            tuple(Python.variable_type_hints_formats.__members__),
            tuple(Python.annotation_evaluations.__members__),
            ("COMPACT", "MULTILINE"),
        )
    )
    remaining = set[Pair]().union(
        *(pairs(configuration=c) for c in candidates)
    )
    required = set(remaining)
    chosen: list[Configuration] = []
    while len(remaining) > 0:
        selected = max(
            candidates, key=lambda c: len(pairs(configuration=c) & remaining)
        )
        chosen.append(selected)
        remaining -= pairs(configuration=selected)
        candidates.remove(selected)
    return chosen, required


def main() -> None:
    """Compile and compare each covered configuration within a fixed
    budget.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--budget-seconds", type=int, default=60)
    args = parser.parse_args()
    if not 1 <= args.budget_seconds <= _MAX_BUDGET_SECONDS:
        parser.error(message="budget must be 1..600 seconds")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    configurations, required = covering_sample()
    deadline = monotonic() + args.budget_seconds
    observed: set[Pair] = set()
    rows: list[dict[str, object]] = []
    failed = False
    expected = TypeAdapter(type=JsonValue).validate_json(_SOURCE)
    for index, config in enumerate(iterable=configurations):
        remaining = deadline - monotonic()
        if remaining <= 0:
            rows.append({"result": "budget-exhausted"})
            failed = True
            break
        sequence, hints, annotations, layout = config
        language = Python(
            sequence_format=Python.sequence_formats[sequence],
            variable_type_hints=Python.variable_type_hints_formats[hints],
            annotation_evaluation=Python.annotation_evaluations[annotations],
        )
        result = literalize(
            source=_SOURCE,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(
                name="result_data", modifiers=frozenset()
            ),
            collection_layout=CollectionLayout[layout],
            wrap_in_file=True,
        )
        sequence_type = "tuple" if sequence == "TUPLE" else "list"
        program = (
            result.code
            + "\nimport json\nimport sys\n"
            + f"if type(result_data['rows']) is not {sequence_type}:\n"
            + "    raise AssertionError('sequence representation changed')\n"
            + "if any(type(flag) is not bool "
            "for flag in result_data['flags']):\n"
            + "    raise AssertionError('boolean representation changed')\n"
            + "sys.stdout.write(json.dumps(result_data))\n"
        )
        case = output / f"{index:03d}"
        case.mkdir()
        _ = (case / "main.py").write_text(data=program, encoding="utf-8")
        _ = (case / "input.json").write_text(data=_SOURCE, encoding="utf-8")
        command = [sys.executable, "-I", "main.py"]
        completed = subprocess.run(
            args=bounded_command(
                args=command,
                fixture=str(object=config),
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
            outcome = "pass" if actual == expected else "value-mismatch"
        elif completed.returncode in {124, 137}:
            outcome = "command-timeout"
        if outcome == "pass":
            observed.update(pairs(configuration=config))
        failed |= outcome != "pass"
        rows.append(
            {"configuration": config, "result": outcome, "command": command}
        )
    report = {
        "python": platform.python_version(),
        "configurations": rows,
        "required_pairs": sorted(required),
        "unverified_pairs": sorted(required - observed),
        "limits": (
            "This is a four-factor Python pilot, "
            "not all supported options or languages."
        ),
    }
    _ = (output / "report.json").write_text(
        data=json.dumps(obj=report, indent=2) + "\n", encoding="utf-8"
    )
    _ = sys.stdout.write(json.dumps(obj=report, indent=2) + "\n")
    if failed or len(required - observed) > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
