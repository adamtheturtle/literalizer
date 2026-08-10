"""Tests for Crystal percent-literal token separation."""

from literalizer import InputFormat, literalize
from literalizer.languages import Crystal


def test_percent_string_dict_keys_do_not_form_macro_tokens() -> None:
    """A hash opener and percent-literal key never form ``{%``."""
    result = literalize(
        source='{"nested": {"a": 1}}',
        input_format=InputFormat.JSON,
        language=Crystal(string_format=Crystal.string_formats.MULTILINE),
    )

    assert "{%" not in result.code
    assert "{ %q|a| => 1}" in result.code


def test_non_string_dict_keys_do_not_gain_spacing() -> None:
    """The separator is limited to keys beginning with a percent token."""
    result = literalize(
        source="1: value",
        input_format=InputFormat.YAML,
        language=Crystal(string_format=Crystal.string_formats.MULTILINE),
    )

    assert "1 => %q|value|" in result.code
    assert "\n    1 =>" in result.code
    assert "\n     1 =>" not in result.code


def test_ordered_map_percent_string_keys_do_not_form_macro_tokens() -> None:
    """The ordered-map opener also stays separate from a percent key."""
    result = literalize(
        source="--- !!omap\n  - a: 1\n  - b: 2\n",
        input_format=InputFormat.YAML,
        language=Crystal(string_format=Crystal.string_formats.MULTILINE),
    )

    assert "{%" not in result.code
    assert "{ %q|a| => 1, %q|b| => 2}" in result.code
