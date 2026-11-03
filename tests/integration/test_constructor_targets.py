"""Golden-file coverage for constructor call targets.

Complete constructor bindings check the target spelling alongside call
styles and variable modifiers. Languages without a compiling binding
retain a fragment snapshot of the target helper.
"""

import enum
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .constructor_cases import (
    CASES_DIR,
    ConstructorBindingCase,
    constructor_binding_cases,
    constructor_golden_path,
)
from .constructor_goldens import run_constructor_binding_golden_case
from .golden_checks import check_golden
from .language_specs import (
    make_golden_path,
    make_spec,
    sorted_languages,
)

_CONSTRUCTOR_NAME = "Playlist"
_GOLDEN_DIR = Path(__file__).parent / "constructor_targets"
_COMPILING_CONSTRUCTOR_LANGUAGES = {
    case.lang_cls
    for case in constructor_binding_cases(cases_dir=CASES_DIR)
    if case.manifest is not None
}


@beartype
def _golden_path(
    *,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> Path:
    """Return the checked-in golden path for a constructor-target case."""
    return make_golden_path(
        parent=_GOLDEN_DIR,
        name=name,
        extension=".txt",
        lang_cls=lang_cls,
        version=version,
    )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=[
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls not in _COMPILING_CONSTRUCTOR_LANGUAGES
    ],
    ids=lambda lang_cls: lang_cls.__name__,
)
def test_constructor_targets_golden_file(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Retain helper snapshots without compiling constructor bindings."""
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            check_golden(
                contents=(
                    spec.format_constructor_target(_CONSTRUCTOR_NAME) + "\n"
                ),
                extension=".txt",
                golden_path=_golden_path(
                    name=f"{lang_cls.__name__}_constructor_target",
                    lang_cls=lang_cls,
                    version=version_format,
                ),
                file_regression=file_regression,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=constructor_binding_cases(cases_dir=CASES_DIR),
    ids=lambda case: (
        case.name
        if case.manifest is None
        else f"{case.manifest.case_dir.name}/{case.name}"
    ),
)
def test_constructor_binding_golden_file(
    *,
    case: ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared constructor binding matches its golden file."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = constructor_golden_path(
                case=case,
                version=version_format,
                fragments_dir=_GOLDEN_DIR,
            )
            run_constructor_binding_golden_case(
                case=case,
                version=version_format,
                golden_path=golden_path,
                file_regression=file_regression,
            )
