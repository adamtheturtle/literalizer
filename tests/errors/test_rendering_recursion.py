"""Recursion exhaustion retains typed errors without fixing a depth
limit.
"""

import ast
import subprocess
import sys
from pathlib import Path

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    JSON5ParseError,
    JSONCParseError,
    JSONParseError,
    ParseError,
    YAMLParseError,
)
from literalizer.languages import Python

_ERRORS: dict[InputFormat, type[ParseError]] = {
    InputFormat.JSON: JSONParseError,
    InputFormat.JSONC: JSONCParseError,
    InputFormat.JSON5: JSON5ParseError,
    InputFormat.YAML: YAMLParseError,
}
_DEPTH = 180


def _check_recursion_error(
    *, input_format: InputFormat, error: ParseError
) -> None:
    """Check the format-specific error and its original recursion
    cause.
    """
    assert isinstance(error, _ERRORS[input_format])
    assert "input exceeds the supported nesting depth" in str(object=error)
    assert isinstance(error.__cause__, RecursionError)


def _check_rendering(
    *, input_format: InputFormat, recursion_budget: int
) -> None:
    """Accept correct rendering or a typed refusal under a known
    budget.
    """
    source = "[" * _DEPTH + "0" + "]" * _DEPTH
    sys.setrecursionlimit(recursion_budget)
    try:
        result = literalize(
            source=source, input_format=input_format, language=Python()
        )
    except ParseError as caught:
        _check_recursion_error(input_format=input_format, error=caught)
        return

    # Validation should not consume the constrained rendering budget.
    sys.setrecursionlimit(5_000)
    node = ast.parse(source=result.code, mode="eval").body
    for _ in range(_DEPTH):
        assert isinstance(node, (ast.List, ast.Tuple))
        assert len(node.elts) == 1
        (node,) = node.elts
    assert isinstance(node, ast.Constant)
    assert node.value == 0


@pytest.mark.parametrize(argnames="recursion_budget", argvalues=[1_000, 5_000])
def test_rendering_recursion_outcome(recursion_budget: int) -> None:
    """Exhaustion stays typed; deeper supported rendering remains
    valid.
    """
    project_root = Path(__file__).resolve().parents[2]
    completed = subprocess.run(  # noqa: S603 - run this repository's isolated recursion probe
        args=[
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--parallel-mode",
            "--rcfile",
            str(object=project_root / "pyproject.toml"),
            "-m",
            "tests.errors.test_rendering_recursion",
            str(object=recursion_budget),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stdout == "checked\n"


if __name__ == "__main__":
    for _format in _ERRORS:
        _check_rendering(
            input_format=_format,
            recursion_budget=int(sys.argv[1]),
        )
    _ = sys.stdout.write("checked\n")
