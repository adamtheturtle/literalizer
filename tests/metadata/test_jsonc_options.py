"""JSONC output keeps JSON syntax while preserving source comments."""

from literalizer.languages.jsonc import JsoncTrailingCommas


def test_jsonc_has_no_trailing_comma_option() -> None:
    """JSONC exposes only the strict JSON comma behavior."""
    assert list(JsoncTrailingCommas) == [JsoncTrailingCommas.NO]
