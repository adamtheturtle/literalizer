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


def test_record_mode_preserves_generic_default() -> None:
    """The default Val union remains available for dynamic values."""
    source = '{"name":"Ada","active":true,"scores":[1,2,3]}'
    default = literalize(
        source=source, input_format=InputFormat.JSON, language=Haskell()
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_record_spec(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "data Val =" in default.code
    assert "data Val =" not in native.code
    assert "data Val0 = Val0" in native.code
    assert "name :: String" in native.code
    assert "active :: Bool" in native.code
    assert "scores :: [Integer]" in native.code
    assert 'name = "Ada"' in native.code


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"bad-key":1}', InputFormat.JSON, "field"),
        ('{"case":1}', InputFormat.JSON, "field"),
        ("1: one\n", InputFormat.YAML, "field"),
        ("{}", InputFormat.JSON, "empty records"),
        ('{"x":null}', InputFormat.JSON, "NoneType"),
        ('{"x":[]}', InputFormat.JSON, "empty list"),
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


def test_record_mode_nested_shapes() -> None:
    """Nested records and sibling lists get concrete declarations."""
    result = literalize(
        source='{"owner":{"name":"Ada"},"members":[{"name":"Ada","score":1.5},{"name":"Bob","score":2.5}]}',
        input_format=InputFormat.JSON,
        language=_record_spec(),
    )
    assert "data Val0" in result.code
    assert "data Val1" in result.code
    assert "data Val2" in result.code
    assert "members :: [Val" in result.code
    assert "HMap" not in result.code


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


def test_record_mode_temporal_string_formats() -> None:
    """Native record fields use strings for configured ISO dates."""
    result = literalize(
        source=(
            "birthday = 2024-01-15\n"
            "when = 2024-01-15T12:30:00Z\n"
            "at = 09:30:00\n"
        ),
        input_format=InputFormat.TOML,
        language=Haskell(
            dict_format=Haskell.dict_formats.RECORD,
            date_format=Haskell.date_formats.ISO,
            datetime_format=Haskell.datetime_formats.ISO,
        ),
    )
    assert "birthday :: String" in result.code
    assert "when :: String" in result.code
    assert "at :: String" in result.code


def test_record_mode_epoch_datetime() -> None:
    """Epoch datetime values use a concrete Integer field."""
    result = literalize(
        source="when = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=Haskell(
            dict_format=Haskell.dict_formats.RECORD,
            datetime_format=Haskell.datetime_formats.EPOCH,
        ),
    )
    assert "when :: Integer" in result.code


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
