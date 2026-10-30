"""Native offsets finer than Go's integer-second time zones are rejected.

These native reference values cannot be written as YAML/TOML timestamps
in a rejection manifest (#6575).
"""

import datetime as dt

import pytest

from literalizer import InputFormat, NewVariable, ValueInput, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Go


@pytest.mark.parametrize(
    argnames="offset",
    argvalues=[
        dt.timedelta(microseconds=1),
        dt.timedelta(microseconds=-1),
        dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=1),
        -dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=1),
    ],
)
@pytest.mark.parametrize(
    argnames="position", argvalues=["scalar", "key", "nested"]
)
def test_go_fractional_datetime_offset_rejected(
    offset: dt.timedelta,
    position: str,
) -> None:
    """Unsupported offset precision raises a representation error."""
    stamp = dt.datetime(
        year=2001,
        month=2,
        day=3,
        hour=4,
        minute=5,
        second=6,
        microsecond=123456,
        tzinfo=dt.timezone(offset=offset),
    )
    value: ValueInput = stamp
    if position == "key":
        value = {stamp: "key"}
    elif position == "nested":
        value = {"stamps": [stamp]}
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="Go native datetime format cannot preserve subsecond UTC offset",
    ):
        _ = literalize(
            source='{"$ref": "binding"}',
            input_format=InputFormat.JSON,
            language=Go(),
            variable_form=NewVariable(
                name="result_data", modifiers=frozenset()
            ),
            ref_key="$ref",
            bound_refs={"binding": value},
            wrap_in_file=True,
        )
