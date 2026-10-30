"""Native offsets outside serialized timestamps use exact Date instants.

Node executes these constructors in the JavaScript roundtrip check (#6582).
"""

import datetime as dt

import pytest

from literalizer.languages import JavaScript


@pytest.mark.parametrize(
    argnames=("year", "wall", "offset", "expression"),
    argvalues=[
        (1970, 0, 1_000_000, "new Date(-1000)"),
        (1970, 1, 1, "new Date(0)"),
        (1970, 999999, -1, "new Date(1000)"),
        (1, 0, 1_000_000, "new Date(-62135596801000)"),
    ],
)
def test_exact_native_javascript_datetime_instant(
    year: int,
    wall: int,
    offset: int,
    expression: str,
) -> None:
    """Preserve exact instants, including beyond the UTC calendar
    bound.
    """
    stamp = dt.datetime(
        year=year,
        month=1,
        day=1,
        microsecond=wall,
        tzinfo=dt.timezone(offset=dt.timedelta(microseconds=offset)),
    )
    assert JavaScript().format_datetime(stamp) == expression
