"""A resolved golden expectation governs execution and fixture writes."""

import functools
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, literalize_call
from literalizer.exceptions import (
    CallArgNotSupportedError,
    ExistingVariableNotSelfContainedError,
)
from literalizer.languages import Bash
from tests.integration.golden_checks import check_outcome
from tests.integration.golden_outcomes import SUCCESS, Exclusion, Rejection

pytest_plugins: tuple[str, ...] = ("pytester",)


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


def test_rejection_propagates_the_wrong_error(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A collection argument error cannot satisfy a binding rejection."""
    golden_path = tmp_path / "call.sh"
    with pytest.raises(
        expected_exception=CallArgNotSupportedError, match="list values"
    ):
        check_outcome(
            outcome=Rejection(
                error=ExistingVariableNotSelfContainedError,
                match="the assignment has no prior declaration",
            ),
            render=functools.partial(_bash_call, source="[]"),
            golden_path=golden_path,
            file_regression=file_regression,
        )
    assert not golden_path.exists()


def test_exclusion_reaching_execution_fails(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A fixture prerequisite belongs in discovery."""
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="Discovery exclusion reached execution: missing call syntax",
    ):
        check_outcome(
            outcome=Exclusion(reason="missing call syntax"),
            render=functools.partial(_bash_call, source="[]"),
            golden_path=tmp_path / "call.sh",
            file_regression=file_regression,
        )


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_rejection_preserves_fixture_ownership(
    *, pytester: pytest.Pytester, regenerate: bool
) -> None:
    """Exercise the real verification and regeneration command lines."""
    _ = pytester.makepyfile(
        """\
from pathlib import Path
import pytest
from literalizer.exceptions import CallArgNotSupportedError
from tests.integration.golden_checks import check_outcome
from tests.integration.golden_outcomes import Rejection
from tests.integration.harness.test_golden_outcomes import _bash_call


def test_rejection(file_regression):
    golden_path = Path(__file__).with_name("rejected.sh")
    outcome = Rejection(error=CallArgNotSupportedError, match="list values")
    with pytest.raises(pytest.fail.Exception, match="DID NOT RAISE"):
        check_outcome(
            outcome=outcome,
            render=lambda: _bash_call(source="3"),
            golden_path=golden_path,
            file_regression=file_regression,
        )

    with pytest.raises(
        pytest.fail.Exception, match="Unexpected success fixture"
    ):
        check_outcome(
            outcome=outcome,
            render=lambda: _bash_call(source="[]"),
            golden_path=Path(__file__).with_name("stale.sh"),
            file_regression=file_regression,
        )
""",
    )
    stale_path = pytester.path / "stale.sh"
    original = b"stale\n"
    _ = stale_path.write_bytes(data=original)
    _ = pytester.makeini(source="[pytest]")
    pytester.syspathinsert(path=Path(__file__).resolve().parents[3])
    result = pytester.runpytest_inprocess(
        "--disable-plugin-autoload",
        "-p",
        "pytest_regressions.plugin",
        "-p",
        "pytest_datadir.plugin",
        "-q",
        *(["--regen-all"] if regenerate else []),
    )
    result.assert_outcomes(passed=1)
    assert stale_path.read_bytes() == original
    assert not (pytester.path / "rejected.sh").exists()
