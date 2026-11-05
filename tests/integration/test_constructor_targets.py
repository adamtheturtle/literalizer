"""Native golden-file coverage for constructor targets and bindings."""

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .constructor_cases import (
    CASES_DIR,
    ConstructorBindingCase,
    constructor_binding_cases,
    constructor_golden_path,
)
from .constructor_goldens import run_constructor_binding_golden_case
from .source_profiles import source_format_marks


@pytest.mark.parametrize(
    argnames="case",
    argvalues=[
        pytest.param(case, marks=source_format_marks(lang_cls=case.lang_cls))
        for case in constructor_binding_cases(cases_dir=CASES_DIR)
    ],
    ids=lambda case: f"{case.manifest.case_dir.name}/{case.name}",
)
def test_constructor_binding_golden_file(
    *,
    case: ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared constructor binding matches its native golden."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = constructor_golden_path(
                case=case,
                version=version_format,
            )
            run_constructor_binding_golden_case(
                case=case,
                version=version_format,
                golden_path=golden_path,
                file_regression=file_regression,
            )
