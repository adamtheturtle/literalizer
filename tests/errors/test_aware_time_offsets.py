"""Validation for timezone-aware ``datetime.time`` values.

Native formatter rejections remain direct tests. Offset-preserving
rendering is covered by the manifest-owned aware-time reference case.
"""

import datetime as dt

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Go, Python

_AWARE_TIME = dt.time(
    hour=12,
    minute=30,
    second=15,
    tzinfo=dt.timezone(offset=dt.timedelta(hours=2)),
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
        _ = literalize(
            source='{"x": {"$ref": "value"}}',
            input_format=InputFormat.JSON,
            language=language,
            ref_key="$ref",
            bound_refs={"value": _AWARE_TIME},
            variable_form=NewVariable(name="out", modifiers=frozenset()),
            wrap_in_file=True,
        )
