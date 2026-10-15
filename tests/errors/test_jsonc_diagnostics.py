"""JSONC parser coordinates refer to the original commented source."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSONCParseError
from literalizer.languages import Python


@pytest.mark.parametrize(argnames="ending", argvalues=["\n", "\r", "\r\n"])
@pytest.mark.parametrize(
    argnames="body", argvalues=['{"a": !}', '{"a": 1, "a": 2}', '{"a": 1e999}']
)
def test_jsonc_error_coordinates(*, ending: str, body: str) -> None:
    """Syntax, duplicate-key, and range failures retain source
    positions.
    """
    with pytest.raises(expected_exception=JSONCParseError) as caught:
        _ = literalize(
            source="/* heading */" + ending + body,
            input_format=InputFormat.JSONC,
            language=Python(),
        )
    expected_column = 10 if body == '{"a": 1, "a": 2}' else 7
    assert (caught.value.line, caught.value.column) == (2, expected_column)
