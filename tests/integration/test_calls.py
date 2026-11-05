"""Default and variant calls share one native golden-file runner."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .call_cases import CASES_DIR, CallCase, run_call_golden_case
from .call_variant_cases import CallVariantCase, call_golden_cases


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=call_golden_cases(cases_dir=CASES_DIR),
    ids=lambda case: case.test_id,
)
def test_call_golden_file(
    call_case: CallCase | CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    pytestconfig: pytest.Config,
) -> None:
    """Every call rendering matches its fixture or declared rejection."""
    for rendering in call_case.renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_call_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
                pytest_config=pytestconfig,
            )
