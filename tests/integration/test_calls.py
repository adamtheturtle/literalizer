"""``literalize_call`` golden-file tests against each language's default
spec.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .call_cases import CallCase, discover_call_cases, run_call_golden_case
from .language_specs import make_spec


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=discover_call_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in discover_call_cases()
    ],
)
def test_call_golden_file(
    call_case: CallCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_call output matches expected golden file."""
    config = call_case.config
    lang_cls = call_case.lang_cls
    kwargs: dict[str, object] = {}
    if config.call_style_type is not None:
        style = next(
            s
            for s in lang_cls.CallStyles
            if isinstance(s.value, config.call_style_type)
        )
        kwargs["call_style"] = style
    spec = make_spec(lang_cls=lang_cls, **kwargs)
    run_call_golden_case(
        config=config,
        spec=spec,
        golden_name=f"{lang_cls.__name__}_call",
        cases_dir=cases_dir,
        file_regression=file_regression,
    )
