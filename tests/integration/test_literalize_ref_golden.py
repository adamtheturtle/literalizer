"""Golden-file tests for ``$ref`` marker support in
:func:`literalizer.literalize`.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .language_specs import make_spec
from .literalize_ref_cases import (
    LiteralizeRefCase,
    LiteralizeRefVariantCase,
    build_literalize_ref_variant_cases,
    discover_literalize_ref_cases,
    ref_language_versions,
    run_literalize_ref_golden_case,
)


@pytest.mark.parametrize(
    argnames="ref_case",
    argvalues=discover_literalize_ref_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.lang_cls.__name__}",
)
def test_literalize_ref_golden_file(
    ref_case: LiteralizeRefCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """``$ref`` markers render as bare identifiers across all
    languages.
    """
    lang_cls = ref_case.lang_cls
    for version_format in ref_language_versions(
        config=ref_case.config, lang_cls=lang_cls
    ):
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            effective_ref_case = ref_case.config.ref_case_for(
                lang_cls=lang_cls
            )
            if effective_ref_case is None:
                effective_ref_case = spec.identifier_cases[0]
            run_literalize_ref_golden_case(
                config=ref_case.config,
                lang_cls=lang_cls,
                spec=spec,
                golden_name=f"{lang_cls.__name__}_ref",
                cases_dir=cases_dir,
                file_regression=file_regression,
                ref_case=effective_ref_case,
                version=version_format,
            )


@pytest.mark.parametrize(
    argnames="ref_variant_case",
    argvalues=build_literalize_ref_variant_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.variant.name}",
)
def test_literalize_ref_variant_golden_file(
    ref_variant_case: LiteralizeRefVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Render reference cases under the exact specs selected by each
    axis.
    """
    lang_cls = ref_variant_case.variant.lang_cls
    spec = ref_variant_case.variant.spec
    config = ref_variant_case.config
    effective_ref_case = ref_variant_case.ref_case
    with subtests.test(version=spec.language_version.name):
        run_literalize_ref_golden_case(
            config=config,
            lang_cls=lang_cls,
            spec=spec,
            golden_name=ref_variant_case.golden_name,
            cases_dir=cases_dir,
            file_regression=file_regression,
            ref_case=effective_ref_case,
            version=spec.language_version,
        )
