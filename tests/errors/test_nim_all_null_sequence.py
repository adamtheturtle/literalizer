"""Rejection of all-null native Nim sequences lacking an element type."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Nim


def test_record_strategy_rejects_top_level_all_null_sequence() -> None:
    """Nim RECORD raises instead of emitting ``@[nil, nil]``."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.RECORD,
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot infer an element type",
    ):
        literalize(
            source="[null, null]",
            input_format=InputFormat.JSON,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )
