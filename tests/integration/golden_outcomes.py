"""Expectations resolved before exercising a golden rendering."""

import dataclasses
from collections.abc import Callable
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from .golden_checks import assert_no_golden, check_golden


@dataclasses.dataclass(frozen=True, kw_only=True)
class Success:
    """Run the renderer and compare the resulting text."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class Rejection:
    """Exercise a documented error at the public API boundary."""

    error: type[Exception]
    match: str | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exclusion:
    """The scenario intentionally omits this combination."""

    reason: str


type GoldenOutcome = Success | Rejection | Exclusion

SUCCESS: Success = Success()


@beartype
def assert_rejection(
    *,
    outcome: Rejection,
    render: Callable[[], object],
    golden_path: Path,
) -> None:
    """Exercise a rejection and prohibit a success fixture at its path."""
    assert_no_golden(golden_path=golden_path)
    with pytest.raises(expected_exception=outcome.error, match=outcome.match):
        _ = render()


@beartype
def check_outcome(
    *,
    outcome: GoldenOutcome,
    render: Callable[[], str],
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Run the expected outcome, allowing regeneration only on success."""
    match outcome:
        case Success():
            check_golden(
                contents=render(),
                golden_path=golden_path,
                file_regression=file_regression,
            )
        case Rejection():
            assert_rejection(
                outcome=outcome, render=render, golden_path=golden_path
            )
        case _:
            assert_no_golden(golden_path=golden_path)
            pytest.skip(reason=outcome.reason)
