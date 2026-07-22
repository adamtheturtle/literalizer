"""Tests for replacing null values in record fields."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


def test_record_null_substitutions_recurse_through_ordered_maps() -> None:
    """Nested records in ordered maps receive configured replacements."""
    result = literalize(
        source="""!!omap
- outer:
  - replacement: null
    present: 1
""",
        input_format=InputFormat.YAML,
        language=Python(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        record_null_substitutions={"replacement": -1},
    )

    assert result.code == (
        "my_data = OrderedDict([\n"
        '    ("outer", ({"replacement": -1, "present": 1},)),\n'
        "])"
    )
