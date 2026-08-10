"""Opt-in ref-marker API behavior."""

from literalizer import InputFormat, literalize
from literalizer.languages import Python


def test_json_schema_ref_is_data_by_default() -> None:
    """The standard JSON Schema ``$ref`` key is not rewritten
    implicitly.
    """
    result = literalize(
        source='{"schema": {"$ref": "#/defs/Foo"}}',
        input_format=InputFormat.JSON,
        language=Python(),
    )

    assert '"$ref": "#/defs/Foo"' in result.code


def test_explicit_ref_key_enables_marker_rendering() -> None:
    """Callers can explicitly request the historical marker syntax."""
    result = literalize(
        source='{"schema": {"$ref": "foo"}}',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="$ref",
    )

    assert '"schema": foo' in result.code
