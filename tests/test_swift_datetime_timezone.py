"""Swift datetime timezone rendering tests."""

from literalizer import InputFormat, literalize
from literalizer.languages import Swift


def test_swift_datetime_preserves_utc_offset() -> None:
    """An aware datetime explicitly carries its parsed offset."""
    result = literalize(
        source="2024-01-02 03:04:05 -05:00",
        input_format=InputFormat.YAML,
        language=Swift(),
    )

    assert "timeZone: TimeZone(secondsFromGMT: -18000)!" in result.code


def test_swift_naive_datetime_uses_utc() -> None:
    """A naive datetime is deterministic across host time zones."""
    result = literalize(
        source="2024-01-02 03:04:05",
        input_format=InputFormat.YAML,
        language=Swift(),
    )

    assert "timeZone: TimeZone(secondsFromGMT: 0)!" in result.code
