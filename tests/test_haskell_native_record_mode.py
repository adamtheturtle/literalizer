"""Public API coverage for opt-in concrete Haskell records."""

import pytest

from literalizer import (
    InputFormat,
    Language,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)
from literalizer.languages import Haskell


def _record_spec() -> Language:
    """Return a Haskell specification with concrete records."""
    return Haskell(dict_format=Haskell.dict_formats.RECORD)


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"bad-key":1}', InputFormat.JSON, "field"),
        ('{"case":1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x":null}', InputFormat.JSON, "NoneType"),
        ('{"x":[]}', InputFormat.JSON, "empty list"),
        (
            '{"x":[[{"y":1}]]}',
            InputFormat.JSON,
            "^Haskell record mode cannot type dict$",
        ),
        ("--- !!omap\n- a: 1\n", InputFormat.YAML, "ordered maps"),
        ("--- !!set\na:\n", InputFormat.YAML, "set"),
    ],
)
def test_record_mode_rejects_unsupported_input(
    source: str, input_format: InputFormat, message: str
) -> None:
    """Unsupported values fail before invalid Haskell is produced."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=message
    ):
        _ = literalize(
            source=source,
            input_format=input_format,
            language=_record_spec(),
        )


def test_record_mode_rejects_variable_field_collision() -> None:
    """A top-level binding cannot reuse a generated field selector."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="variable name",
    ):
        _ = literalize(
            source='{"my_data":1}',
            input_format=InputFormat.JSON,
            language=_record_spec(),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )


def test_record_mode_rejects_invalid_type_name() -> None:
    """Generated type constructors need an uppercase Haskell name."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="type_name"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=Haskell(
                dict_format=Haskell.dict_formats.RECORD,
                type_name="lowercase",
            ),
        )


def test_record_mode_conflicts_with_aeson() -> None:
    """The JSON value backend and records are distinct output modes."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="json_type"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=Haskell(
                dict_format=Haskell.dict_formats.RECORD,
                json_type=Haskell.json_types.AESON_VALUE,
            ),
        )


def test_record_mode_conflicts_with_tuple_sequences() -> None:
    """Tuple sequences do not have a uniform list field type."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="LIST"
    ):
        _ = literalize(
            source='{"x":[1]}',
            input_format=InputFormat.JSON,
            language=Haskell(
                dict_format=Haskell.dict_formats.RECORD,
                sequence_format=Haskell.sequence_formats.TUPLE,
            ),
        )


def test_record_mode_rejects_call_stubs() -> None:
    """Call stubs cannot assume the generic Val type in record mode."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="call stub"
    ):
        _ = literalize_call(
            source='[{"x":1}]',
            input_format=InputFormat.JSON,
            language=_record_spec(),
            target_function="consume",
            parameter_names=("item",),
            wrap_in_file=True,
        )
