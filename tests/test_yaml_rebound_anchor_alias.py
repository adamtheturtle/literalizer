"""TOML-driven tests for YAML aliases whose anchor was rebound."""

import warnings

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python
from tests.toml_cases import load_toml_cases


class _ReboundAliasCase(BaseModel, extra="forbid", frozen=True):
    """One duplicate-anchor input and its expected Python rendering."""

    id: str
    source: str
    expected: str


_CASES = TypeAdapter(type=tuple[_ReboundAliasCase, ...]).validate_python(
    load_toml_cases(name="yaml_rebound_anchor_alias")["cases"]
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES,
    ids=lambda case: case.id,
)
def test_rebound_anchor_is_not_a_cycle(case: _ReboundAliasCase) -> None:
    """An alias taking a newer binding is not a self-reference."""
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore")
        result = literalize(
            source=case.source,
            input_format=InputFormat.YAML,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )
    assert result.code == case.expected
