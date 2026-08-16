"""Focused coverage for scalar temporal rendering branches."""

import datetime

from literalizer._checks import (
    _format_scalar_identity,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.languages import Python
from literalizer.languages.csharp import (
    _csharp_scalar_type,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.languages.erlang import (
    _format_string_otp_json,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.languages.occam import (
    _format_occam_entry,  # pyright: ignore[reportPrivateUsage]
)


def test_scalar_identity_formats_null_and_time() -> None:
    """Collection identity delegates null and time to their formatters."""
    spec = Python()

    assert _format_scalar_identity(value=None, spec=spec) == "None"
    assert (
        _format_scalar_identity(
            value=datetime.time(hour=1, minute=2), spec=spec
        )
        == "datetime.time(hour=1, minute=2, second=0)"
    )


def test_csharp_scalar_datetime_type_hint() -> None:
    """C# datetime inference selects the datetime hint."""
    value = datetime.datetime(  # noqa: DTZ001 - deliberately naive
        year=2024, month=1, day=1
    )

    assert (
        _csharp_scalar_type(
            value=value, date_hint="DateOnly", datetime_hint="DateTime"
        )
        == "DateTime"
    )


def test_erlang_json_noncharacters_use_codepoint_segments() -> None:
    """Erlang JSON strings escape illegal source non-characters."""
    assert (
        _format_string_otp_json(value="a\ufffe") == "<<97/utf8, 65534/utf8>>"
    )


def test_occam_epoch_datetime_uses_integer_literal() -> None:
    """Occam wraps integer epoch datetimes as integer variants."""
    value = datetime.datetime(  # noqa: DTZ001 - representation is irrelevant
        year=2024, month=1, day=1
    )

    assert (
        _format_occam_entry(original=value, formatted="1")
        == "MOBILE LIT(lit.int; 1)"
    )
