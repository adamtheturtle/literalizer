"""C++ ``json_type`` rejection paths."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Cpp


def test_cpp_json_type_structurally_renders_terminator_key() -> None:
    r"""Structural JSON rendering does not use a raw-string delimiter."""
    result = literalize(
        source='{")json": "x"}',
        input_format=InputFormat.JSON,
        language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert result.code == (
        'auto my_data = nlohmann::json::object({{")json", "x"}});'
    )
