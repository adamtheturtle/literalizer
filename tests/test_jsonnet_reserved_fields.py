"""Jsonnet object-field quoting tests."""

from literalizer import InputFormat, literalize
from literalizer.languages import Jsonnet


def test_jsonnet_quotes_reserved_object_fields() -> None:
    """Every Jsonnet keyword remains a quoted object field."""
    reserved = (
        "assert",
        "else",
        "error",
        "false",
        "for",
        "function",
        "if",
        "import",
        "importbin",
        "importstr",
        "in",
        "local",
        "null",
        "self",
        "super",
        "tailstrict",
        "then",
        "true",
    )
    source = "{" + ", ".join(f'"{key}": 1' for key in reserved) + "}"

    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Jsonnet(),
    )

    for key in reserved:
        assert f'"{key}": 1' in result.code


def test_jsonnet_keeps_ordinary_object_field_bare() -> None:
    """An ordinary identifier keeps the idiomatic bare spelling."""
    result = literalize(
        source='{"ordinary": 1}',
        input_format=InputFormat.JSON,
        language=Jsonnet(),
    )

    assert "ordinary: 1" in result.code
