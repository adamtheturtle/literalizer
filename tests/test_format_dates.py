"""Tests for exact date and datetime formatting helpers."""

import datetime

from literalizer._formatters.format_dates import datetime_epoch_seconds

_FAR_FUTURE_EXPECTED_EPOCH_SECONDS = 32535215999


def test_far_future_epoch_seconds_do_not_round_into_next_second() -> None:
    """Far-future microseconds remain below the following whole second."""
    value = datetime.datetime(
        year=3000,
        month=12,
        day=31,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
        tzinfo=datetime.UTC,
    )
    assert (
        datetime_epoch_seconds(value=value)
        == _FAR_FUTURE_EXPECTED_EPOCH_SECONDS
    )


def test_epoch_seconds_floor_negative_fraction() -> None:
    """A fractional instant before the epoch floors to minus one."""
    value = datetime.datetime(  # noqa: DTZ001
        year=1969,
        month=12,
        day=31,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )
    assert datetime_epoch_seconds(value=value) == -1
