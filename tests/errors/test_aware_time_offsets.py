"""Validation for timezone-aware ``datetime.time`` values.

A manifest spells ``bound_refs`` as a TOML inline table, and TOML has
no offset-carrying time, so the value these bind cannot be written in
one.
"""

import datetime

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Go, Hcl, Python

_AWARE_TIME = datetime.time(
    hour=12,
    minute=30,
    second=15,
    tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
)


@pytest.mark.parametrize(argnames="language", argvalues=[Go(), Python()])
def test_aware_time_rejected_when_native_formatter_drops_offset(
    language: Language,
) -> None:
    """Constructor output must not silently turn an aware time naive."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=r"native time format cannot preserve UTC offset 2:00:00",
    ):
        literalize(
            source='{"x": {"$ref": "value"}}',
            input_format=InputFormat.JSON,
            language=language,
            ref_key="$ref",
            bound_refs={"value": _AWARE_TIME},
            variable_form=NewVariable(name="out", modifiers=frozenset()),
            wrap_in_file=True,
        )


def test_aware_time_allowed_when_string_formatter_preserves_offset() -> None:
    """Offset-preserving string back ends remain supported."""
    result = literalize(
        source='{"x": {"$ref": "value"}}',
        input_format=InputFormat.JSON,
        language=Hcl(),
        ref_key="$ref",
        bound_refs={"value": _AWARE_TIME},
        variable_form=NewVariable(name="out", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert '"12:30:15+02:00"' in result.code
