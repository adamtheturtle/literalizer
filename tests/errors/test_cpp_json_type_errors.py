"""C++ ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp
from literalizer.languages.cpp import _nlohmann_json_expression


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


def test_cpp_json_type_rejects_integer_beyond_finite_numeric_range() -> None:
    """A finite integer must not silently become JSON infinity."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="magnitude exceeds nlohmann::json's finite numeric range",
    ):
        _nlohmann_json_expression(data=10**400)
