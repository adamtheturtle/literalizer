"""Java record-strategy validation around ordered maps."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Java


def test_ordered_map_allows_null_inside_nested_record() -> None:
    """Only direct Map.entry values reject null record fields."""
    result = literalize(
        source="!!omap\n- outer:\n  - name: null\n    id: 1\n",
        input_format=InputFormat.YAML,
        language=Java(
            heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
            sequence_format=Java.sequence_formats.ARRAY,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert 'Map.entry("outer", new Object[]{new Record0(null, 1)})' in (
        result.code
    )
