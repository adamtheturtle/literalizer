"""Internal invocation errors for native integer-result transforms."""

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer.languages import Python
from tests.toml_cases import load_toml_cases

from .call_cases import call_transform_for_case, default_call_case_specs


class _ErrorCase(BaseModel, extra="forbid", frozen=True):
    """An unsupported direct use of the internal arithmetic recipe."""

    name: str
    message: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The internal invocation-error corpus."""

    errors: tuple[_ErrorCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="integer_call_transforms")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.errors, ids=lambda case: case.name
)
def test_integer_transform_requires_native_result(case: _ErrorCase) -> None:
    """A direct invocation cannot invent an integer result type."""
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_integer_result_arithmetic_outer"
    )
    with pytest.raises(expected_exception=ValueError, match=case.message):
        _ = call_transform_for_case(spec=Python(), config=config)
