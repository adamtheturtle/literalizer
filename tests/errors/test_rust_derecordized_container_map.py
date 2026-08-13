"""Rejection of Rust widened record maps with container values."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Rust


def test_record_strategy_rejects_widened_map_container_values() -> None:
    """Rust RECORD raises instead of naming an unusable value enum."""
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="values contain containers",
    ):
        literalize(
            source='[{"m":{"x":[1,2]}},{"m":{"y":{"k":1}}}]',
            input_format=InputFormat.JSON,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )
