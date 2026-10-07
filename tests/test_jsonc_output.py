"""JSONC output keeps JSON syntax while preserving source comments."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Jsonc
from literalizer.languages.jsonc import JsoncTrailingCommas


def test_jsonc_output_rejects_nonfinite_numbers() -> None:
    """Non-finite numeric tokens cannot leak into JSONC output."""
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        _ = literalize(
            source="value: .nan",
            input_format=InputFormat.YAML,
            language=Jsonc(),
        )


def test_jsonc_has_no_trailing_comma_option() -> None:
    """JSONC exposes only the strict JSON comma behavior."""
    assert list(JsoncTrailingCommas) == [JsoncTrailingCommas.NO]
