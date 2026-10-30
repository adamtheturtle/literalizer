"""Native formatter offsets unavailable in YAML/TOML timestamps (#6574).

Ruby's reference framework rejects native bindings; the runtime runner
executes these formatter expressions directly and checks their values.
"""

import datetime as dt

import pytest

from literalizer.languages import Ruby


@pytest.mark.parametrize(
    argnames=("offset", "expression"),
    argvalues=[
        (dt.timedelta(seconds=1), "1"),
        (dt.timedelta(seconds=-1), "-1"),
        (dt.timedelta(microseconds=1), "Rational(1, 1000000)"),
        (dt.timedelta(microseconds=-1), "Rational(-1, 1000000)"),
        (
            dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=1),
            "Rational(19815000001, 1000000)",
        ),
        (
            -dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=1),
            "Rational(-19815000001, 1000000)",
        ),
    ],
)
def test_ruby_subminute_datetime_offset(
    offset: dt.timedelta,
    expression: str,
) -> None:
    """The direct formatter retains native subminute offset precision."""
    stamp = dt.datetime(
        year=2001,
        month=2,
        day=3,
        hour=4,
        minute=5,
        second=6,
        tzinfo=dt.timezone(offset=offset),
    )
    assert Ruby().format_datetime(stamp) == (
        f"Time.new(2001, 2, 3, 4, 5, 6, {expression})"
    )
