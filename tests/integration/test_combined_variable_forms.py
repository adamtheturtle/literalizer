"""Golden-file tests that combine declaration and assignment forms in
one output file.
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
    combined_languages,
    group_combined_cases_by_language,
)
from .golden_assertions import check_golden
from .language_specs import lang_cls_name, make_spec


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=combined_languages(),
    ids=lang_cls_name,
)
def test_golden_file_combined_variable_forms(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize with BothVariableForms produces expected
    golden output combining declaration and assignment in one file.
    """
    for combined_case in group_combined_cases_by_language()[lang_cls]:
        with subtests.test(
            case_name=combined_case.case_name,
            golden_file_name=combined_case.golden_file_name,
        ):
            input_path = cases_dir / combined_case.case_name / "input.yaml"
            spec = make_spec(
                lang_cls=lang_cls,
                declaration_style=combined_case.declaration_style,
            )
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (
                combined_case.golden_file_name + lang_cls.extension
            )
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=literalizer.BothVariableForms(
                        name="my_data",
                    ),
                    wrap_in_file=True,
                )
            except UnrepresentableIntegerError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_cls.__name__} cannot represent integer in "
                    "this input"
                )
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_cls.__name__} cannot represent this "
                    "heterogeneous input"
                )
            check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=lang_cls.extension,
                newline="",
                golden_path=golden_path,
            )
