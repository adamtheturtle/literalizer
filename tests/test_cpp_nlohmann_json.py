"""Focused tests for structural nlohmann JSON rendering."""

from literalizer import InputFormat, NewVariable, literalize
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
