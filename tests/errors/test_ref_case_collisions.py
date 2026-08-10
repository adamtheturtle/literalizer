"""Ref identifier case-conversion collision errors."""

import pytest

from literalizer import (
    IdentifierCase,
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Python

_COLLIDING_REFS = '{"a": {"$ref": "userId"}, "b": {"$ref": "user_id"}}'


def test_literalize_rejects_ref_case_collision() -> None:
    """Whole-value refs retain distinct identifiers after conversion."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=("identifier 'user_id' collides with ref name 'userId'"),
    ):
        literalize(
            source=_COLLIDING_REFS,
            input_format=InputFormat.JSON,
            language=Python(),
            ref_case=IdentifierCase.SNAKE,
        )


def test_literalize_call_rejects_nested_ref_case_collision() -> None:
    """Call arguments apply the same injectivity check."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot convert ref name 'user_id' to SNAKE",
    ):
        literalize_call(
            source=f"[{_COLLIDING_REFS}]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="consume",
            parameter_names=("value",),
            ref_case=IdentifierCase.SNAKE,
        )


def test_repeated_source_ref_name_remains_valid() -> None:
    """Repeated uses of one source name are not a collision."""
    result = literalize(
        source='[{"$ref": "userId"}, {"$ref": "userId"}]',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_case=IdentifierCase.SNAKE,
    )

    expected_occurrences = 2
    assert result.code.count("user_id") == expected_occurrences
