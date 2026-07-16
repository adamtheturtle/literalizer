"""Golden tests for normalized ``NewVariable`` identifiers."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_discovery import case_input
from .language_specs import (
    lang_cls_name,
    make_golden_path,
    make_spec,
    with_per_fixture_module_name,
)
from .new_variable_cases import cases_for_language, normalizing_languages


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=normalizing_languages(),
    ids=lang_cls_name,
)
def test_new_variable_name_golden_files(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Check complete wrapped files for every normalizing language."""
    case_dir = cases_dir / "new_variable_names"
    input_info = case_input(case_dir=case_dir)
    source_text = input_info.path.read_text(encoding="utf-8")
    for case in cases_for_language(lang_cls=lang_cls):
        for version_format in lang_cls.VersionFormats:
            with subtests.test(
                case=case.name,
                version=version_format.name,
            ):
                golden_path = make_golden_path(
                    parent=case_dir,
                    name=f"{case.name}_{lang_cls.__name__}",
                    extension=lang_cls.extension,
                    lang_cls=lang_cls,
                    version=version_format,
                )
                spec = with_per_fixture_module_name(
                    spec=make_spec(
                        lang_cls=lang_cls,
                        language_version=version_format,
                    ),
                    golden_path=golden_path,
                )
                result = literalizer.literalize(
                    source=source_text,
                    input_format=input_info.input_format,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=literalizer.NewVariable(
                        name=case.variable_name,
                        modifiers=frozenset(),
                    ),
                    wrap_in_file=True,
                )
                file_regression.check(
                    contents=result.code + "\n",
                    encoding="utf-8",
                    extension=lang_cls.extension,
                    newline="",
                    fullpath=golden_path,
                )
