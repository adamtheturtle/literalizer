"""Golden-file tests across the cross-product of language formatter
variants and input cases.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    NullInCollectionError,
)

from .golden_assertions import check_golden
from .language_specs import lang_cls_name
from .variant_cases import (
    group_variant_cases_by_language,
    variant_languages,
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
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=variant.spec,
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
