"""Unit tests for shared integer-width element-type inference."""

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer._formatters.type_inference import (
    BeyondI64,
    DictType,
    WideInt,
    infer_element_type,
    int_widening_tier,
)

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


def test_infer_element_type_widens_past_i32() -> None:
    """A homogeneous int list with a value past i32 becomes WideInt."""
    assert infer_element_type(items=[1, 1099511627776]) is WideInt


def test_infer_element_type_widens_past_i64() -> None:
    """A homogeneous int list with a value past i64 becomes BeyondI64."""
    assert (
        infer_element_type(
            items=[9223372036854775807, 9223372036854775808],
        )
        is BeyondI64
    )


def test_infer_element_type_beyond_i64_beats_wide_int() -> None:
    """BeyondI64 takes precedence when both widening tiers apply."""
    assert infer_element_type(items=[1, 9223372036854775808]) is BeyondI64


def test_infer_element_type_dict_values_use_same_join() -> None:
    """Map values use the same integer least-upper-bound as list
    elements.
    """
    mapping: dict[Scalar, Value] = {"a": 1, "b": 1099511627776}
    items: list[Value] = [mapping]
    inferred = infer_element_type(items=items)
    assert isinstance(inferred, DictType)
    assert inferred.value_type is WideInt


def test_int_widening_tier_empty_and_non_int() -> None:
    """Empty or mixed collections do not report a widening tier."""
    assert int_widening_tier(items=[]) is None
    assert int_widening_tier(items=[1, "x"]) is None
    assert int_widening_tier(items=[True, 1]) is None


def test_int_widening_tier_magnitude_boundaries() -> None:
    """Homogeneous int collections report WideInt or BeyondI64."""
    assert int_widening_tier(items=[1, 2, 3]) is None
    assert int_widening_tier(items=[1, 1099511627776]) is WideInt
    assert int_widening_tier(items=[1, 9223372036854775808]) is BeyondI64
    assert (
        int_widening_tier(
            items=[1099511627776, 9223372036854775808],
        )
        is BeyondI64
    )


def test_infer_element_type_skips_bool_when_widening_ints() -> None:
    """Bools are not ints for widening; a bool+int list stays mixed."""
    assert infer_element_type(items=[True, 1]) is None
