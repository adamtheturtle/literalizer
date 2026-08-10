"""SystemVerilog null-representation tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import SystemVerilog


def test_systemverilog_rejects_null() -> None:
    """Null never aliases the empty-string tagged value."""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source='{"a": null, "b": ""}',
            input_format=InputFormat.JSON,
            language=SystemVerilog(),
        )


def test_systemverilog_preserves_empty_string() -> None:
    """An empty string remains a valid string-tagged value."""
    result = literalize(
        source='{"b": ""}',
        input_format=InputFormat.JSON,
        language=SystemVerilog(),
    )

    assert '_VVAL_STR, i: 0, r: 0.0, s: ""' in result.code
