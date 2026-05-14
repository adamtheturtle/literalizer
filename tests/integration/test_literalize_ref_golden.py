"""Golden-file tests for ``$ref`` marker support in
:func:`literalizer.literalize`.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .language_specs import make_spec
from .literalize_ref_cases import (
    LiteralizeRefCase,
    discover_literalize_ref_cases,
    run_literalize_ref_golden_case,
)


@pytest.mark.parametrize(
    argnames="ref_case",
    argvalues=discover_literalize_ref_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in discover_literalize_ref_cases()
    ],
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
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            run_literalize_ref_golden_case(
                config=ref_case.config,
                lang_cls=lang_cls,
                spec=spec,
                golden_name=f"{lang_cls.__name__}_ref",
                cases_dir=cases_dir,
                file_regression=file_regression,
                ref_case=spec.identifier_cases[0],
                version=version_format,
            )
