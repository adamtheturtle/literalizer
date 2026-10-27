"""Public input formats declare whether they support null values."""

from literalizer import InputFormat


def test_formats_supporting_null() -> None:
    """Null support is metadata, separate from a document's rendering."""
    assert {
        input_format
        for input_format in InputFormat
        if input_format.supports_null
    } == {
        InputFormat.JSON,
        InputFormat.JSONC,
        InputFormat.JSON5,
        InputFormat.YAML,
    }
