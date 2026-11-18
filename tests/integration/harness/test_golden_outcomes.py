"""A resolved golden expectation governs execution and fixture writes."""

import functools
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, literalize_call
from literalizer.exceptions import CallArgNotSupportedError
from literalizer.languages import Bash
from tests.integration.golden_outcomes import SUCCESS, Rejection, check_outcome


def _bash_call(*, source: str) -> str:
    """Render a native call carrying one JSON value."""
    return literalize_call(
        source=source,
        input_format=InputFormat.JSON,
        language=Bash(),
        target_function="emit",
        parameter_names=("value",),
        per_element=False,
    ).code


def test_success_propagates_a_previous_skip_error(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A selected successful call fails if Bash rejects its value."""
    golden_path = tmp_path / "call.sh"
    with pytest.raises(
        expected_exception=CallArgNotSupportedError, match="list values"
    ):
        check_outcome(
            outcome=SUCCESS,
            render=functools.partial(_bash_call, source="[]"),
            golden_path=golden_path,
            file_regression=file_regression,
        )
    assert not golden_path.exists()


def test_unexpected_success_cannot_regenerate_a_rejection(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Successful rendering cannot turn a rejection into a native
    fixture.
    """
    monkeypatch.setattr(
        target=file_regression.request.config.option,
        name="regen_all",
        value=True,
    )
    golden_path = tmp_path / "call.sh"
    with pytest.raises(
        expected_exception=pytest.fail.Exception, match="DID NOT RAISE"
    ):
        check_outcome(
            outcome=Rejection(
                error=CallArgNotSupportedError, match="list values"
            ),
            render=functools.partial(_bash_call, source="3"),
            golden_path=golden_path,
            file_regression=file_regression,
        )
    assert not golden_path.exists()
