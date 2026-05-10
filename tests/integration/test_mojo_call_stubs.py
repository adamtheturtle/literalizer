"""Targeted Mojo call-stub tests.

Covers branches in ``_mojo_typed_param_list`` and
``_mojo_call_preamble_stub`` that the integration golden files no
longer exercise once cross-call type divergence skips under the
default ``ERROR`` heterogeneous_strategy.
"""

from typing import TYPE_CHECKING, cast

import pytest

from literalizer._language import StubReturn
from literalizer.exceptions import HeterogeneousScalarCollectionError
from literalizer.languages.mojo import Mojo

if TYPE_CHECKING:
    from collections.abc import Sequence

    from literalizer._types import Value


def test_typed_stub_falls_back_for_null_value() -> None:
    """A ``None`` slot value has no Mojo type, so the stub falls back
    to the generic ``[*Ts: AnyType](*args: *Ts)`` form regardless of
    the heterogeneous strategy.
    """
    mojo = Mojo()
    result = mojo.format_call_preamble_stub(
        ["process"],
        ["value"],
        StubReturn.VOID,
        [None],
    )
    assert result == ("def process[*Ts: AnyType](*args: *Ts):\n    pass",)


def test_typed_stub_raises_on_scalar_divergence_under_error() -> None:
    """Cross-call scalar-type divergence raises under ``ERROR``.

    ``arg_values`` carries one per-call slot list per element; passing
    ``[["hello"], [42]]`` represents two single-argument calls whose
    slot-0 types disagree.
    """
    mojo = Mojo()
    scalar_divergence = cast("Sequence[Value]", [["hello"], [42]])
    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError,
        match=r"diverge across calls at parameter 'value'",
    ):
        mojo.format_call_preamble_stub(
            ["process"],
            ["value"],
            StubReturn.VOID,
            scalar_divergence,
        )


def test_typed_stub_raises_on_shape_divergence_under_error() -> None:
    """Scalar at one call and a list at another counts as divergence."""
    mojo = Mojo()
    shape_divergence = cast("Sequence[Value]", [[1], [[1, 2, 3]]])
    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError,
        match=r"diverge across calls at parameter 'data'",
    ):
        mojo.format_call_preamble_stub(
            ["process"],
            ["data"],
            StubReturn.VOID,
            shape_divergence,
        )


def test_typed_stub_raises_on_list_element_divergence_under_error() -> None:
    """Lists with disagreeing element types across calls raise."""
    mojo = Mojo()
    list_divergence = cast("Sequence[Value]", [[[1, 2, 3]], [["a", "b"]]])
    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError,
        match=r"diverge across calls at parameter 'data'",
    ):
        mojo.format_call_preamble_stub(
            ["process"],
            ["data"],
            StubReturn.VOID,
            list_divergence,
        )


def test_typed_stub_falls_back_under_variant_for_divergence() -> None:
    """Cross-call divergence under ``VARIANT`` falls back to the generic
    stub pending the cross-call wrap machinery in a follow-up slice.
    """
    variant = next(
        s for s in Mojo().heterogeneous_strategies if s.name == "VARIANT"
    )
    mojo = Mojo(heterogeneous_strategy=variant)
    scalar_divergence = cast("Sequence[Value]", [["hello"], [42]])
    result = mojo.format_call_preamble_stub(
        ["process"],
        ["value"],
        StubReturn.VOID,
        scalar_divergence,
    )
    assert result == ("def process[*Ts: AnyType](*args: *Ts):\n    pass",)


def test_dotted_method_generic_stub_for_untypable_value() -> None:
    """A dotted-method stub falls back to the generic form when the
    slot has a value with no Mojo type, exercising the multi-part
    generic branches of ``_mojo_call_preamble_stub``.
    """
    mojo = Mojo()
    result = mojo.format_call_preamble_stub(
        ["app", "client", "fetch"],
        ["payload"],
        StubReturn.VOID,
        [None],
    )
    expected = (
        "@fieldwise_init\nstruct _ClientType(Copyable, Movable):\n"
        "    def fetch[*Ts: AnyType](self, *args: *Ts):\n"
        "        pass\n"
        "@fieldwise_init\nstruct _AppType(Copyable, Movable):\n"
        "    var client: _ClientType",
    )
    assert result == expected


def test_deep_dotted_method_generic_stub_for_untypable_value() -> None:
    """A 4-part dotted-method stub exercises the inner-fields loop in
    ``_mojo_call_preamble_stub`` (the path between the innermost type
    and the root type).
    """
    mojo = Mojo()
    result = mojo.format_call_preamble_stub(
        ["obj", "api", "client", "post"],
        ["data"],
        StubReturn.VOID,
        [None],
    )
    expected = (
        "@fieldwise_init\nstruct _ClientType(Copyable, Movable):\n"
        "    def post[*Ts: AnyType](self, *args: *Ts):\n"
        "        pass\n"
        "@fieldwise_init\nstruct _ApiType(Copyable, Movable):\n"
        "    var client: _ClientType\n"
        "@fieldwise_init\nstruct _ObjType(Copyable, Movable):\n"
        "    var api: _ApiType",
    )
    assert result == expected
