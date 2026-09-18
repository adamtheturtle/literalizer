"""JSONC output keeps JSON syntax while preserving source comments."""

import json

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Jsonc
from literalizer.languages.jsonc import JsoncTrailingCommas


def test_jsonc_output_uses_json_keys_and_no_trailing_commas() -> None:
    """Comment-free output is also valid strict JSON."""
    result = literalize(
        source='{"plain": [1, 2], "with-dash": "a\\nb"}',
        input_format=InputFormat.JSON,
        language=Jsonc(),
    )

    assert result.code == (
        '{\n    "plain": [1, 2],\n    "with-dash": "a\\nb"\n}'
    )
    assert json.loads(s=result.code) == {
        "plain": [1, 2],
        "with-dash": "a\nb",
    }


def test_jsonc_output_preserves_yaml_comments() -> None:
    """JSONC comments use the supported double-slash spelling."""
    result = literalize(
        source="# server\nhost: localhost # default\n",
        input_format=InputFormat.YAML,
        language=Jsonc(),
    )

    assert result.code == (
        '{\n    // server\n    "host": "localhost"  // default\n}'
    )


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
