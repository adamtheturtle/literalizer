"""Focused C++ scalar-string declaration tests."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Cpp


def test_cpp_nul_scalar_uses_value_type() -> None:
    """A NUL-safe ``std::string`` expression cannot initialize a
    pointer.
    """
    result = literalize(
        source='"\\u0000x"',
        input_format=InputFormat.JSON,
        language=Cpp(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert result.code == 'auto my_data = std::string{""} + \'\\0\' + "x";'
