"""Default and variant calls share one native golden-file runner."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .call_cases import (
    run_call_golden_case,
)
from .call_collection import (
    CASES_DIR,
    CallRendering,
)
from .call_variant_cases import call_golden_cases
from .golden_checks import golden_test_parameters


@pytest.mark.parametrize(
    argnames="renderings",
    argvalues=golden_test_parameters(
        cases=(
            (case.test_id, case.renderings)
            for case in call_golden_cases(cases_dir=CASES_DIR)
        ),
    ),
)
def test_call_golden_file(
    renderings: tuple[CallRendering, ...],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every call rendering matches its fixture or declared rejection."""
    for rendering in renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_call_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
            )
