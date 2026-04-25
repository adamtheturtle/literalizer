"""Golden-file tests for combined declaration + assignment output with
non-default line endings.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_discovery import (
    LineEndingCombinedCase,
    build_line_ending_combined_cases,
)
from .golden_assertions import check_golden
from .language_specs import find_redefinition_styles, make_spec


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_line_ending_combined_cases(),
    ids=[c.name for c in build_line_ending_combined_cases()],
)
def test_line_ending_combined_variable_forms(
    case: LineEndingCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default line ending matches the golden file.
    """
    input_path = cases_dir / case.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    base_spec = make_spec(lang_cls=case.lang_cls)
    redef_styles = find_redefinition_styles(spec=base_spec)
    assert redef_styles
    spec = make_spec(
        lang_cls=case.lang_cls,
        line_ending=case.line_ending,
        declaration_style=redef_styles[0],
    )
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=literalizer.BothVariableForms(name="my_data"),
        wrap_in_file=True,
    )
    check_golden(
        file_regression=file_regression,
        contents=result.code + "\n",
        extension=spec.extension,
        newline=None,
        golden_path=input_path.parent / (case.name + spec.extension),
    )
