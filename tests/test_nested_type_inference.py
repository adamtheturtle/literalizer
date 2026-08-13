"""Focused tests for recursive homogeneous collection inference."""

from typing import TYPE_CHECKING

from literalizer._formatters.type_inference import (
    BeyondI64,
    ListType,
    MixedNumeric,
    WideInt,
    infer_element_type,
)

if TYPE_CHECKING:
    from literalizer._types import Value


def test_nested_lists_unify_integer_widths() -> None:
    """Sibling inner lists share the widest integer type."""
    narrow: list[Value] = [1]
    wide: list[Value] = [2**40]
    values: list[Value] = [narrow, wide]
    assert infer_element_type(items=values) == ListType(inner=WideInt)


def test_nested_lists_unify_mixed_numeric_types() -> None:
    """Sibling inner lists preserve numeric compatibility recursively."""
    integers: list[Value] = [1]
    floats: list[Value] = [2.5]
    values: list[Value] = [integers, floats]
    assert infer_element_type(items=values) == ListType(inner=MixedNumeric)


def test_nested_lists_unify_beyond_i64_widths() -> None:
    """The widest integer tier wins recursively."""
    narrow: list[Value] = [1]
    beyond_i64: list[Value] = [2**70]
    values: list[Value] = [narrow, beyond_i64]
    assert infer_element_type(items=values) == ListType(inner=BeyondI64)
