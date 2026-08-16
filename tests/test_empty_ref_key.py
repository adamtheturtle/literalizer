"""Explicit empty-string reference-marker keys."""

from literalizer import InputFormat, literalize, literalize_call
from literalizer.languages import Python


def test_literalize_empty_ref_key_emits_identifier() -> None:
    """An explicit empty ref key remains distinct from disabled refs."""
    result = literalize(
        source='[{"": "external_value"}]',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="",
    )
    assert result.code == "(\n    external_value,\n)"


def test_literalize_call_empty_ref_key_emits_identifier() -> None:
    """Call arguments also recognize an explicit empty ref key."""
    result = literalize_call(
        source='[[{"": "external_value"}]]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="consume",
        parameter_names=("value",),
        ref_key="",
    )
    assert "consume(value=external_value)" in result.code


def test_omitted_ref_key_keeps_empty_key_as_data() -> None:
    """Omitting ref_key preserves the historical disabled behavior."""
    result = literalize(
        source='[{"": "external_value"}]',
        input_format=InputFormat.JSON,
        language=Python(),
    )
    assert '{"": "external_value"}' in result.code
