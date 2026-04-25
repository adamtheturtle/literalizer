"""Golden-file tests where each input is rendered as a single
declaration form per file.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    UnrepresentableIntegerError,
)

from .case_discovery import (
    golden_file_languages,
    group_cases_by_language,
)
from .golden_assertions import check_golden
from .language_specs import lang_cls_name, make_spec
from .variable_form_wrapping import wrap_variable_form


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=golden_file_languages(),
    ids=lang_cls_name,
)
def test_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    lang_name = lang_cls.__name__
    for case_name in group_cases_by_language()[lang_cls]:
        with subtests.test(case_name=case_name):
            input_path = cases_dir / case_name / "input.yaml"
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (lang_name + lang_cls.extension)
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=make_spec(lang_cls=lang_cls),
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=wrap_variable_form(lang_cls=lang_cls),
                    wrap_in_file=True,
                )
            except UnrepresentableIntegerError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_name} cannot represent integer in this input",
                )
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_name} cannot represent this heterogeneous input",
                )
            # newline="" prevents Python text-mode from converting \r\n to
            # \n on Windows, which would corrupt golden files containing
            # literal CR bytes (e.g. CommonLisp string_control_chars).
            check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=lang_cls.extension,
                newline="",
                golden_path=golden_path,
            )
