"""Tests for precedence between bound refs and explicit ref values."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import V


def test_explicit_ref_value_wins_when_bound_refs_are_wrapped() -> None:
    """File wrapping preserves the caller's explicit ref type intent."""
    variable_form = NewVariable(
        name="y",
        modifiers=frozenset(),
    )

    unwrapped = literalize(
        source='{"$ref": "x"}',
        input_format=InputFormat.JSON,
        language=V(),
        ref_key="$ref",
        ref_values={"x": 1},
        bound_refs={"x": [1, 2]},
        variable_form=variable_form,
        wrap_in_file=False,
    )
    wrapped = literalize(
        source='{"$ref": "x"}',
        input_format=InputFormat.JSON,
        language=V(),
        ref_key="$ref",
        ref_values={"x": 1},
        bound_refs={"x": [1, 2]},
        variable_form=variable_form,
        wrap_in_file=True,
    )

    assert unwrapped.declaration_code == "y := x"
    assert "y := x\n" in wrapped.declaration_code
    assert "y := x.clone()" not in wrapped.declaration_code
