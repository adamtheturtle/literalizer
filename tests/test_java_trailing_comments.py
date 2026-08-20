"""Java formatter behavior without a parser-backed golden surface."""

from literalizer.languages import Java


def test_java_terminator_precedes_trailing_comments() -> None:
    """A trailing Java comment remains after the statement terminator.

    This directly exercises an already-rendered value fragment; input parsing
    separates comments before the variable formatter sees them, so a TOML
    golden case cannot reach this formatter branch.
    """
    rendered = Java().format_variable_declaration(
        "my_data",
        "42\n// note",
        42,
        frozenset(),
    )

    assert rendered == "var my_data = 42;\n// note"
