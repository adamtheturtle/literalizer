"""Golden-file tests for ``$ref`` marker support in
:func:`literalizer.literalize`.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .case_manifests import REF_OWNER
from .literalize_ref_cases import (
    run_literalize_ref_golden_case,
)
from .reference_cases import (
    LiteralizeRefCase,
    LiteralizeRefVariantCase,
    build_literalize_ref_variant_cases,
    discover_literalize_ref_cases,
)


@pytest.mark.parametrize(
    argnames="ref_case",
    argvalues=discover_literalize_ref_cases(owner=REF_OWNER),
    ids=lambda case: f"{case.config.coverage_id}/{case.lang_cls.__name__}",
)
def test_literalize_ref_golden_file(
    ref_case: LiteralizeRefCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    pytestconfig: pytest.Config,
) -> None:
    """``$ref`` markers render as bare identifiers across all
    languages.
    """
    for rendering in ref_case.renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
                pytest_config=pytestconfig,
            )


@pytest.mark.parametrize(
    argnames="ref_variant_case",
    argvalues=build_literalize_ref_variant_cases(),
    ids=lambda case: f"{case.config.coverage_id}/{case.variant.name}",
)
def test_literalize_ref_variant_golden_file(
    ref_variant_case: LiteralizeRefVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    pytestconfig: pytest.Config,
) -> None:
    """Render reference cases under the exact specs selected by each
    axis.
    """
    for rendering in ref_variant_case.renderings:
        with subtests.test(version=rendering.spec.language_version.name):
            run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=cases_dir,
                file_regression=file_regression,
                pytest_config=pytestconfig,
            )
