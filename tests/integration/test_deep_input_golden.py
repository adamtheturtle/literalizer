"""Below-guard input depths render into complete native programs."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import literalize

from .deep_input_cases import DeepInputCase, deep_input_cases
from .golden_checks import check_golden


@pytest.mark.parametrize(
    argnames="case",
    argvalues=deep_input_cases(cases_dir=Path(__file__).parent / "cases"),
    ids=lambda case: case.manifest.case_dir.name,
)
def test_deep_input_golden_program(
    case: DeepInputCase, file_regression: FileRegressionFixture
) -> None:
    """Retain the unwrapped API call and consume its actual native
    value.
    """
    recipe = case.recipe
    result = literalize(
        source=recipe.source,
        input_format=recipe.input_format,
        language=recipe.language(),
    )
    contents = recipe.consumer_template.format(
        preamble="\n".join(result.preamble),
        body_preamble="\n".join(result.body_preamble),
        code=result.bare_code,
        depth=recipe.depth,
    )
    check_golden(
        contents=contents,
        extension=recipe.language.extension,
        golden_path=case.golden_path,
        file_regression=file_regression,
    )
