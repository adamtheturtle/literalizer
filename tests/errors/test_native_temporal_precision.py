"""Native offsets can change the precision of the represented instant.

YAML/TOML timestamps cannot express these offsets (#6582).
"""

import datetime as dt

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Go, JavaScript, Python


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Python(datetime_format=Python.datetime_formats.EPOCH),
        Go(datetime_format=Go.datetime_formats.EPOCH),
        JavaScript(datetime_format=JavaScript.datetime_formats.EPOCH),
        JavaScript(),
    ],
)
@pytest.mark.parametrize(argnames="offset", argvalues=[-1, 1])
def test_inexact_native_datetime_instant_rejected(
    language: Language,
    offset: int,
) -> None:
    """An integral wall time does not imply an integral instant."""
    stamp = dt.datetime(
        year=1970,
        month=1,
        day=1,
        tzinfo=dt.timezone(offset=dt.timedelta(microseconds=offset)),
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=r"cannot preserve .*precision",
    ):
        _ = literalize(
            source='{"$ref": "stamp"}',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(
                name="result_data", modifiers=frozenset()
            ),
            ref_key="$ref",
            bound_refs={"stamp": stamp},
            wrap_in_file=True,
        )
