"""Rejection of sibling maps with incompatible inferred value types."""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import HeterogeneousSiblingMapsError
from literalizer.languages import Rust, V


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_typed_sibling_maps_reject_different_value_types(
    language: Language,
) -> None:
    """Narrow map types must agree across one enclosing list slot."""
    with pytest.raises(expected_exception=HeterogeneousSiblingMapsError):
        literalize(
            source='[{"s": "y"}, {"t": 3}]',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_typed_sibling_maps_allow_same_value_type(language: Language) -> None:
    """Different keys do not matter when every map value type agrees."""
    for source in ('[{"s": 1}, {"t": 3}]', '[{"m": {}}, {"m": {}}]'):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )
