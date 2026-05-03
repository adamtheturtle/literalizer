"""Golden-file tests for default ``$ref`` handling in ``literalize``."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer.languages import Python

from .language_specs import make_spec
from .literalize_ref_cases import (
    LiteralizeRefCase,
    discover_literalize_default_ref_cases,
    run_literalize_ref_golden_case,
)
from .variant_cases import Variant, build_language_version_variants

_PYTHON_DEFAULT_REF_WHOLE = next(
    case
    for case in discover_literalize_default_ref_cases()
    if case.config.case_dir_name == "literalize_ref_default_whole"
    and case.lang_cls is Python
)

_PYTHON_LANGUAGE_VERSION_VARIANTS = [
    variant
    for variant in build_language_version_variants()
    if variant.lang_cls is Python
]


@pytest.mark.parametrize(
    argnames="ref_case",
    argvalues=discover_literalize_default_ref_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in discover_literalize_default_ref_cases()
    ],
)
def test_literalize_ref_default_golden_file(
    ref_case: LiteralizeRefCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """``literalize`` renders ref markers without requiring
    ``ref_case``.
    """
    lang_cls = ref_case.lang_cls
    spec = make_spec(lang_cls=lang_cls)
    run_literalize_ref_golden_case(
        config=ref_case.config,
        lang_cls=lang_cls,
        spec=spec,
        golden_name=f"{lang_cls.__name__}_ref_default",
        cases_dir=cases_dir,
        file_regression=file_regression,
        ref_case=None,
    )


@pytest.mark.parametrize(
    argnames="variant",
    argvalues=_PYTHON_LANGUAGE_VERSION_VARIANTS,
    ids=[variant.name for variant in _PYTHON_LANGUAGE_VERSION_VARIANTS],
)
def test_literalize_ref_default_variant_golden_file(
    variant: Variant,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Default ``$ref`` cases also cover language-version variants."""
    run_literalize_ref_golden_case(
        config=_PYTHON_DEFAULT_REF_WHOLE.config,
        lang_cls=Python,
        spec=variant.spec,
        golden_name=variant.name,
        cases_dir=cases_dir,
        file_regression=file_regression,
        ref_case=None,
    )
