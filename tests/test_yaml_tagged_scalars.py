"""Explicit YAML scalar tag handling."""

from literalizer import InputFormat, literalize
from literalizer.languages import Python


def test_custom_yaml_scalar_tag_uses_its_payload() -> None:
    """An application-specific scalar tag does not leak its wrapper."""
    rendered = literalize(
        source="key: !example value\n",
        input_format=InputFormat.YAML,
        language=Python(),
    )

    assert '"key": "value"' in rendered.code
