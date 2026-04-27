"""Golden-file tests that drive :func:`literalizer.literalize`.

Each test exercises a different axis of the public API — single
declaration form, combined declaration + assignment, format-variant
kwargs, line-ending option, heterogeneous-scalar strategy,
``pre_indent_level`` — but all share the same shape: render YAML to a
language and compare against a checked-in golden file.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    NullInCollectionError,
    UnrepresentableIntegerError,
)

from .case_discovery import (
    HeterogeneousStrategyCombinedCase,
    LineEndingCombinedCase,
    PreIndentCase,
    build_heterogeneous_strategy_combined_cases,
    build_line_ending_combined_cases,
    build_pre_indent_cases,
    group_cases_by_language,
    group_combined_cases_by_language,
)
from .check_golden import check_golden
from .language_specs import (
    find_redefinition_styles,
    lang_cls_name,
    make_spec,
    make_spec_for_golden,
    sorted_languages,
    with_per_fixture_module_name,
)
from .variant_cases import (
    group_variant_cases_by_language,
    variant_languages,
    wrap_variable_form,
)


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
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
    grouped = group_cases_by_language(cases_dir=cases_dir)
    for case_name in grouped.get(lang_cls, []):
        with subtests.test(case_name=case_name):
            input_path = cases_dir / case_name / "input.yaml"
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (lang_name + lang_cls.extension)
            spec = make_spec_for_golden(
                lang_cls=lang_cls,
                golden_path=golden_path,
            )
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=spec,
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


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
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
    grouped = group_combined_cases_by_language(cases_dir=cases_dir)
    for combined_case in grouped.get(lang_cls, []):
        with subtests.test(
            case_name=combined_case.case_name,
            golden_file_name=combined_case.golden_file_name,
        ):
            input_path = cases_dir / combined_case.case_name / "input.yaml"
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (
                combined_case.golden_file_name + lang_cls.extension
            )
            spec = make_spec_for_golden(
                lang_cls=lang_cls,
                golden_path=golden_path,
                declaration_style=combined_case.declaration_style,
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


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=variant_languages(),
    ids=lang_cls_name,
)
def test_format_variant_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test format-variant options (dates, sequences, sets, type hints)
    against golden files.
    """
    for variant_case in group_variant_cases_by_language()[lang_cls]:
        with subtests.test(
            variant_name=variant_case.variant_name,
            case_dir_name=variant_case.case_dir_name,
        ):
            case_dir = cases_dir / variant_case.case_dir_name
            variant = variant_case.variant
            yaml_string = (case_dir / "input.yaml").read_text()
            golden_path = case_dir / (
                variant_case.variant_name + variant.spec.extension
            )
            spec = with_per_fixture_module_name(
                spec=variant.spec,
                golden_path=golden_path,
            )
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=variant_case.variable_form,
                    wrap_in_file=True,
                )
            except NullInCollectionError:
                pytest.skip("Format rejects null elements in this input")
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip("Format cannot represent this heterogeneous input")
            except IncompatibleFormatsError:
                golden_path.unlink(missing_ok=True)
                pytest.skip("Format combination cannot represent this input")
            check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=variant.spec.extension,
                newline=None,
                golden_path=golden_path,
            )


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
    golden_path = input_path.parent / (case.name + base_spec.extension)
    spec = make_spec_for_golden(
        lang_cls=case.lang_cls,
        golden_path=golden_path,
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
        golden_path=golden_path,
    )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_heterogeneous_strategy_combined_cases(),
    ids=[c.name for c in build_heterogeneous_strategy_combined_cases()],
)
def test_heterogeneous_strategy_combined_variable_forms(
    case: HeterogeneousStrategyCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default heterogeneous-scalar strategy matches the golden file.
    """
    input_path = cases_dir / case.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    base_spec = make_spec(lang_cls=case.lang_cls)
    redef_styles = find_redefinition_styles(spec=base_spec)
    assert redef_styles
    golden_path = input_path.parent / (case.name + base_spec.extension)
    spec = make_spec_for_golden(
        lang_cls=case.lang_cls,
        golden_path=golden_path,
        heterogeneous_strategy=case.heterogeneous_strategy,
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
        golden_path=golden_path,
    )


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
    base_spec = make_spec(lang_cls=case.lang_cls)
    golden_path = input_path.parent / (case.name + base_spec.extension)
    spec = make_spec_for_golden(
        lang_cls=case.lang_cls,
        golden_path=golden_path,
    )
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
        golden_path=golden_path,
    )
