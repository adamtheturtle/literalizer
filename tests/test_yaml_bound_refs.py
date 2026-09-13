"""Public YAML rendering behavior for bound references."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


def test_bound_ref_in_ordered_map_preserves_mapping_kind() -> None:
    """Replacing a marker must not demote its ordered-map parent."""
    result = literalize(
        source="!!omap\n- value:\n    $ref: bound\n",
        input_format=InputFormat.YAML,
        language=Python(),
        variable_form=NewVariable(name="out", modifiers=frozenset()),
        wrap_in_file=True,
        bound_refs={"bound": 2},
        ref_key="$ref",
    )

    assert result.code == (
        "from collections import OrderedDict\n"
        "bound = 2\n"
        "out = OrderedDict([\n"
        '    ("value", bound),\n'
        "])"
    )


def test_integer_bound_ref_widens_with_literal_float_sibling() -> None:
    """A bound declaration must use the numeric type required at its
    use.
    """
    result = literalize(
        source='[{"$ref": "integer"}, 1.5]',
        input_format=InputFormat.JSON,
        language=Python(),
        bound_refs={"integer": 1},
        ref_key="$ref",
        variable_form=NewVariable(name="out", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert result.code.startswith("integer = 1.0\n")
