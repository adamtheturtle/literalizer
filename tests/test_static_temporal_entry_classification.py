"""Tests for formerly static temporal entry formatters."""

import datetime

from literalizer.languages import Ada, Forth, ObjectiveC, Occam, SystemVerilog

_DATETIME = datetime.datetime(
    year=2024,
    month=1,
    day=2,
    hour=3,
    minute=4,
    second=5,
    tzinfo=datetime.UTC,
)


def test_ada_datetime_entry_uses_configured_output_type() -> None:
    """Ada does not infer the union constructor from rendered text."""
    iso = Ada(datetime_format=Ada.datetime_formats.ISO)
    epoch = Ada(datetime_format=Ada.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == "AStr (123)"
    assert epoch.format_sequence_entry(_DATETIME, '"text"') == 'AInt ("text")'


def test_forth_datetime_marker_uses_configured_output_type() -> None:
    """Forth does not infer the visitor marker from rendered text."""
    iso = Forth(datetime_format=Forth.datetime_formats.ISO)
    epoch = Forth(datetime_format=Forth.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == "123 +str"
    assert epoch.format_sequence_entry(_DATETIME, 's\\" text"') == (
        's\\" text" +int'
    )


def test_objective_c_datetime_entry_uses_configured_output_type() -> None:
    """Objective-C decides whether to box from format metadata."""
    iso = ObjectiveC(datetime_format=ObjectiveC.datetime_formats.ISO)
    epoch = ObjectiveC(datetime_format=ObjectiveC.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == "123"
    assert epoch.format_sequence_entry(_DATETIME, '"text"') == '@("text")'


def test_occam_datetime_entry_uses_configured_output_type() -> None:
    """Occam does not infer the union constructor from rendered text."""
    iso = Occam(datetime_format=Occam.datetime_formats.ISO)
    epoch = Occam(datetime_format=Occam.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == (
        "MOBILE LIT(lit.str; MOBILE []BYTE 123)"
    )
    assert epoch.format_sequence_entry(_DATETIME, '"text"') == (
        'MOBILE LIT(lit.int; "text")'
    )


def test_systemverilog_datetime_entry_uses_configured_output_type() -> None:
    """SystemVerilog does not infer the value tag from rendered text."""
    iso = SystemVerilog(datetime_format=SystemVerilog.datetime_formats.ISO)
    epoch = SystemVerilog(datetime_format=SystemVerilog.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == (
        "_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: 123}"
    )
    assert epoch.format_sequence_entry(_DATETIME, '"text"') == (
        '_VVal\'{tag: _VVAL_INT, i: "text", r: 0.0, s: ""}'
    )
