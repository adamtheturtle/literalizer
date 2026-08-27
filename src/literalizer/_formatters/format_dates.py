"""Date and datetime formatting functions."""

import datetime
from collections.abc import Callable

from beartype import beartype

from literalizer.exceptions import UnrepresentableInputError


@beartype
def normalize_datetime_utc(
    value: datetime.datetime, *, language_name: str
) -> datetime.datetime:
    """Normalize an aware datetime or raise a typed representation
    error.
    """
    try:
        return value.astimezone(tz=datetime.UTC)
    except OverflowError as error:
        msg = (
            f"{language_name} cannot normalize datetime to UTC within "
            f"Python's supported year range: {value.isoformat()}"
        )
        raise UnrepresentableInputError(msg) from error


@beartype
def format_date_iso(value: datetime.date) -> str:
    """Format a date as an ISO 8601 quoted string literal.

    Example: ``datetime.date(2024, 1, 15)`` -> ``"2024-01-15"``.
    """
    return f'"{value.isoformat()}"'


@beartype
def format_date_javascript(value: datetime.date) -> str:
    """Format a date as a JavaScript local-midnight ``Date``.

    The numeric constructor uses local calendar components. Its month is
    zero-based, unlike :class:`datetime.date`.
    """
    return f"new Date({value.year}, {value.month - 1}, {value.day})"


@beartype
def format_datetime_javascript(value: datetime.datetime) -> str:
    """Format an exactly representable JavaScript ``Date``.

    Naive values use the numeric constructor so their calendar components do
    not get parsed as an environment-dependent instant. Aware values retain
    their explicit ISO offset. JavaScript ``Date`` has millisecond precision.
    """
    if value.microsecond % 1000:
        msg = (
            "JavaScript Date cannot preserve sub-millisecond datetime "
            f"precision: {value.isoformat()}"
        )
        raise UnrepresentableInputError(msg)
    if value.utcoffset() is not None:
        return f'new Date("{value.isoformat(timespec="milliseconds")}")'
    args = (
        f"{value.year}, {value.month - 1}, {value.day}, {value.hour}, "
        f"{value.minute}, {value.second}"
    )
    if value.microsecond:
        args += f", {value.microsecond // 1000}"
    return f"new Date({args})"


