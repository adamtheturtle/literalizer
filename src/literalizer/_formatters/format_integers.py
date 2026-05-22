"""Integer formatting functions."""

from collections.abc import Callable

from beartype import beartype

from literalizer._types import Value
from literalizer.exceptions import UnrepresentableIntegerError

I64_MAX = 2**63 - 1
I64_MIN = -(2**63)


@beartype
def _format_with_base(*, value: int, prefix: str, fmt: str) -> str:
    """Format an integer with a base prefix.

    Negative values are formatted with a leading ``-``.
    """
    if value < 0:
        return f"-{prefix}{abs(value):{fmt}}"
    return f"{prefix}{value:{fmt}}"


@beartype
def format_integer_hex(value: int) -> str:
    """Format an integer as a hexadecimal literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"0xff"``, ``-10`` -> ``"-0xa"``.
    """
    return _format_with_base(value=value, prefix="0x", fmt="x")


@beartype
def format_integer_octal(value: int) -> str:
    """Format an integer as an octal literal with ``0o`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"0o377"``, ``-10`` -> ``"-0o12"``.
    """
    return _format_with_base(value=value, prefix="0o", fmt="o")


@beartype
def format_integer_octal_c_style(value: int) -> str:
    """Format an integer as a C-style octal literal with ``0`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"0377"``, ``-10`` -> ``"-012"``.
    """
    # "00" is technically valid octal, but "0" is the conventional
    # representation of zero in C-family languages.
    if value == 0:
        return "0"
    return _format_with_base(value=value, prefix="0", fmt="o")


@beartype
def format_integer_binary(value: int) -> str:
    """Format an integer as a binary literal with ``0b`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"0b11111111"``, ``-10`` -> ``"-0b1010"``.
    """
    return _format_with_base(value=value, prefix="0b", fmt="b")


@beartype
def format_integer_hex_erlang(value: int) -> str:
    """Format an integer as an Erlang hexadecimal literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"16#FF"``, ``-10`` -> ``"-16#A"``.
    """
    return _format_with_base(value=value, prefix="16#", fmt="X")


@beartype
def format_integer_binary_erlang(value: int) -> str:
    """Format an integer as an Erlang binary literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` -> ``"2#11111111"``, ``-10`` -> ``"-2#1010"``.
    """
    return _format_with_base(value=value, prefix="2#", fmt="b")


@beartype
def _format_integer_grouped(*, value: int, separator: str) -> str:
    """Format an integer with digit-group separators every 3 digits.

    Example: ``_format_integer_grouped(1000000, separator="_")``
    -> ``"1_000_000"``.
    """
    s = str(object=abs(value))
    group_size = 3
    groups: list[str] = []
    while len(s) > group_size:
        groups.append(s[-group_size:])
        s = s[:-group_size]
    groups.append(s)
    formatted = separator.join(reversed(groups))
    if value < 0:
        return f"-{formatted}"
    return formatted


@beartype
def format_integer_underscore(value: int) -> str:
    """Format an integer with underscore separators every 3 digits.

    Example: ``1000000`` -> ``"1_000_000"``.
    """
    return _format_integer_grouped(value=value, separator="_")


@beartype
def format_integer_tick(value: int) -> str:
    """Format an integer with tick (apostrophe) separators every 3 digits.

    Used by C++ digit separators.

    Example: ``1000000`` -> ``"1'000'000"``.
    """
    return _format_integer_grouped(value=value, separator="'")


@beartype
def _format_long_suffix(value: int, base: Callable[[int], str]) -> str:
    """Format with ``L`` suffix."""
    return f"{base(value)}L"


@beartype
def make_long_suffix_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter so its output gets an ``L`` suffix.

    Example: ``100`` → ``"100L"``, ``-10`` → ``"-10L"``.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _format_long_suffix(value=value, base=base)

    return _format


@beartype
def _format_overflow_suffix(
    value: int,
    base: Callable[[int], str],
    min_value: int,
    max_value: int,
    suffix: str,
) -> str:
    """Format, appending *suffix* when out of range."""
    formatted = base(value)
    if min_value <= value <= max_value:
        return formatted
    return f"{formatted}{suffix}"


