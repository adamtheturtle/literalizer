"""TOML-driven formatter contracts without a whole-file golden surface."""

import datetime as dt

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer._formatters.format_integers import (
    make_negative_nondecimal_i64_formatter,
)
from literalizer._language import DateFormatEnum
from tests.enum_members import enum_member_by_name
from tests.integration.case_manifests import ManifestLanguage
from tests.toml_cases import load_toml_cases


class _IntegerSuffixCase(BaseModel, extra="forbid", frozen=True):
    """One pre-rendered integer and its composed suffix."""

    name: str
    value: int
    rendered: str
    suffix: str
    base_suffix: str
    expected: str


class _LanguageCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """The identity of a direct language operation."""

    name: str
    language: ManifestLanguage


class _DateViewCase(_LanguageCase, frozen=True):
    """A datetime accepted through an option's date interface."""

    format: str
    value: dt.datetime


class _FormatterCases(BaseModel, extra="forbid", frozen=True):
    """The complete manifest-owned direct formatter corpus."""

    integer_suffixes: tuple[_IntegerSuffixCase, ...]
    date_views: tuple[_DateViewCase, ...]


_CASES = TypeAdapter(type=_FormatterCases).validate_python(
    load_toml_cases(name="formatter_operations")
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES.integer_suffixes,
    ids=lambda case: case.name,
)
def test_integer_suffix_composition(case: _IntegerSuffixCase) -> None:
    """Retain or widen a pre-existing suffix without duplication."""
    formatter = make_negative_nondecimal_i64_formatter(
        base=lambda _value: case.rendered,
        suffix=case.suffix,
        base_suffix=case.base_suffix,
    )
    assert formatter(case.value) == case.expected


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.date_views, ids=lambda case: case.name
)
def test_date_formatter_accepts_datetime(case: _DateViewCase) -> None:
    """Accept datetime through the date interface, outside API
    dispatch.
    """
    member = enum_member_by_name(
        enum_cls=case.language.DateFormats, name=case.format
    )
    assert isinstance(member, DateFormatEnum)
    assert member(case.value) == member(case.value.date())
