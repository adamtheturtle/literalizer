"""Public API coverage for opt-in concrete Gleam records."""

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
from literalizer.languages import Gleam


def _record_spec() -> Language:
    """Return a Gleam specification with concrete records."""
    return Gleam(dict_format=Gleam.dict_formats.RECORD)


def test_record_mode_preserves_generic_default() -> None:
    """The generic value union remains the default representation."""
    source = '{"name":"Ada","active":true,"scores":[1,2,3]}'
    default = literalize(
        source=source, input_format=InputFormat.JSON, language=Gleam()
    )
    native = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_record_spec(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "pub type GVal {" in "\n".join(default.preamble)
    native_preamble = native.code
    assert "pub type GVal {" not in native_preamble
    assert "pub type GVal0 {" in native_preamble
    assert "name: String" in native_preamble
    assert "active: Bool" in native_preamble
    assert "scores: List(Int)" in native_preamble
    assert 'name: "Ada"' in native.code


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
    """Unsupported values fail before invalid Gleam is produced."""
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
    preamble = "\n".join(result.preamble)
    assert "pub type GVal0" in preamble
    assert "pub type GVal1" in preamble
    assert "pub type GVal2" in preamble
    assert "members: List(GVal" in preamble
    assert "GDict" not in result.code


def test_record_mode_rejects_invalid_type_name() -> None:
    """Generated constructors need an uppercase Gleam name."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match="type_name"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=Gleam(
                dict_format=Gleam.dict_formats.RECORD,
                type_name="lowercase",
            ),
        )


def test_record_mode_temporal_fields() -> None:
    """Date, time, and datetime values retain concrete scalar types."""
    result = literalize(
        source=(
            "birthday = 2024-01-15\n"
            "when = 2024-01-15T12:30:00Z\n"
            "at = 09:30:00\n"
        ),
        input_format=InputFormat.TOML,
        language=_record_spec(),
    )
    preamble = "\n".join(result.preamble)
    assert "birthday: String" in preamble
    assert "when: String" in preamble
    assert "at: String" in preamble


def test_record_mode_epoch_datetime() -> None:
    """Epoch datetime values use a concrete Int field."""
    result = literalize(
        source="when = 2024-01-15T12:30:00Z\n",
        input_format=InputFormat.TOML,
        language=Gleam(
            dict_format=Gleam.dict_formats.RECORD,
            datetime_format=Gleam.datetime_formats.EPOCH,
        ),
    )
    assert "when: Int" in "\n".join(result.preamble)


def test_record_mode_binary_string_field() -> None:
    """Binary inputs use unwrapped string literals in native records."""
    for bytes_format in (Gleam.bytes_formats.HEX, Gleam.bytes_formats.BASE64):
        result = literalize(
            source="blob: !!binary AQID\n",
            input_format=InputFormat.YAML,
            language=Gleam(
                dict_format=Gleam.dict_formats.RECORD,
                bytes_format=bytes_format,
            ),
        )
        assert "blob: String" in "\n".join(result.preamble)
        assert "GStr" not in result.code


def test_record_mode_conflicts_with_json_value() -> None:
    """The JSON value backend and records are distinct output modes."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="json_type"
    ):
        _ = literalize(
            source='{"x":1}',
            input_format=InputFormat.JSON,
            language=Gleam(
                dict_format=Gleam.dict_formats.RECORD,
                json_type=Gleam.json_types.GLEAM_JSON_JSON,
            ),
        )


def test_record_mode_conflicts_with_tuple_sequences() -> None:
    """Tuple sequences do not have uniform list field types."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="LIST"
    ):
        _ = literalize(
            source='{"x":[1]}',
            input_format=InputFormat.JSON,
            language=Gleam(
                dict_format=Gleam.dict_formats.RECORD,
                sequence_format=Gleam.sequence_formats.TUPLE,
            ),
        )


def test_record_mode_rejects_call_stubs() -> None:
    """Call stubs cannot assume the generic GVal type in record mode."""
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
