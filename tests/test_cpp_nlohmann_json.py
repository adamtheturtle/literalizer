"""Focused tests for structural nlohmann JSON rendering."""

from literalizer import CollectionLayout, InputFormat, NewVariable, literalize
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
        "nlohmann::json::number_integer_t{(-9223372036854775807LL - 1)}"
        in result.code
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
