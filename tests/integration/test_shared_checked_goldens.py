"""Shared checked calls retain complete executable golden programs."""

import subprocess
import sys
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, literalize_invocations

from .golden_checks import check_golden, format_consumer
from .shared_checked_cases import SharedCheckedCase, shared_checked_cases


@pytest.mark.parametrize(
    argnames="case",
    argvalues=shared_checked_cases(cases_dir=Path(__file__).parent / "cases"),
    ids=lambda case: (
        f"{case.name}/{case.lang_cls.__name__}/{case.version.name}"
    ),
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
        language=case.spec,
        invocation=recipe.invocation,
        pre_indent_level=(
            recipe.pre_indent_level
            if case.consumer.pre_indent_level is None
            else case.consumer.pre_indent_level
        ),
    )
    template = case.consumer.template
    if template is None:
        template = recipe.consumer_template
    program = format_consumer(
        template=template.replace(
            "{expected_calls}", str(object=recipe.expected_calls)
        ),
        result=result,
        golden_path=case.golden_path,
    )
    check_golden(
        contents=program,
        golden_path=case.golden_path,
        file_regression=file_regression,
    )
    if len(case.consumer.execution) > 0:
        completed = subprocess.run(  # noqa: S603 - execute complete native fixtures
            args=[
                arg.format(python=sys.executable, golden_path=case.golden_path)
                for arg in case.consumer.execution
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
