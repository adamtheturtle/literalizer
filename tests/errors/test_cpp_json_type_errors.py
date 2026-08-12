"""C++ ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp


def test_cpp_json_type_rejects_integer_beyond_finite_numeric_range() -> None:
    """A finite integer must not silently become JSON infinity."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="magnitude exceeds nlohmann::json's finite numeric range",
    ):
        literalize(
            source=f"{{\"value\": {10**400}}}",
            input_format=InputFormat.JSON,
            language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
