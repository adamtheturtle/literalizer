"""Focused tests for shared temporal formatters."""

import datetime

import pytest

from literalizer._formatters.format_dates import (
    datetime_epoch_seconds,
    format_datetime_epoch_fractional,
    format_datetime_javascript,
)
from literalizer.exceptions import UnrepresentableInputError


def test_javascript_naive_datetime_uses_calendar_components() -> None:
    """Naive input must not be parsed as a host-time-zone instant."""
    value = datetime.datetime(  # noqa: DTZ001 - intentionally naive input
        2024, 1, 15, 12, 30, 1, 123000
    )

    assert format_datetime_javascript(value) == (
        "new Date(2024, 0, 15, 12, 30, 1, 123)"
    )


def test_javascript_aware_datetime_keeps_explicit_offset() -> None:
    """Aware input retains its offset in the native constructor."""
    value = datetime.datetime(
        2024,
        1,
        15,
        12,
        30,
        1,
        123000,
        tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30)),
    )

    assert format_datetime_javascript(value) == (
        'new Date("2024-01-15T12:30:01.123+05:30")'
    )


def test_javascript_datetime_rejects_sub_millisecond_precision() -> None:
    """JavaScript Date must not silently truncate Python microseconds."""
    value = datetime.datetime(  # noqa: DTZ001 - intentionally naive input
        2024, 1, 15, microsecond=123456
    )

    with pytest.raises(UnrepresentableInputError, match="sub-millisecond"):
        format_datetime_javascript(value)


def test_integer_epoch_rejects_fractional_seconds() -> None:
    """Integer epoch formats must not floor fractional seconds."""
    value = datetime.datetime(1970, 1, 1, microsecond=1, tzinfo=datetime.UTC)

    with pytest.raises(UnrepresentableInputError, match="fractional"):
        datetime_epoch_seconds(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            datetime.datetime(1970, 1, 1, microsecond=1, tzinfo=datetime.UTC),
            "0.000001",
        ),
        (
            datetime.datetime(
                1969,
                12,
                31,
                23,
                59,
                59,
                500000,
                tzinfo=datetime.UTC,
            ),
            "-0.5",
        ),
        (datetime.datetime(1970, 1, 1, second=1, tzinfo=datetime.UTC), "1"),
    ],
)
def test_fractional_epoch_is_exact(
    value: datetime.datetime, expected: str
) -> None:
    """Fractional epoch literals preserve both sign and microseconds."""
    assert format_datetime_epoch_fractional(value) == expected
