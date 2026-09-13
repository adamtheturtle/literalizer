"""Sibling maps whose value types agree.

The rejections are declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the acceptance side --
which no rejection manifest expresses.
"""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.languages import Rust, V


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_typed_sibling_maps_allow_same_value_type(language: Language) -> None:
    """Different keys do not matter when every map value type agrees."""
    for source in ('[{"s": 1}, {"t": 3}]', '[{"m": {}}, {"m": {}}]'):
        _ = literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )
