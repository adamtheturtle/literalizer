"""Java declaration termination checks."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Java


def test_java_declaration_terminates_after_trailing_comment() -> None:
    """The semicolon follows a collection carrying a trailing comment."""
    result = literalize(
        source="a: 1\n# trailing\n",
        input_format=InputFormat.YAML,
        language=Java(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert result.code.endswith("// trailing\n);")
