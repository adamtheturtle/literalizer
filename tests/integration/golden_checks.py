"""Comparison and outcome assertions for golden fixtures."""

import enum
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Protocol

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import Language, LiteralizeResult

from .fixture_names import fixture_module_name
from .golden_outcomes import Exclusion, GoldenOutcome, Rejection, Success
from .language_metadata import language_metadata


class _OutcomeRendering(Protocol):
    """A rendering with a resolved outcome."""

    @property
    def outcome(self) -> GoldenOutcome:
        """Return the discovered outcome for this rendering."""
        ...


def golden_test_parameters(
    *, cases: Iterable[tuple[str, Iterable[_OutcomeRendering]]]
) -> list[pytest.ParameterSet]:
    """Schedule executable renderings under their case IDs."""
    parameters: list[pytest.ParameterSet] = []
    for case_id, renderings in cases:
        executable = tuple(
            rendering
            for rendering in renderings
            if not isinstance(rendering.outcome, Exclusion)
        )
        if len(executable) > 0:
            parameters.append(pytest.param(executable, id=case_id))
    return parameters


@beartype
def assert_no_golden(*, golden_path: Path) -> None:
    """Fail when an unsuccessful rendering still has a success fixture."""
    if golden_path.exists():
        pytest.fail(
            reason=f"Unexpected success fixture: {golden_path}",
        )


@beartype
def check_golden(
    *,
    contents: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Compare *contents* against the fixture at *golden_path*."""
    # newline="" prevents Python text-mode from converting \r\n to \n on
    # Windows, which would corrupt golden files containing literal CR
    # bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=contents,
        encoding="utf-8",
        extension=golden_path.suffix,
        newline="",
        fullpath=golden_path,
    )


@beartype
def format_consumer(
    *,
    template: str,
    result: LiteralizeResult,
    golden_path: Path,
    spec: Language,
) -> str:
    """Format a native consumer from the result and fixture path."""
    options: Mapping[str, object] = vars(spec)
    return template.format(
        **{
            name: value.name
            for name, value in options.items()
            if isinstance(value, enum.Enum)
        },
        preamble="\n".join(result.preamble),
        body_preamble="\n".join(result.body_preamble),
        code=result.code,
        bare_code=result.bare_code,
        module_name=fixture_module_name(golden_path=golden_path),
    )


@beartype
def fixture_contents(
    *, code: str, language_id: str, intentional_identifier: bool
) -> str:
    """Finish a fixture with its declared identifier preamble and
    newline.
    """
    preamble = (
        language_metadata(
            language_id=language_id
        ).golden.intentional_identifier_preamble
        if intentional_identifier
        else ()
    )
    return "\n".join((*preamble, code, ""))


@beartype
def assert_rejection(
    *,
    outcome: Rejection,
    render: Callable[[], object],
    golden_path: Path,
    exact_type: bool,
) -> None:
    """Exercise a rejection and prohibit a success fixture at its path."""
    assert_no_golden(golden_path=golden_path)
    with pytest.raises(
        expected_exception=outcome.error, match=outcome.match
    ) as raised:
        _ = render()
    if exact_type and raised.type is not outcome.error:
        pytest.fail(
            reason=(
                f"Expected {outcome.error.__name__}, "
                f"got {raised.type.__name__}: {raised.value}"
            ),
        )


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
                outcome=outcome,
                render=render,
                golden_path=golden_path,
                exact_type=outcome.exact_type,
            )
        case _:
            reason = outcome.reason
            pytest.fail(
                reason=f"Discovery exclusion reached execution: {reason}"
            )
