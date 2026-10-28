"""Formatter contracts for combinations outside the golden corpus."""

import datetime as dt
from textwrap import dedent

import pytest

from literalizer import FileWrapperContext
from literalizer._language import DateFormatEnum
from literalizer.languages import Roc, Ruby


def test_roc_call_wrapper_without_preamble() -> None:
    """An empty call preamble does not add separator lines."""
    # Wrapped public calls always generate a stub in the body preamble.
    # Only the wrapper itself accepts a call with no stub or declarations.
    language = Roc()
    assert language.wrap_calls_with_declarations(
        declarations=(),
        calls="call",
        context=FileWrapperContext(
            line_prefix="",
            bound_variable_names=(),
            variable_name="",
            modifiers=frozenset(),
            body_preamble=(),
            class_preamble=(),
            has_literal_declarations=False,
            generated_body_preamble=(),
            call_stub_names=frozenset(),
            root_is_object_literal=False,
            root_mapping_entries=None,
            has_existing_bindings=False,
        ),
    ) == dedent(
        text="""\
        module [main]

        main =
            dbg (call)
            {}"""
    )


@pytest.mark.parametrize(
    argnames="date_format",
    argvalues=[Ruby.date_formats.RUBY, Ruby.date_formats.RUBY_SHORT],
)
@pytest.mark.parametrize(
    argnames="value",
    argvalues=[
        dt.datetime(year=1500, month=3, day=1, tzinfo=dt.UTC),
        dt.datetime(year=1582, month=10, day=10, tzinfo=dt.UTC),
        dt.datetime(year=1582, month=10, day=15, tzinfo=dt.UTC),
        dt.datetime(year=2024, month=1, day=15, tzinfo=dt.UTC),
    ],
)
def test_ruby_native_date_formatter_accepts_datetime(
    date_format: DateFormatEnum,
    value: dt.datetime,
) -> None:
    """Native date formatters accept values through the date interface."""
    # Literalize routes datetimes through datetime_format instead, so a
    # date-format golden cannot exercise this direct formatter contract.
    assert date_format(value) == date_format(value.date())
