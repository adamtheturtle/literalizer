"""Scanner-only contracts with no compiling call-binding surface."""

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer._statements import (
    PrefixedIdentifierSyntax,
    split_trailing_line_comments,
)
from tests.toml_cases import load_toml_cases


class _IdentifierSpanCase(BaseModel, extra="forbid", frozen=True):
    """A scanner's prefix and complete identifier token grammar."""

    prefix: str
    identifier: str


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
    identifier_span: _IdentifierSpanCase | None = None


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
    span = (
        None
        if case.identifier_span is None
        else PrefixedIdentifierSyntax(
            prefix=case.identifier_span.prefix,
            identifier=case.identifier_span.identifier,
        )
    )
    comments = split_trailing_line_comments(
        statement=case.statement,
        prefix="//",
        regex_literals=case.regex_literals,
        quotes="\"'",
        literal_span_end=span,
        backtick_strings=case.backtick_strings,
        raw_string_prefixes=case.raw_string_prefixes,
        verbatim_strings=case.verbatim_strings,
        interpolation_syntax=case.interpolation_syntax,
    )
    assert comments.code == case.expected_code
    assert comments.trailing_comments == case.expected_trailing
