"""Date and datetime formatting functions."""

import datetime
import math
from collections.abc import Callable

from beartype import beartype


@beartype
def format_date_iso(value: datetime.date) -> str:
    """Format a date as an ISO 8601 quoted string literal.

    Example: ``datetime.date(2024, 1, 15)`` -> ``"2024-01-15"``.
    """
    return f'"{value.isoformat()}"'


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
    """Format a time as an F# ``TimeOnly(...)`` expression."""
    return f"TimeOnly({_time_only_args(value=value)})"


@beartype
def format_time_vb(value: datetime.time) -> str:
    """Format a time as a VB.NET ``New TimeOnly(...)`` expression."""
    return f"New TimeOnly({_time_only_args(value=value)})"


@beartype
def datetime_epoch_seconds(value: datetime.datetime) -> int:
    """Return integer Unix epoch seconds for a datetime."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.UTC)
    return math.floor(value.timestamp())


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


@beartype
def _format_datetime_ymdhms(value: datetime.datetime, template: str) -> str:
    """Format a datetime using a year/month/day/hour/minute/second
    template.
    """
    return template.format(
        year=value.year,
        month=value.month,
        day=value.day,
        hour=value.hour,
        minute=value.minute,
        second=value.second,
    )


@beartype
def datetime_ymdhms_formatter(
    *,
    template: str,
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that substitutes year, month, day,
    hour, minute, and second into *template*.

    The *template* must contain ``{year}``, ``{month}``, ``{day}``,
    ``{hour}``, ``{minute}``, and ``{second}`` placeholders.

    Example::

        fmt = datetime_ymdhms_formatter(
            template="new DateTime({year}, {month}, {day}, "
                     "{hour}, {minute}, {second})",
        )
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _format_datetime_ymdhms(value=value, template=template)

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
