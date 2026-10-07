"""Public API coverage for opt-in Standard ML records."""

import pytest

from literalizer import (
    InputFormat,
    Language,
    literalize,
)
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Sml


def _record_spec() -> Language:
    """Return an SML specification using native records."""
    return Sml(dict_format=Sml.dict_formats.RECORD)


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"bad-key":1}', InputFormat.JSON, "field"),
        ('{"val":1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x":null}', InputFormat.JSON, "NoneType"),
        ('[{"x":1},{"x":"one"}]', InputFormat.JSON, "uniform"),
        ('[{"x":1},{"y":1}]', InputFormat.JSON, "uniform"),
        ('[1,"one"]', InputFormat.JSON, "uniform"),
        ('{"x":2147483648}', InputFormat.JSON, "32-bit"),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Unsupported shapes fail before invalid SML is emitted."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=_record_spec(),
        )


def test_record_mode_rejects_mismatched_nested_list_fields() -> None:
    """Sibling records with different list element types cannot unify."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="uniform"
    ):
        _ = literalize(
            source='[{"scores":[1]},{"scores":["one"]}]',
            input_format=InputFormat.JSON,
            language=_record_spec(),
        )


def test_record_mode_rejects_wide_epoch() -> None:
    """An epoch beyond native int range fails before SML compilation."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="32-bit epoch"
    ):
        _ = literalize(
            source="when: 2040-01-01T00:00:00Z\n",
            input_format=InputFormat.YAML,
            language=Sml(
                dict_format=Sml.dict_formats.RECORD,
                datetime_format=Sml.datetime_formats.EPOCH,
            ),
        )
