"""PHP-specific representation errors."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Php


@pytest.mark.parametrize(
    argnames="source",
    argvalues=['{"0": "a", "1": "b"}', '{"outer": {"-2": "value"}}'],
)
def test_php_numeric_string_mapping_key_raises(source: str) -> None:
    """PHP arrays must not silently coerce string keys to integers."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="coerce numeric string mapping key",
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=Php(),
        )


def test_php_leading_zero_string_mapping_key_is_preserved() -> None:
    """PHP does not coerce integer-looking strings with leading zeros."""
    result = literalize(
        source='{"08": "value"}',
        input_format=InputFormat.JSON,
        language=Php(),
    )

    assert '"08" => "value"' in result.code
