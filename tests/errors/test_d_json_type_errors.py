"""D ``json_type=None`` (narrow-typed) rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import D


def _narrow_literalize(source: str) -> None:
    """Render *source* under D narrow-typed mode for a rejection test."""
    literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=D(json_type=None),
        variable_form=NewVariable(name="my_data"),
    )


def test_d_narrow_rejects_heterogeneous_list() -> None:
    """A mixed scalar list has no common D element type."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="narrow-typed",
    ):
        _narrow_literalize(source='[1, "two"]')


def test_d_narrow_rejects_heterogeneous_dict_values() -> None:
    """A dict whose values mix types has no common D AA value type."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="narrow-typed",
    ):
        _narrow_literalize(source='{"a": 1, "b": "two"}')


def test_d_narrow_rejects_empty_list() -> None:
    """D's ``auto`` cannot infer an element type for ``[]``."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="narrow-typed",
    ):
        _narrow_literalize(source="[]")


def test_d_narrow_rejects_empty_dict() -> None:
    """D's ``auto`` cannot infer a value type for ``[:]``."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="narrow-typed",
    ):
        _narrow_literalize(source="{}")


def test_d_narrow_rejects_record_strategy() -> None:
    """Narrow and ``RECORD`` cannot be combined."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="mutually exclusive",
    ):
        D(
            json_type=None,
            heterogeneous_strategy=D.heterogeneous_strategies.RECORD,
        )
