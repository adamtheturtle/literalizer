"""Golden-file tests for ``$ref`` marker support in
:func:`literalizer.literalize`.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .case_manifests import REF_OWNER
from .golden_checks import golden_test_parameters
from .literalize_ref_cases import (
    run_literalize_ref_golden_case,
)
from .reference_cases import (
    CASES_DIR,
    RefRendering,
    build_literalize_ref_variant_cases,
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
            for case in discover_literalize_ref_cases(
                owner=REF_OWNER, cases_dir=CASES_DIR
            )
        ),
    ),
)
def test_literalize_ref_golden_file(
    renderings: tuple[RefRendering, ...],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """``$ref`` markers render as bare identifiers across all
    languages.
    """
    for rendering in renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
            )


@pytest.mark.parametrize(
    argnames="renderings",
    argvalues=golden_test_parameters(
        cases=(
            (f"{case.config.coverage_id}/{case.variant.name}", case.renderings)
            for case in build_literalize_ref_variant_cases(cases_dir=CASES_DIR)
        ),
    ),
)
def test_literalize_ref_variant_golden_file(
    renderings: tuple[RefRendering, ...],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Render reference cases under the exact specs selected by each
    axis.
    """
    for rendering in renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
            )
