"""Rust call fragments whose incomplete syntax has no compiling
surface.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer.languages import Rust
from tests.toml_cases import load_toml_cases


class _CallLiteralCase(BaseModel, extra="forbid", frozen=True):
    """One Rust expression and its independently declared trailing
    comments.
    """

    name: str
    statement: str
    expected_code: str
    expected_trailing: str


class _CallLiteralCases(BaseModel, extra="forbid", frozen=True):
    """The Rust-specific scanner corpus."""

    cases: tuple[_CallLiteralCase, ...]


_CASES = TypeAdapter(type=_CallLiteralCases).validate_python(
    load_toml_cases(name="rust_call_literals")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_rust_call_literals(case: _CallLiteralCase) -> None:
    """Declarations and assignments preserve comments after Rust
    literals.
    """
    language = Rust()
    expression = f"{case.expected_code};{case.expected_trailing}"
    assert (
        language.format_call_variable_declaration(
            "widget", case.statement, 1, frozenset()
        )
        == f"let widget = {expression}"
    )
    assert (
        language.format_call_variable_assignment("widget", case.statement, 1)
        == f"widget = {expression}"
    )
