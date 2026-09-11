"""Tests for mapping-key formatting from source keys."""

import pytest

from literalizer.languages import JavaScript, Ruby, TypeScript


@pytest.mark.parametrize(
    argnames="lang_cls", argvalues=[JavaScript, TypeScript]
)
def test_object_proto_key_uses_source_name(
    lang_cls: type[JavaScript] | type[TypeScript],
) -> None:
    """Computed-property selection does not decode the rendered key."""
    language = lang_cls()

    assert (
        language.dict_format_config.format_key(
            raw_key="__proto__", formatted_key='"not the source key"'
        )
        == '["not the source key"]'
    )
    assert (
        language.dict_format_config.format_key(
            raw_key="ordinary", formatted_key='"__proto__"'
        )
        == '"__proto__"'
    )


@pytest.mark.parametrize(
    argnames="lang_cls", argvalues=[JavaScript, TypeScript]
)
def test_ordered_object_proto_key_uses_source_name(
    lang_cls: type[JavaScript] | type[TypeScript],
) -> None:
    """Ordered objects use the same source-key classification."""
    language = lang_cls()

    assert (
        language.ordered_map_format_config.format_key(
            raw_key="__proto__", formatted_key='"not the source key"'
        )
        == '["not the source key"]'
    )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        JavaScript(string_format=JavaScript.string_formats.MULTILINE),
        TypeScript(string_format=TypeScript.string_formats.MULTILINE),
    ],
)
def test_multiline_ordered_object_computes_every_key(
    language: JavaScript | TypeScript,
) -> None:
    """Multiline strings require computed-property syntax."""
    assert (
        language.ordered_map_format_config.format_key(
            raw_key="ordinary", formatted_key='"rendered"'
        )
        == '["rendered"]'
    )


def test_ruby_symbol_label_uses_source_name() -> None:
    """Ruby label eligibility is decided before rendering the key."""
    language = Ruby(dict_entry_style=Ruby.dict_entry_styles.SYMBOL)

    assert (
        language.dict_format_config.format_key(
            raw_key="label?", formatted_key='"not the source key"'
        )
        == "label?"
    )
    assert (
        language.dict_format_config.format_key(
            raw_key="not-a-label", formatted_key='"label"'
        )
        == '"label"'
    )
