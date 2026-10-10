"""Declarative contracts for the shared call-comment scanner and
descriptors.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

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


class _CommentHaxe(Haxe):
    """Attach the shared descriptors to a language for contract checks."""

    comment_declaration = line_comment_call_variable_declaration(
        regex_literals=True,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=("${", "'"),
    )
    comment_assignment = line_comment_call_variable_assignment(
        regex_literals=True,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=("${", "'"),
    )


def test_shared_call_declaration_descriptor() -> None:
    """The shared descriptor delegates declaration formatting and retains
    comments.
    """
    language = _CommentHaxe()
    assert isinstance(language, _CommentHaxe)
    formatter = language.comment_declaration
    assert callable(formatter)
    assert formatter(
        "my_data", "make_widget(42) // note", 42, frozenset()
    ) == ("final my_data = make_widget(42); // note")


def test_shared_call_assignment_descriptor() -> None:
    """The shared descriptor delegates assignment formatting and retains
    comments.
    """
    language = _CommentHaxe()
    assert isinstance(language, _CommentHaxe)
    formatter = language.comment_assignment
    assert callable(formatter)
    assert formatter("my_data", "make_widget(42) // note", 42) == (
        "my_data = make_widget(42); // note"
    )
