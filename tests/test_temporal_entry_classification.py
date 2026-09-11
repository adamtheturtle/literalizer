"""Tests for temporal entry classification from format metadata."""

import datetime

from literalizer.languages import C, Fortran, FSharp, OCaml, Sml

_DATETIME = datetime.datetime(
    year=2024,
    month=1,
    day=2,
    hour=3,
    minute=4,
    second=5,
    tzinfo=datetime.UTC,
)
_DATE = _DATETIME.date()


def test_c_datetime_entry_uses_configured_output_type() -> None:
    """C does not infer the union field from rendered text."""
    iso = C(datetime_format=C.datetime_formats.ISO)
    epoch = C(datetime_format=C.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123") == "((CVal){.s = 123})"
    assert (
        epoch.format_sequence_entry(_DATETIME, '"not an integer"')
        == '((CVal){.i = "not an integer"})'
    )


def test_fortran_datetime_entry_uses_configured_output_type() -> None:
    """Fortran does not infer the wrapper from rendered text."""
    iso = Fortran(datetime_format=Fortran.datetime_formats.ISO)
    epoch = Fortran(datetime_format=Fortran.datetime_formats.EPOCH)

    assert iso.format_sequence_entry(_DATETIME, "123_int64") == (
        "fstr(123_int64)"
    )
    assert (
        epoch.format_sequence_entry(_DATETIME, '"not an integer"')
        == 'fint("not an integer")'
    )


def test_fsharp_temporal_entries_use_configured_output_types() -> None:
    """F# tags dates and datetimes from format metadata."""
    iso = FSharp(
        date_format=FSharp.date_formats.ISO,
        datetime_format=FSharp.datetime_formats.ISO,
    )
    native = FSharp(
        date_format=FSharp.date_formats.FSHARP,
        datetime_format=FSharp.datetime_formats.FSHARP,
    )

    assert iso.format_sequence_entry(_DATE, "System.DateOnly(...)") == (
        "FStr System.DateOnly(...)"
    )
    assert iso.format_sequence_entry(_DATETIME, "System.DateTime(...)") == (
        "FStr System.DateTime(...)"
    )
    assert native.format_sequence_entry(_DATE, '"string-looking"') == (
        'FDate ("string-looking")'
    )
    assert native.format_sequence_entry(_DATETIME, '"string-looking"') == (
        'FDatetime ("string-looking")'
    )


def test_ocaml_temporal_entries_use_configured_output_types() -> None:
    """OCaml tags dates and datetimes from format metadata."""
    iso = OCaml(
        date_format=OCaml.date_formats.ISO,
        datetime_format=OCaml.datetime_formats.ISO,
    )
    native = OCaml(
        date_format=OCaml.date_formats.OCAML,
        datetime_format=OCaml.datetime_formats.OCAML,
    )

    assert iso.format_sequence_entry(_DATE, "not quoted") == "OStr not quoted"
    assert iso.format_sequence_entry(_DATETIME, "123") == "OStr 123"
    assert native.format_sequence_entry(_DATE, '"string-looking"') == (
        '"string-looking"'
    )
    assert native.format_sequence_entry(_DATETIME, '"string-looking"') == (
        '"string-looking"'
    )


def test_sml_temporal_entries_use_configured_output_types() -> None:
    """SML tags dates and datetimes from format metadata."""
    iso = Sml(
        date_format=Sml.date_formats.ISO,
        datetime_format=Sml.datetime_formats.ISO,
    )
    native = Sml(
        date_format=Sml.date_formats.SML,
        datetime_format=Sml.datetime_formats.SML,
    )

    assert iso.format_sequence_entry(_DATE, "not quoted") == "SStr not quoted"
    assert iso.format_sequence_entry(_DATETIME, "123") == "SStr 123"
    assert native.format_sequence_entry(_DATE, '"string-looking"') == (
        '"string-looking"'
    )
    assert native.format_sequence_entry(_DATETIME, '"string-looking"') == (
        '"string-looking"'
    )
