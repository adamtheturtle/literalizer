"""C++ ``json_type`` rejection paths."""

import pytest

from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages.cpp import _nlohmann_json_expression


def test_cpp_json_type_rejects_integer_beyond_finite_numeric_range() -> None:
    """A finite integer must not silently become JSON infinity."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="magnitude exceeds nlohmann::json's finite numeric range",
    ):
        _nlohmann_json_expression(data=10**400)
