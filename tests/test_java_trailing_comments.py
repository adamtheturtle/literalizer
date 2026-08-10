"""Java declaration termination checks."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Java
from literalizer.languages.java import _format_java_var_declaration


def test_java_declaration_terminates_after_trailing_comment() -> None:
    """The semicolon follows a collection carrying a trailing comment."""
    result = literalize(
        source="a: 1\n# trailing\n",
        input_format=InputFormat.YAML,
        language=Java(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert result.code.endswith("// trailing\n);")


def test_java_var_declaration_terminates_before_trailing_comment() -> None:
    """The declaration formatter keeps a final comment after its semicolon."""
    result = _format_java_var_declaration(
        name="my_data",
        value="List.of(1)\n// trailing",
        _data=[1],
        _modifiers=frozenset(),
    )

    assert result == "var my_data = List.of(1);\n// trailing"
