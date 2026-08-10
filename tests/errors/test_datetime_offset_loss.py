"""Errors for native datetime formats that cannot retain UTC offsets."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp, Kotlin, Rust


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
