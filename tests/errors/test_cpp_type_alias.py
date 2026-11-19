"""Validation for C++ type alias rendering."""

import pytest

from literalizer import InputFormat
from literalizer.languages import Python
from literalizer.languages.cpp import literalize_cpp_type_alias


def test_cpp_type_alias_requires_a_cpp_language() -> None:
    """Reject a language other than C++ before rendering the alias."""
    with pytest.raises(
        expected_exception=TypeError,
        match="type alias rendering requires",
    ):
        _ = literalize_cpp_type_alias(
            language=Python(),
            name="Example",
            source="1",
            input_format=InputFormat.JSON,
        )
