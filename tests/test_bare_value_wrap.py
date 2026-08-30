"""TOML-driven tests for whole files holding values that bind no name."""

from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import InputFormat, NewVariable, VariableForm, literalize
from literalizer.languages import JavaScript, TypeScript
from tests.toml_cases import load_toml_cases


class _BareValueCase(BaseModel, extra="forbid", frozen=True):
    """One declarative whole-file rendering assertion."""

    id: str
    language: Literal["JavaScript", "TypeScript"]
    source: str
    variable_form: Literal["new", "none"]
    assertion: Literal["contains", "excludes", "starts_with"]
    expected: str


_CASES = TypeAdapter(type=tuple[_BareValueCase, ...]).validate_python(
    load_toml_cases(name="bare_value_wrap")["cases"]
)
_LANGUAGES = {"JavaScript": JavaScript, "TypeScript": TypeScript}


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES,
    ids=lambda case: case.id,
)
def test_bare_value_wrap(case: _BareValueCase) -> None:
    """A declared bare or bound root has its declared code shape."""
    variable_form: VariableForm | None = (
        NewVariable(name="my_data", modifiers=frozenset())
        if case.variable_form == "new"
        else None
    )
    result = literalize(
        source=case.source,
        input_format=InputFormat.JSON,
        language=_LANGUAGES[case.language](),
        wrap_in_file=True,
        variable_form=variable_form,
    )

    if case.assertion == "starts_with":
        assert result.code.startswith(case.expected)
    elif case.assertion == "contains":
        assert case.expected in result.code
    else:
        assert case.expected not in result.code
