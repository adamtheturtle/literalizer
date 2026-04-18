"""Integer formatting functions."""

from collections.abc import Callable

from beartype import beartype

from literalizer._types import Value
from literalizer.exceptions import UnrepresentableIntegerError


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
def _format_integer_grouped(value: int, *, separator: str) -> str:
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
def make_long_suffix_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter so its output gets an ``L`` suffix.

    Example: ``100`` → ``"100L"``, ``-10`` → ``"-10L"``.
    """

    @beartype
    def _format(value: int) -> str:
        """Format with ``L`` suffix."""
        return f"{base(value)}L"

    return _format


@beartype
def make_int64_cast_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter so its output is cast to ``int64``.

    Example: ``100`` → ``"int64(100)"``.
    """

    @beartype
    def _format(value: int) -> str:
        """Format with ``int64()`` cast."""
        return f"int64({base(value)})"

    return _format


I32_MAX = 2**31 - 1
I32_MIN = -(2**31)
I64_MAX = 2**63 - 1
I64_MIN = -(2**63)


@beartype
def make_overflow_fallback_formatter(
    *,
    base: Callable[[int], str],
    fallback: Callable[[int], str],
    min_value: int = I64_MIN,
    max_value: int = I64_MAX,
) -> Callable[[int], str]:
    """Wrap a formatter so values outside ``[min_value, max_value]`` use
    *fallback* instead of *base*.

    Defaults to the signed 64-bit range.  Used by language backends
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
    ``UnrepresentableIntegerError``.

    Used by backends whose fixed-width integer types cannot hold values
    outside the signed 64-bit range and which have no built-in
    arbitrary-precision alternative available to the lint toolchain.
    The integration test catches this error and skips the case for
    that language.
    """

    @beartype
    def _format(value: int) -> str:
        """Raise ``UnrepresentableIntegerError`` for any value."""
        msg = (
            f"{language_name} cannot represent integer {value} without "
            "external bignum support."
        )
        raise UnrepresentableIntegerError(msg)

    return _format


@beartype
def data_has_out_of_range_int(*, data: Value) -> bool:
    """Return ``True`` if *data* contains an integer outside i64 range.

    Recurses into lists, sets, and dict values.  Used by languages that
    need to add a preamble (e.g. an ``import`` statement) conditionally
    on the presence of a very large integer scalar.
    """
    if isinstance(data, bool):
        return False
    if isinstance(data, int):
        return not I64_MIN <= data <= I64_MAX
    if isinstance(data, list):
        return any(data_has_out_of_range_int(data=v) for v in data)
    if isinstance(data, set):
        return any(data_has_out_of_range_int(data=v) for v in data)
    if isinstance(data, dict):
        return any(data_has_out_of_range_int(data=v) for v in data.values())
    return False
