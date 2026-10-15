"""JSON5 parser coordinates refer to the original commented source."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSON5ParseError
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames="ending", argvalues=["\n", "\r", "\r\n", "\u2028", "\u2029"]
)
@pytest.mark.parametrize(
    argnames="body", argvalues=["{a: !}", "{a: 1, a: 2}", "{a: 1e999}"]
)
def test_json5_error_coordinates(*, ending: str, body: str) -> None:
    """Syntax, duplicate-key, and range failures retain source
    positions.
    """
    with pytest.raises(expected_exception=JSON5ParseError) as caught:
        _ = literalize(
            source="/* heading */" + ending + body,
            input_format=InputFormat.JSON5,
            language=Python(),
        )
    expected_column = 8 if body == "{a: 1, a: 2}" else 5
    assert (caught.value.line, caught.value.column) == (2, expected_column)
