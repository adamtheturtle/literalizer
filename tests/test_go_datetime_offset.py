"""Go datetime offset rendering tests."""

from literalizer import InputFormat, literalize
from literalizer.languages import Go


def test_go_datetime_preserves_non_utc_offset() -> None:
    """An aware datetime uses a fixed zone with its parsed offset."""
    result = literalize(
        source="2024-01-02 03:04:05 -05:00",
        input_format=InputFormat.YAML,
        language=Go(),
    )

    assert 'time.FixedZone("", -18000)' in result.code


def test_go_utc_datetime_uses_utc_location() -> None:
    """A UTC datetime retains the concise standard-library location."""
    result = literalize(
        source="2024-01-02 03:04:05 +00:00",
        input_format=InputFormat.YAML,
        language=Go(),
    )

    assert "time.UTC" in result.code
