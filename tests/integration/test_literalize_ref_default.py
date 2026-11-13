"""Golden-file tests for default ``$ref`` handling in ``literalize``."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .case_manifests import REF_DEFAULT_OWNER
from .literalize_ref_cases import (
    run_literalize_ref_golden_case,
)
from .reference_cases import (
    LiteralizeRefCase,
    discover_literalize_ref_cases,
)


@pytest.mark.parametrize(
    argnames="ref_case",
    argvalues=discover_literalize_ref_cases(owner=REF_DEFAULT_OWNER),
    ids=lambda case: f"{case.config.coverage_id}/{case.lang_cls.__name__}",
)
def test_literalize_ref_default_golden_file(
    ref_case: LiteralizeRefCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    pytestconfig: pytest.Config,
) -> None:
    """``literalize`` renders ref markers without requiring
    ``ref_case``.
    """
    for rendering in ref_case.renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
                pytest_config=pytestconfig,
            )
