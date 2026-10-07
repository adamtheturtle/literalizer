"""Public API coverage for opt-in Standard ML records."""

import pytest

from literalizer import (
    InputFormat,
    Language,
    literalize,
    literalize_call,
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


def test_record_mode_call_uses_native_argument() -> None:
    """Call arguments use the same native representation."""
    result = literalize_call(
        source='[{"name":"Ada"}]',
        input_format=InputFormat.JSON,
        language=_record_spec(),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert 'name = "Ada"' in result.code
    assert "SMap" not in result.code


def test_record_mode_curried_call_uses_native_argument() -> None:
    """Curried calls parenthesize a record argument without tagging it."""
    result = literalize_call(
        source='[{"name":"Ada"}]',
        input_format=InputFormat.JSON,
        language=Sml(
            dict_format=Sml.dict_formats.RECORD,
            call_style=Sml.call_styles.CURRIED,
        ),
        target_function="consume",
        parameter_names=("item",),
        wrap_in_file=True,
    )
    assert "consume (" in result.code
    assert 'name = "Ada"' in result.code


def test_record_mode_epoch_uses_sml_negation() -> None:
    """A pre-1970 epoch keeps SML's tilde negation syntax."""
    result = literalize(
        source="when: 1969-12-31T23:59:59Z\n",
        input_format=InputFormat.YAML,
        language=Sml(
            dict_format=Sml.dict_formats.RECORD,
            datetime_format=Sml.datetime_formats.EPOCH,
        ),
    )
    assert "when = ~1" in result.code


def test_record_mode_positive_epoch() -> None:
    """Positive epoch timestamps remain ordinary SML integers."""
    result = literalize(
        source="when: 1970-01-01T00:00:01Z\n",
        input_format=InputFormat.YAML,
        language=Sml(
            dict_format=Sml.dict_formats.RECORD,
            datetime_format=Sml.datetime_formats.EPOCH,
        ),
    )
    assert "when = 1" in result.code


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
