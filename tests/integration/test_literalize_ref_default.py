"""Golden-file tests for default ``$ref`` handling in ``literalize``."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .case_manifests import REF_DEFAULT_OWNER
from .golden_checks import golden_test_parameters
from .literalize_ref_cases import (
    run_literalize_ref_golden_case,
)
from .reference_cases import (
    RefRendering,
    discover_literalize_ref_cases,
)


@pytest.mark.parametrize(
    argnames="renderings",
    argvalues=golden_test_parameters(
        cases=(
            (
                f"{case.config.coverage_id}/{case.lang_cls.__name__}",
                case.renderings,
            )
            for case in discover_literalize_ref_cases(owner=REF_DEFAULT_OWNER)
        ),
    ),
)
def test_literalize_ref_default_golden_file(
    renderings: tuple[RefRendering, ...],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """``literalize`` renders ref markers without requiring
    ``ref_case``.
    """
    for rendering in renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
            )
