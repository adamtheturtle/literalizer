"""Native golden-file coverage for constructor targets and bindings."""

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .constructor_cases import (
    CASES_DIR,
    ConstructorBindingCase,
    constructor_binding_cases,
)
from .constructor_goldens import run_constructor_binding_golden_case


@pytest.mark.parametrize(
    argnames="case",
    argvalues=constructor_binding_cases(cases_dir=CASES_DIR),
    ids=lambda case: f"{case.manifest.case_dir.name}/{case.name}",
)
def test_constructor_binding_golden_file(
    *,
    case: ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared constructor binding matches its native golden."""
    for rendering in case.renderings:
        with subtests.test(version=rendering.version.name):
            run_constructor_binding_golden_case(
                rendering=rendering,
                file_regression=file_regression,
            )
