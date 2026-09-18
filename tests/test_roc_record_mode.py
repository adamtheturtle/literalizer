"""Input boundaries for the opt-in native Roc record format."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Roc


@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        ('{"not-a-field": 1}', InputFormat.JSON),
        ('{"if": 1}', InputFormat.JSON),
        ('{"outer": {"Bad": 1}}', InputFormat.JSON),
        ("1: one\n", InputFormat.YAML),
    ],
)
def test_record_mode_rejects_non_field_keys(
    source: str, input_format: InputFormat
) -> None:
    """Never emit a syntactically invalid Roc record field."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="field"
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=Roc(dict_format=Roc.dict_formats.RECORD),
        )


def test_default_mode_preserves_arbitrary_string_keys() -> None:
    """Native records do not narrow the pre-existing tagged mode."""
    result = literalize(
        source='{"not-a-field": 1}',
        input_format=InputFormat.JSON,
        language=Roc(),
    )
    assert '("not-a-field", RInt 1i128)' in result.code


def test_record_mode_rejects_conflicting_list_field_types() -> None:
    """A Roc list cannot mix records with conflicting field types."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="uniform record list types",
    ):
        _ = literalize(
            source='[{"x": 1}, {"x": "a"}]',
            input_format=InputFormat.JSON,
            language=Roc(dict_format=Roc.dict_formats.RECORD),
        )


@pytest.mark.parametrize(
    argnames=("source", "expected"),
    argvalues=[
        ("--- !!omap\n- a: 1\n", "ordered maps"),
        (
            "---\n- x: !!set\n    a:\n- x: !!set\n    b:\n",
            "sets",
        ),
    ],
)
def test_record_mode_rejects_non_record_collections(
    source: str, expected: str
) -> None:
    """Ordered maps and sets retain the default tagged representation."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=expected
    ):
        _ = literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=Roc(dict_format=Roc.dict_formats.RECORD),
        )


def test_record_mode_formats_epoch_datetime() -> None:
    """The epoch option keeps its integer value without a tag."""
    result = literalize(
        source="event_time = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=Roc(
            dict_format=Roc.dict_formats.RECORD,
            datetime_format=Roc.datetime_formats.EPOCH,
        ),
    )
    assert "event_time: 1705321800i128" in result.code
