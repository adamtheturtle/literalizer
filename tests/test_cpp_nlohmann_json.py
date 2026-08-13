"""Focused tests for nlohmann JSON rendering."""

import pytest

from literalizer import CollectionLayout, InputFormat, NewVariable, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Cpp


def test_signed_64_bit_minimum_uses_a_portable_expression() -> None:
    """Avoid an out-of-range positive token for signed 64-bit minimum."""
    result = literalize(
        source="-9223372036854775808",
        input_format=InputFormat.JSON,
        language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert (
        result.code
        == "auto my_data = nlohmann::json((-9223372036854775807LL - 1));"
    )


def test_variable_declaration_honours_multiline_collection_layout() -> None:
    """Keep structural JSON declarations readable for nested documents."""
    result = literalize(
        source='[{"id": "alpha", "size": 1}, {"id": "beta", "size": 2}]',
        input_format=InputFormat.JSON,
        language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
        variable_form=NewVariable(name="rows", modifiers=frozenset()),
        collection_layout=CollectionLayout.MULTILINE,
    )

    assert (
        result.declaration_code
        == """auto rows = nlohmann::json::array({
    nlohmann::json::object({
        {"id", "alpha"},
        {"size", 1},
    }),
    nlohmann::json::object({
        {"id", "beta"},
        {"size", 2},
    }),
});"""
    )


@pytest.mark.parametrize(
    argnames=("source", "expected_token"),
    argvalues=[
        ("0", "0"),
        ("-1", "-1"),
        ("9223372036854775807", "9223372036854775807"),
        ("18446744073709551615", "18446744073709551615"),
    ],
)
def test_inline_document_accepts_json_integer_tokens(
    source: str,
    expected_token: str,
) -> None:
    """Accept decimal integer boundaries covered by JSON grammar."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            json_rendering=Cpp.json_renderings.INLINE_DOCUMENT,
        ),
    )

    assert result.code == expected_token


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            json_rendering=Cpp.json_renderings.INLINE_DOCUMENT,
            integer_format=Cpp.integer_formats.HEX,
        ),
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            json_rendering=Cpp.json_renderings.INLINE_DOCUMENT,
            integer_format=Cpp.integer_formats.OCTAL,
        ),
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            json_rendering=Cpp.json_renderings.INLINE_DOCUMENT,
            integer_format=Cpp.integer_formats.BINARY,
        ),
        Cpp(
            json_type=Cpp.json_types.NLOHMANN_JSON,
            json_rendering=Cpp.json_renderings.INLINE_DOCUMENT,
            numeric_separator=Cpp.numeric_separators.UNDERSCORE,
        ),
    ],
)
def test_inline_document_rejects_non_json_integer_tokens(
    language: Language,
) -> None:
    """Reject C++-specific base and separator syntax inside JSON."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match="does not produce a valid JSON integer token",
    ):
        literalize(
            source="1000",
            input_format=InputFormat.JSON,
            language=language,
        )