@beartype
def make_overflow_suffix_formatter(
    *,
    base: Callable[[int], str],
    min_value: int,
    max_value: int,
    suffix: str,
) -> Callable[[int], str]:
    """Wrap a formatter to append *suffix* when the value is outside
    ``[min_value, max_value]``.

    This is used by languages where the default integer literal type
    is 32-bit and a wider-type suffix (``L``, ``i64``) is required for
    values that overflow 32-bit signed range.

    Example with ``suffix="L"`` and i32 bounds: ``42`` → ``"42"``,
    ``2147483648`` → ``"2147483648L"``.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _format_overflow_suffix(
            value=value,
            base=base,
            min_value=min_value,
            max_value=max_value,
            suffix=suffix,
        )

    return _format


@beartype
def _format_int64_cast(value: int, base: Callable[[int], str]) -> str:
    """Format with ``int64()`` cast."""
    return f"int64({base(value)})"


@beartype
def make_int64_cast_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter so its output is cast to ``int64``.

    Example: ``100`` → ``"int64(100)"``.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _format_int64_cast(value=value, base=base)

    return _format


@beartype
def make_overflow_fallback_formatter(
    *,
    base: Callable[[int], str],
    fallback: Callable[[int], str],
    min_value: int = I64_MIN,
    max_value: int = I64_MAX,
) -> Callable[[int], str]:
    """Wrap a formatter so values outside ``[min_value, max_value]``
    delegate to *fallback* instead of *base*.

    Defaults to the signed 64-bit range.  Used by language specifications
    whose scalar integer code path can't emit a bare decimal literal
    for values that exceed native fixed-width integer ranges.
    """

    @beartype
    def _format(value: int) -> str:
        """Format, delegating to *fallback* when out of range."""
        if min_value <= value <= max_value:
            return base(value)
        return fallback(value)

    return _format


@beartype
def raise_for_unrepresentable_int(
    *,
    language_name: str,
) -> Callable[[int], str]:
    """Return a fallback formatter that raises
    ``UnrepresentableIntegerError`` for any value.

    Used by languages whose fixed-width integer types cannot hold
    values outside the signed 64-bit range and which have no built-in
    arbitrary-precision integer type available to the per-language
    lint pipeline.
    """

    @beartype
    def _format(value: int) -> str:
        """Raise ``UnrepresentableIntegerError``."""
        msg = (
            f"{language_name} cannot represent integer {value} without "
            "external arbitrary-precision integer support."
        )
        raise UnrepresentableIntegerError(msg)

    return _format


@beartype
def make_unsigned_overflow_fallback(
    *,
    format_positive: Callable[[int], str],
    language_name: str,
) -> Callable[[int], str]:
    """Wrap a positive-only unsigned-literal formatter so negative
    out-of-range values raise ``UnrepresentableIntegerError``.

    Languages whose overflow fallback produces an unsigned 64-bit
    literal cannot represent values below ``-2^63``: the signed range
    lower bound excludes them and the unsigned range starts at zero.
    """

    @beartype
    def _format(value: int) -> str:
        """Delegate to *format_positive*, raising for negatives."""
        if value < 0:
            msg = (
                f"{language_name} cannot represent negative integer "
                f"{value} below the signed 64-bit range using an "
                "unsigned fallback."
            )
            raise UnrepresentableIntegerError(msg)
        return format_positive(value)

    return _format


@beartype
def _format_positive_ull(value: int) -> str:
    """Format a non-negative integer with a ``ULL`` suffix."""
    return f"{value}ULL"


@beartype
def make_ull_fallback(
    *,
    language_name: str,
) -> Callable[[int], str]:
    """Return a fallback that formats positive overflow values with a
    ``ULL`` suffix and raises for negative overflow.

    Shared by C and C++ where signed 64-bit literals are rejected above
    ``LLONG_MAX`` and ``unsigned long long`` holds positive values up to
    ``ULLONG_MAX``.
    """
    return make_unsigned_overflow_fallback(
        format_positive=_format_positive_ull,
        language_name=language_name,
    )


@beartype
def data_has_out_of_range_int(*, data: Value) -> bool:
    """Return ``True`` if *data* contains an integer outside i64 range.

    Descends into lists, sets, and dict values.  Used by languages that
    need to add a preamble (e.g. an ``import`` statement) conditionally
    on the presence of a very large integer scalar.
    """
    return data_has_int_outside_range(
        data=data, min_value=I64_MIN, max_value=I64_MAX
    )


@beartype
def data_has_int_outside_range(
    *, data: Value, min_value: int, max_value: int
) -> bool:
    """Return ``True`` if *data* contains an integer outside
    ``[min_value, max_value]``.

    Descends into lists, sets, and dict values.  Used by languages that
    need to add a preamble (e.g. an ``import`` statement) conditionally
    on the presence of an integer whose magnitude exceeds the language's
    native fixed-precision range.
    """
    match data:
        case bool():
            return False
        case int():
            return not min_value <= data <= max_value
        case list():
            return any(
                data_has_int_outside_range(
                    data=v, min_value=min_value, max_value=max_value
                )
                for v in data
            )
        case set():
            return any(
                data_has_int_outside_range(
                    data=v, min_value=min_value, max_value=max_value
                )
                for v in data
            )
        case dict():
            return any(
                data_has_int_outside_range(
                    data=v, min_value=min_value, max_value=max_value
                )
                for v in data.values()
            )
        case _:
            return False
