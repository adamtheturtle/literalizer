"""Golden-file tests covering ``pre_indent_level > 0`` output."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_discovery import PreIndentCase, build_pre_indent_cases
from .golden_assertions import check_golden
from .language_specs import make_spec


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_pre_indent_cases(),
    ids=[c.name for c in build_pre_indent_cases()],
)
def test_pre_indent_level_with_new_variable_golden_file(
    case: PreIndentCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """``pre_indent_level > 0`` with ``NewVariable`` produces uniformly
    indented output.

    Regression test for the bug where the first line of a multi-line
    value was inserted after ``=`` with the indent baked in, producing
    extra spaces between ``=`` and the value and shifting continuation
    lines by an extra indent.
    """
    input_path = cases_dir / case.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    spec = make_spec(lang_cls=case.lang_cls)
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=case.pre_indent_level,
        include_delimiters=True,
        variable_form=literalizer.NewVariable(
            name="my_data",
            modifiers=case.modifiers,
        ),
        wrap_in_file=True,
    )
    check_golden(
        file_regression=file_regression,
        contents=result.code + "\n",
        extension=spec.extension,
        newline=None,
        golden_path=input_path.parent / (case.name + spec.extension),
    )
