"""Errors for native datetime formats that cannot retain UTC offsets."""

import datetime

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp, Kotlin, Rust
from literalizer.languages.rust import (
    _rust_scalar_type,  # pyright: ignore[reportPrivateUsage]
)


@pytest.mark.parametrize(
    argnames="language", argvalues=[CSharp(), Kotlin(), Rust()]
)
def test_native_datetime_rejects_offset_loss(language: Language) -> None:
    """Native naive-datetime output must not silently discard an
    offset.
    """
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="native datetime format cannot preserve UTC offset",
    ):
        literalize(
            source="value: 2024-01-02 03:04:05 -05:00",
            input_format=InputFormat.YAML,
            language=language,
        )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        CSharp(datetime_format=CSharp.datetime_formats.ISO),
        Kotlin(datetime_format=Kotlin.datetime_formats.ISO),
        Rust(datetime_format=Rust.datetime_formats.ISO),
    ],
)
def test_iso_datetime_preserves_offset(language: Language) -> None:
    """The explicitly selected ISO format remains available for
    offsets.
    """
    result = literalize(
        source="value: 2024-01-02 03:04:05 -05:00",
        input_format=InputFormat.YAML,
        language=language,
    )

    assert "-05:00" in result.code


def test_native_datetime_rejects_offset_loss_in_dict_key() -> None:
    """Timezone-aware mapping keys are validated like values."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="native datetime format cannot preserve UTC offset",
    ):
        literalize(
            source="2024-01-02 03:04:05 -05:00: value",
            input_format=InputFormat.YAML,
            language=Rust(),
        )


def test_rust_record_type_retains_native_naive_datetime_type() -> None:
    """Naive native datetimes still receive their configured type."""
    assert (
        _rust_scalar_type(
            data=datetime.datetime(  # noqa: DTZ001
                year=2024,
                month=1,
                day=2,
                hour=3,
                minute=4,
            ),
            date_type="NaiveDate",
            datetime_type="NaiveDateTime",
        )
        == "NaiveDateTime"
    )
