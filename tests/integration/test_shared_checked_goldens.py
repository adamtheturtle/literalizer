"""Shared checked calls retain complete executable golden programs."""

import subprocess
import sys
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, literalize_invocations
from literalizer.languages import Python

from .golden_checks import check_golden
from .language_specs import make_spec
from .shared_checked_cases import SharedCheckedCase, shared_checked_cases


@pytest.mark.parametrize(
    argnames="case",
    argvalues=shared_checked_cases(cases_dir=Path(__file__).parent / "cases"),
    ids=lambda case: f"{case.name}/{case.version.name}",
)
def test_shared_checked_golden(
    case: SharedCheckedCase, file_regression: FileRegressionFixture
) -> None:
    """The actual public result must call receivers and pair expected rows."""
    recipe = case.recipe
    result = literalize_invocations(
        source=recipe.source,
        input_format=InputFormat.JSON,
        zip_source=recipe.zip_source,
        zip_input_format=InputFormat.JSON,
        language=make_spec(
            lang_cls=Python,
            language_version=case.version,
            call_style=Python.call_styles["POSITIONAL"],
        ),
        invocation=recipe.invocation,
        pre_indent_level=recipe.pre_indent_level,
    )
    program = recipe.consumer_template.format(
        preamble="\n".join(result.preamble), code=result.code
    )
    check_golden(
        contents=program,
        extension=Python.extension,
        golden_path=case.golden_path,
        file_regression=file_regression,
    )
    completed = subprocess.run(  # noqa: S603 - execute complete native fixtures
        args=[sys.executable, "-I", str(object=case.golden_path)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
