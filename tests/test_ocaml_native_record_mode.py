"""Public API coverage for opt-in concrete OCaml records."""

import pytest

from literalizer import (
    CollectionLayout,
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
from literalizer.languages import OCaml


def _record_spec() -> Language:
    """Return an OCaml specification with concrete records."""
    return OCaml(dict_format=OCaml.dict_formats.RECORD)


def test_record_mode_preserves_generic_default() -> None:
    """The generic value union remains the default representation."""
    source = '{"name":"Ada","active":true,"scores":[1,2,3]}'
    default = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=OCaml(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_record_spec(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "type val_t =" in default.code
    assert "type val_t =" not in native.code
    assert "type val_t0 =" in native.code
    assert "name : string" in native.code
    assert "active : bool" in native.code
    assert "scores : int list" in native.code
    assert 'name = "Ada"' in native.code


@pytest.mark.parametrize(
    argnames=("source", "input_format", "message"),
    argvalues=[
        ('{"bad-key":1}', InputFormat.JSON, "field"),
        ('{"let":1}', InputFormat.JSON, "field"),
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
    """Unsupported values fail before invalid OCaml is produced."""
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
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "type val_t0" in result.code
    assert "type val_t1" in result.code
    assert "type val_t2" in result.code
    assert "members : val_t2 list" in result.code
    assert "OMap" not in result.code


def test_record_mode_compact_uses_semicolons() -> None:
    """Compact records use OCaml separators rather than commas."""
    result = literalize(
        source='[{"name":"Ada","active":true}]',
        input_format=InputFormat.JSON,
        language=_record_spec(),
        collection_layout=CollectionLayout.COMPACT,
    )
    assert 'name = "Ada"; active = true' in result.code
    assert 'name = "Ada",' not in result.code


def test_record_mode_rejects_invalid_type_name() -> None:
    """Generated type names must be valid lowercase OCaml names."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="type_name"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=OCaml(
                dict_format=OCaml.dict_formats.RECORD,
                type_name="Invalid",
            ),
        )


def test_record_mode_temporal_string_formats() -> None:
    """Native record fields use strings for configured ISO dates."""
    result = literalize(
        source=(
            "birthday = 2024-01-15\n"
            "moment = 2024-01-15T12:30:00Z\n"
            "at = 09:30:00\n"
        ),
        input_format=InputFormat.TOML,
        language=OCaml(
            dict_format=OCaml.dict_formats.RECORD,
            date_format=OCaml.date_formats.ISO,
            datetime_format=OCaml.datetime_formats.ISO,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "birthday : string" in result.code
    assert "moment : string" in result.code
    assert "at : string" in result.code


def test_record_mode_epoch_datetime() -> None:
    """Epoch datetime values use a concrete int field."""
    result = literalize(
        source="moment = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=OCaml(
            dict_format=OCaml.dict_formats.RECORD,
            datetime_format=OCaml.datetime_formats.EPOCH,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "moment : int" in result.code


def test_record_mode_conflicts_with_json_value() -> None:
    """The JSON value backend and records are distinct output modes."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="json_type"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=OCaml(
                dict_format=OCaml.dict_formats.RECORD,
                json_type=OCaml.json_types.YOJSON_SAFE_T,
            ),
        )


def test_record_mode_conflicts_with_array_sequences() -> None:
    """Array sequences do not have the requested list field types."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="LIST"
    ):
        _ = literalize(
            source='{"x":[1]}',
            input_format=InputFormat.JSON,
            language=OCaml(
                dict_format=OCaml.dict_formats.RECORD,
                sequence_format=OCaml.sequence_formats.ARRAY,
            ),
        )


def test_record_mode_rejects_call_stubs() -> None:
    """Call stubs cannot assume the generic val_t type in record mode."""
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