@beartype
def format_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as an ISO 8601 quoted string literal.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` ->
    ``"2024-01-15T12:30:00"``.
    """
    return f'"{value.isoformat()}"'


@beartype
def format_time_iso(value: datetime.time) -> str:
    """Format a time as an ISO 8601 quoted string literal.

    Example: ``datetime.time(9, 30)`` -> ``"09:30:00"``.
    """
    return f'"{value.isoformat()}"'


@beartype
def format_time_local_time_of(value: datetime.time) -> str:
    """Format a time as a ``LocalTime.of(...)`` call.

    Shared by Java, Kotlin, Scala, and Groovy, which all use the
    ``java.time.LocalTime`` factory method.

    Example: ``datetime.time(9, 30)`` -> ``LocalTime.of(9, 30)``.
    """
    parts = [str(object=value.hour), str(object=value.minute)]
    nanoseconds = value.microsecond * 1000
    if value.second or nanoseconds:
        parts.append(str(object=value.second))
    if nanoseconds:
        parts.append(str(object=nanoseconds))
    return f"LocalTime.of({', '.join(parts)})"


@beartype
def _time_only_args(value: datetime.time) -> str:
    """Return the comma-separated argument list for a ``TimeOnly``
    call.
    """
    parts = [
        str(object=value.hour),
        str(object=value.minute),
        str(object=value.second),
    ]
    if value.microsecond:
        milliseconds, microseconds = divmod(value.microsecond, 1000)
        parts.append(str(object=milliseconds))
        if microseconds:
            parts.append(str(object=microseconds))
    return ", ".join(parts)


@beartype
def format_time_csharp(value: datetime.time) -> str:
    """Format a time as a C# ``new TimeOnly(...)`` expression."""
    return f"new TimeOnly({_time_only_args(value=value)})"


@beartype
def format_time_fsharp(value: datetime.time) -> str:
    """Format a time as an F# ``System.TimeOnly(...)`` expression.

    Fully qualifies ``System.TimeOnly`` so the rendered output does not
    require an ``open System`` preamble; an ``open`` directive would
    sort before ``module``, which F# rejects.
    """
    return f"System.TimeOnly({_time_only_args(value=value)})"


@beartype
def format_time_vb(value: datetime.time) -> str:
    """Format a time as a VB.NET ``New TimeOnly(...)`` expression."""
    return f"New TimeOnly({_time_only_args(value=value)})"


@beartype
def datetime_epoch_seconds(value: datetime.datetime) -> int:
    """Return exact integer Unix epoch seconds for a datetime."""
    if value.microsecond:
        msg = (
            "integer Unix epoch seconds cannot preserve fractional "
            f"datetime precision: {value.isoformat()}"
        )
        raise UnrepresentableInputError(msg)
    offset = value.utcoffset() or datetime.timedelta()
    elapsed = datetime.timedelta(
        days=value.toordinal()
        - datetime.date(year=1970, month=1, day=1).toordinal(),
        seconds=value.hour * 3600 + value.minute * 60 + value.second,
        microseconds=value.microsecond,
    )
    return (elapsed - offset) // datetime.timedelta(seconds=1)


@beartype
def format_datetime_epoch_fractional(value: datetime.datetime) -> str:
    """Format exact Unix epoch seconds, retaining a fractional part."""
    offset = value.utcoffset() or datetime.timedelta()
    elapsed = datetime.timedelta(
        days=value.toordinal()
        - datetime.date(year=1970, month=1, day=1).toordinal(),
        seconds=value.hour * 3600 + value.minute * 60 + value.second,
        microseconds=value.microsecond,
    )
    total_microseconds = (elapsed - offset) // datetime.timedelta(
        microseconds=1
    )
    sign = "-" if total_microseconds < 0 else ""
    seconds, microseconds = divmod(abs(total_microseconds), 1_000_000)
    if not microseconds:
        return f"{sign}{seconds}"
    fraction = f"{microseconds:06d}".rstrip("0")
    return f"{sign}{seconds}.{fraction}"


@beartype
def format_datetime_epoch(value: datetime.datetime) -> str:
    """Format a datetime as integer Unix epoch seconds."""
    return str(object=datetime_epoch_seconds(value=value))


@beartype
def datetime_epoch_formatter(
    *,
    format_integer: Callable[[int], str],
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that delegates epoch seconds to an
    integer formatter.
    """

    def _format(value: datetime.datetime) -> str:
        """Format using the supplied integer formatter."""
        return format_integer(datetime_epoch_seconds(value=value))

    return _format


@beartype
def _format_date_ymd(value: datetime.date, template: str) -> str:
    """Format a date using a year/month/day template."""
    return template.format(
        year=value.year,
        month=value.month,
        day=value.day,
    )


@beartype
def date_ymd_formatter(
    *,
    template: str,
) -> Callable[[datetime.date], str]:
    """Return a date formatter that substitutes year, month, and day
    into *template*.

    The *template* must contain ``{year}``, ``{month}``, and ``{day}``
    placeholders.

    Example::

        fmt = date_ymd_formatter(
            template="LocalDate.of({year}, {month}, {day})",
        )
        fmt(datetime.date(2024, 1, 15))  # => "LocalDate.of(2024, 1, 15)"
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _format_date_ymd(value=value, template=template)

    return _format


_MICROSECONDS_PER_MILLISECOND = 1000


@beartype
def _format_datetime_ymdhms(
    value: datetime.datetime,
    template: str,
    millisecond_template: str | None,
) -> str:
    """Format a datetime using a year/month/day/hour/minute/second
    template.

    A target whose native type carries milliseconds supplies a second
    template taking a ``{millisecond}`` placeholder; it is used only
    for a value that has one, so a whole-second value keeps the
    shorter spelling (issue #4521).
    """
    if millisecond_template is None:
        if value.microsecond:
            msg = (
                "whole-second native datetime format cannot preserve "
                f"microseconds: {value.isoformat()}"
            )
            raise UnrepresentableInputError(msg)
    elif value.microsecond % _MICROSECONDS_PER_MILLISECOND:
        msg = (
            "millisecond-precision native datetime format cannot "
            f"preserve sub-millisecond precision: {value.isoformat()}"
        )
        raise UnrepresentableInputError(msg)
    if value.utcoffset() is not None:
        msg = (
            "timezone-naive native datetime format cannot preserve "
            f"timezone awareness: {value.isoformat()}"
        )
        raise UnrepresentableInputError(msg)
    selected = (
        millisecond_template
        if millisecond_template is not None and value.microsecond
        else template
    )
    return selected.format(
        year=value.year,
        month=value.month,
        day=value.day,
        hour=value.hour,
        minute=value.minute,
        second=value.second,
        millisecond=value.microsecond // _MICROSECONDS_PER_MILLISECOND,
    )


@beartype
def datetime_ymdhms_formatter(
    *,
    template: str,
    millisecond_template: str | None,
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that substitutes year, month, day,
    hour, minute, and second into *template*.

    The *template* must contain ``{year}``, ``{month}``, ``{day}``,
    ``{hour}``, ``{minute}``, and ``{second}`` placeholders.

    *millisecond_template* is that template plus a ``{millisecond}``
    placeholder, for a target whose native datetime type carries
    milliseconds; ``None`` means the target is whole-second and any
    fraction is refused.

    Example::

        fmt = datetime_ymdhms_formatter(
            template="new DateTime({year}, {month}, {day}, "
                     "{hour}, {minute}, {second})",
            millisecond_template=None,
        )
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _format_datetime_ymdhms(
            value=value,
            template=template,
            millisecond_template=millisecond_template,
        )

    return _format


@beartype
def _format_date_iso_template(value: datetime.date, template: str) -> str:
    """Format a date using the ISO template."""
    return template.format(iso=value.isoformat())


@beartype
def date_iso_formatter(
    *,
    template: str,
) -> Callable[[datetime.date], str]:
    """Return a date formatter that substitutes the ISO 8601 string
    into *template*.

    The *template* must contain an ``{iso}`` placeholder.

    Example::

        fmt = date_iso_formatter(
            template='DateTime.parse("{iso}")',
        )
        fmt(datetime.date(2024, 1, 15))  # => 'DateTime.parse("2024-01-15")'
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _format_date_iso_template(value=value, template=template)

    return _format


@beartype
def _format_datetime_iso_template(
    value: datetime.datetime, template: str
) -> str:
    """Format a datetime using the ISO template."""
    return template.format(iso=value.isoformat())


@beartype
def datetime_iso_formatter(
    *,
    template: str,
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that substitutes the ISO 8601 string
    into *template*.

    The *template* must contain an ``{iso}`` placeholder.

    Example::

        fmt = datetime_iso_formatter(
            template='new Date("{iso}")',
        )
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _format_datetime_iso_template(value=value, template=template)

    return _format
