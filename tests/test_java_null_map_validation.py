"""Focused Java validation tests for null-valued maps."""

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.languages import Java


def _record_java() -> Language:
    """Return Java configured for record rendering."""
    return Java(
        heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
        sequence_format=Java.sequence_formats.ARRAY,
    )


def test_record_strategy_allows_null_inside_nested_record() -> None:
    """A record field may be null even when nested in an ordered map."""
    result = literalize(
        source="!!omap\n- outer:\n  - name: null\n    id: 1\n",
        input_format=InputFormat.YAML,
        language=_record_java(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert 'Map.entry("outer", new Object[]{new Record0(null, 1)})' in (
        result.code
    )


def test_java_terminator_precedes_trailing_comments() -> None:
    """A trailing Java comment remains after the statement terminator."""
    rendered = Java().format_variable_declaration(
        "my_data",
        "42\n// note",
        42,
        frozenset(),
    )

    assert rendered == "var my_data = 42;\n// note"
