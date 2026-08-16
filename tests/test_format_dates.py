"""Focused tests for shared temporal formatters."""

import datetime

import pytest

from literalizer._formatters.format_dates import (
    datetime_epoch_seconds,
    datetime_ymdhms_formatter,
    format_datetime_epoch_fractional,
    format_datetime_javascript,
)
from literalizer.exceptions import UnrepresentableInputError


def test_javascript_naive_datetime_uses_calendar_components() -> None:
    """Naive input must not be parsed as a host-time-zone instant."""
    value = datetime.datetime(  # noqa: DTZ001 - intentionally naive input
        year=2024,
        month=1,
        day=15,
        hour=12,
        minute=30,
        second=1,
        microsecond=123000,
    )

    assert format_datetime_javascript(value=value) == (
        "new Date(2024, 0, 15, 12, 30, 1, 123)"
    )


def test_javascript_aware_datetime_keeps_explicit_offset() -> None:
    """Aware input retains its offset in the native constructor."""
    value = datetime.datetime(
        year=2024,
        month=1,
        day=15,
        hour=12,
        minute=30,
        second=1,
        microsecond=123000,
        tzinfo=datetime.timezone(
            offset=datetime.timedelta(hours=5, minutes=30)
        ),
    )

    assert format_datetime_javascript(value=value) == (
        'new Date("2024-01-15T12:30:01.123+05:30")'
    )


def test_javascript_datetime_rejects_sub_millisecond_precision() -> None:
    """JavaScript Date must not silently truncate Python microseconds."""
    value = datetime.datetime(  # noqa: DTZ001 - intentionally naive input
        year=2024, month=1, day=15, microsecond=123456
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="sub-millisecond",
    ):
        format_datetime_javascript(value=value)


def test_integer_epoch_rejects_fractional_seconds() -> None:
    """Integer epoch formats must not floor fractional seconds."""
    value = datetime.datetime(
        year=1970, month=1, day=1, microsecond=1, tzinfo=datetime.UTC
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="fractional"
    ):
        datetime_epoch_seconds(value=value)


@pytest.mark.parametrize(
    argnames=("value", "expected"),
    argvalues=[
        (
            datetime.datetime(
                year=1970,
                month=1,
                day=1,
                microsecond=1,
                tzinfo=datetime.UTC,
            ),
            "0.000001",
        ),
        (
            datetime.datetime(
                year=1969,
                month=12,
                day=31,
                hour=23,
                minute=59,
                second=59,
                microsecond=500000,
                tzinfo=datetime.UTC,
            ),
            "-0.5",
        ),
        (
            datetime.datetime(
                year=1970,
                month=1,
                day=1,
                second=1,
                tzinfo=datetime.UTC,
            ),
            "1",
        ),
    ],
)
def test_fractional_epoch_is_exact(
    value: datetime.datetime, expected: str
) -> None:
    """Fractional epoch literals preserve both sign and microseconds."""
    assert format_datetime_epoch_fractional(value=value) == expected


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[
        datetime.datetime(  # noqa: DTZ001 - intentionally naive input
            year=2024, month=1, day=15, microsecond=1
        ),
        datetime.datetime(year=2024, month=1, day=15, tzinfo=datetime.UTC),
    ],
)
def test_whole_second_naive_formatter_rejects_lossy_datetimes(
    value: datetime.datetime,
) -> None:
    """A whole-second naive constructor rejects precision or awareness."""
    formatter = datetime_ymdhms_formatter(
        template=(
            "DateTime({year}, {month}, {day}, {hour}, {minute}, {second})"
        )
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot preserve",
    ):
        formatter(value)
