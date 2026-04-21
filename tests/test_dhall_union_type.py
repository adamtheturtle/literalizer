"""Unit tests for Dhall's union-type heterogeneous-value strategy.

Golden-file coverage for the main rendering paths lives in
``tests/integration/cases/*/Dhall_heterogeneous_strategy_union_type*.dhall``.
These unit tests cover the behaviors that don't fit the golden-file
workflow: error-raising on the default strategy, configurable union
name, and the homogeneous-input no-op.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
)
from literalizer.languages import Dhall

_TAGGED = Dhall(
    heterogeneous_strategy=Dhall.heterogeneous_strategies.UNION_TYPE,
)


def test_default_strategy_is_error() -> None:
    """Default Dhall spec still raises on heterogeneous scalars."""
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source='{"a": 1, "b": "x"}',
            input_format=InputFormat.JSON,
            language=Dhall(),
        )


def test_sibling_lists_still_error_without_opt_in() -> None:
    """Default Dhall spec raises ``HeterogeneousSiblingListsError`` for
    sibling-list heterogeneity.
    """
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source='[[1, 2], ["a", "b"]]',
            input_format=InputFormat.JSON,
            language=Dhall(),
        )


def test_configurable_union_name() -> None:
    """The emitted union name comes from the
    ``heterogeneous_value_union_name`` constructor argument.
    """
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=Dhall(
            heterogeneous_strategy=Dhall.heterogeneous_strategies.UNION_TYPE,
            heterogeneous_value_union_name="MyUnion",
        ),
        wrap_in_file=True,
    )
    expected = (
        "let MyUnion = < Int : Integer | Str : Text > in\n"
        "{\n"
        "  a = MyUnion.Int +1,\n"
        '  b = MyUnion.Str "x",\n'
        "}"
    )
    assert result.code == expected


def test_homogeneous_data_emits_no_union() -> None:
    """Opting into the union-type strategy is a no-op when the data
    contains no heterogeneous collections.
    """
    result = literalize(
        source='{"a": 1, "b": 2}',
        input_format=InputFormat.JSON,
        language=_TAGGED,
        wrap_in_file=True,
    )
    expected = "{\n  a = +1,\n  b = +2,\n}"
    assert result.code == expected
