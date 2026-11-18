"""A resolved golden expectation governs execution and fixture writes."""

import functools
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, literalize_call
from literalizer.exceptions import CallArgNotSupportedError
from literalizer.languages import Bash
from tests.integration.golden_outcomes import SUCCESS, check_outcome


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


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_rejection_preserves_fixture_ownership(
    *, tmp_path: Path, regenerate: bool
) -> None:
    """Exercise the real verification and regeneration command lines."""
    test_path = tmp_path / "test_rejection.py"
    _ = test_path.write_text(
        data="""\
from pathlib import Path
import pytest
from literalizer.exceptions import CallArgNotSupportedError
from tests.integration.golden_outcomes import Rejection, check_outcome
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
        encoding="utf-8",
    )
    stale_path = tmp_path / "stale.sh"
    original = b"stale\n"
    _ = stale_path.write_bytes(data=original)
    config_path = tmp_path / "pytest.ini"
    _ = config_path.write_text(data="[pytest]\n", encoding="utf-8")
    project_root = Path(__file__).resolve().parents[3]
    completed = subprocess.run(  # noqa: S603 - exercise the real pytest CLI
        args=[
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--parallel-mode",
            "--rcfile",
            str(object=project_root / "pyproject.toml"),
            "-m",
            "pytest",
            "-c",
            str(object=config_path),
            "--disable-plugin-autoload",
            "-p",
            "pytest_regressions.plugin",
            "-p",
            "pytest_datadir.plugin",
            "-q",
            "--tb=short",
            str(object=test_path),
            *(["--regen-all"] if regenerate else []),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert completed.returncode == pytest.ExitCode.OK, (
        completed.stdout + completed.stderr
    )
    assert stale_path.read_bytes() == original
    assert not (tmp_path / "rejected.sh").exists()
