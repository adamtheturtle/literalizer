"""Declarative contracts for the shared call-comment scanner and
descriptors.
"""

from typing import ClassVar

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import (
    ExistingVariable,
    InputFormat,
    NewVariable,
    literalize_call,
)
from literalizer._language import (
    line_comment_call_variable_assignment,
    line_comment_call_variable_declaration,
)
from literalizer._statements import split_trailing_line_comments
from literalizer.languages import Haxe
from tests.toml_cases import load_toml_cases


class _CommentCase(BaseModel, extra="forbid", frozen=True):  # noqa: NOD001
    """One expression and its independently declared trailing comments."""

    name: str
    statement: str
    expected_code: str
    expected_trailing: str
    regex_literals: bool = False
    backtick_strings: bool = False
    raw_string_prefixes: tuple[str, ...] = ()
    verbatim_strings: bool = False
    interpolation_syntax: tuple[str, str] | None = None


class _CommentCases(BaseModel, extra="forbid", frozen=True):
    """The manifest-owned scanner corpus."""

    cases: tuple[_CommentCase, ...]


_CASES = TypeAdapter(type=_CommentCases).validate_python(
    load_toml_cases(name="trailing_line_comments")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_trailing_line_comments(case: _CommentCase) -> None:
    """Only comments after the complete expression are split off."""
    assert split_trailing_line_comments(
        statement=case.statement,
        prefix="//",
        regex_literals=case.regex_literals,
        backtick_strings=case.backtick_strings,
        raw_string_prefixes=case.raw_string_prefixes,
        verbatim_strings=case.verbatim_strings,
        interpolation_syntax=case.interpolation_syntax,
    ) == (case.expected_code, case.expected_trailing)


class _CommentAwareHaxe(Haxe):
    """Exercise shared binding descriptors through the public call API."""

    format_call_variable_declaration: ClassVar[property] = (
        line_comment_call_variable_declaration(
            regex_literals=True,
            raw_string_prefixes=(),
            verbatim_strings=False,
            interpolation_syntax=("${", "'"),
        )
    )
    format_call_variable_assignment: ClassVar[property] = (
        line_comment_call_variable_assignment(
            regex_literals=True,
            raw_string_prefixes=(),
            verbatim_strings=False,
            interpolation_syntax=("${", "'"),
        )
    )


@pytest.mark.parametrize(
    argnames=("variable_form", "expected"),
    argvalues=[
        (
            NewVariable(name="my_data", modifiers=frozenset()),
            "final my_data = make_widget(42); // note",
        ),
        (
            ExistingVariable(name="my_data"),
            "my_data = make_widget(42); // note",
        ),
    ],
)
def test_shared_call_binding_descriptors(
    variable_form: NewVariable | ExistingVariable, expected: str
) -> None:
    """Both shared descriptors place the terminator before final
    comments.
    """
    result = literalize_call(
        source="42",
        input_format=InputFormat.JSON,
        language=_CommentAwareHaxe(),
        target_function="make_widget",
        parameter_names=["count"],
        per_element=False,
        variable_form=variable_form,
        call_transform=lambda context: context.call + " // note",
        wrap_in_file=False,
    )
    assert result.code == expected
