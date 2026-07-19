"""Rejection of out-of-range integers on 64-bit-only languages (#2713).

Languages whose widest built-in integer type cannot hold the input
value raise :class:`~literalizer.exceptions.UnrepresentableIntegerError`
at literalize time rather than emit a literal the target compiler will
either silently truncate or reject.  The golden-file harness only
exercises output that runs, so the raise-paths past every language's
fallback boundary need direct pytest coverage.
"""

import json

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Cpp, D, Go, Rust, TypeScript, V, Zig

_BEYOND_U64 = 2**64
_BEYOND_NEG_I64 = -(2**63) - 1
_BEYOND_SAFE_INT = 2**53
_BEYOND_I128 = 2**127

_NO_BIGINT_MSG = r" without external arbitrary-precision integer support\.$"
_UNSIGNED_FALLBACK_MSG = (
    r" below the signed 64-bit range using an unsigned fallback\.$"
)
_ABOVE_U64_MSG = r" above the unsigned 64-bit range\.$"


def _literalize_scalar(language: Language, value: int) -> None:
    """Literalize *value* under *language*, discarding the result."""
    literalize(
        source=json.dumps(obj=value),
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="x", modifiers=frozenset()),
    )


def _literalize_list(language: Language, values: list[int]) -> None:
    """Literalize *values* as a list under *language*, discarding it."""
    literalize(
        source=json.dumps(obj=values),
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="x", modifiers=frozenset()),
    )


def test_go_raises_above_unsigned_64_bit_range() -> None:
    """Go has no native literal for values above ``math.MaxUint64``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^Go cannot represent integer \d+" + _ABOVE_U64_MSG,
    ):
        _literalize_scalar(language=Go(), value=_BEYOND_U64)


@pytest.mark.parametrize(argnames="language", argvalues=[V(), Zig()])
def test_v_and_zig_raise_above_unsigned_64_bit_range(
    language: Language,
) -> None:
    """Neither target has a native integer type wider than ``u64``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=(r"^(?:V|Zig) cannot represent integer \d+" + _ABOVE_U64_MSG),
    ):
        _literalize_scalar(language=language, value=_BEYOND_U64)


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        V(),
        Zig(),
    ],
    ids=["v", "zig_zval"],
)
def test_v_and_zig_containers_raise_above_unsigned_64_bit_range(
    language: Language,
) -> None:
    """Integer members cannot overflow V/Zig collection or record
    types.
    """
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=(r"^(?:V|Zig) cannot represent integer \d+" + _ABOVE_U64_MSG),
    ):
        _literalize_list(language=language, values=[_BEYOND_U64])


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        V(heterogeneous_strategy=V.heterogeneous_strategies.RECORD),
        Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
    ],
    ids=["v", "zig"],
)
def test_v_and_zig_record_fields_raise_above_unsigned_64_bit_range(
    language: Language,
) -> None:
    """Record field literals cannot overflow their inferred ``u64``
    type.
    """
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=(r"^(?:V|Zig) cannot represent integer \d+" + _ABOVE_U64_MSG),
    ):
        literalize(
            source=json.dumps(obj={"value": _BEYOND_U64}),
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="x", modifiers=frozenset()),
        )


def test_go_raises_for_in_range_negative_in_uint64_collection() -> None:
    """A ``BeyondI64`` collection opens as ``[]uint64``, so an in-range
    negative sibling that renders fine as a scalar cannot be represented
    inside the unsigned element type.
    """
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^Go cannot represent negative integer -\d+"
        + _UNSIGNED_FALLBACK_MSG,
    ):
        _literalize_list(language=Go(), values=[2**63, -5])


def test_cpp_raises_above_unsigned_64_bit_range() -> None:
    """C++ has no native literal for values above ``ULLONG_MAX``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^C\+\+ cannot represent integer \d+" + _ABOVE_U64_MSG,
    ):
        _literalize_scalar(language=Cpp(), value=_BEYOND_U64)


def test_cpp_raises_below_signed_64_bit_range() -> None:
    """C++'s unsigned fallback rejects negatives past ``LLONG_MIN``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^C\+\+ cannot represent negative integer -\d+"
        + _UNSIGNED_FALLBACK_MSG,
    ):
        _literalize_scalar(language=Cpp(), value=_BEYOND_NEG_I64)


def test_d_raises_above_unsigned_64_bit_range() -> None:
    """D has no native literal for values above the unsigned 64-bit
    max.
    """
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^D cannot represent integer \d+" + _ABOVE_U64_MSG,
    ):
        _literalize_scalar(language=D(), value=_BEYOND_U64)


def test_d_raises_below_signed_64_bit_range() -> None:
    """D's unsigned fallback rejects negatives past ``long.min``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^D cannot represent negative integer -\d+"
        + _UNSIGNED_FALLBACK_MSG,
    ):
        _literalize_scalar(language=D(), value=_BEYOND_NEG_I64)


def test_typescript_raises_above_safe_integer() -> None:
    """JavaScript ``number`` precision tops out at ``2**53 - 1``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^TypeScript cannot represent integer \d+" + _NO_BIGINT_MSG,
    ):
        _literalize_scalar(language=TypeScript(), value=_BEYOND_SAFE_INT)


def test_typescript_raises_below_negative_safe_integer() -> None:
    """JavaScript ``number`` precision tops out at ``-(2**53 - 1)``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^TypeScript cannot represent integer -\d+" + _NO_BIGINT_MSG,
    ):
        _literalize_scalar(language=TypeScript(), value=-_BEYOND_SAFE_INT)


def test_rust_raises_above_i128_range() -> None:
    """Rust's widest native integer type is ``i128``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^Rust cannot represent integer \d+" + _NO_BIGINT_MSG,
    ):
        _literalize_scalar(language=Rust(), value=_BEYOND_I128)


def test_rust_raises_below_i128_range() -> None:
    """Rust's widest native integer type is ``i128``."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=r"^Rust cannot represent integer -\d+" + _NO_BIGINT_MSG,
    ):
        _literalize_scalar(language=Rust(), value=-_BEYOND_I128 - 1)
