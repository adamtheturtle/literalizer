"""Hypothesis roundtrip tests for literalizer converter."""

import ast
import base64
import json

from beartype import beartype
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from literalizer import literalize_json, literalize_yaml
from literalizer._formatters import format_bytes_hex, format_bytes_python
from literalizer.languages import Python

PYTHON = Python(
    date_format=Python.DateFormat.PYTHON,
    datetime_format=Python.DatetimeFormat.PYTHON,
    bytes_format=Python.BytesFormat.HEX,
    sequence_format=Python.SequenceFormat.TUPLE,
    set_format=Python.SetFormat.SET,
    variable_type_hints=Python.VariableTypeHints.NONE,
)

type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]


@beartype
def _lists_to_tuples(*, value: _JSONValue) -> object:
    """Recursively convert lists to tuples to match Python converter
    output.
    """
    if isinstance(value, list):
        return tuple(_lists_to_tuples(value=v) for v in value)
    if isinstance(value, dict):
        return {k: _lists_to_tuples(value=v) for k, v in value.items()}
    return value


# Characters valid in JSON strings: Unicode letters (L), marks (M), numbers
# (N), punctuation (P), symbols (S), and separators (Z). Control characters
# (category C) are excluded because JSON forbids raw control characters,
# and ``\x00`` is excluded explicitly because json.dumps refuses null bytes.
json_text = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"
    )
)
json_scalars = (
    st.none()
    | st.booleans()
    | st.integers()
    # ``nan`` and ``inf`` are excluded because JSON does not support them.
    | st.floats(allow_nan=False, allow_infinity=False)
    | json_text
)
json_values: st.SearchStrategy[_JSONValue] = st.recursive(
    base=json_scalars,
    extend=lambda children: (
        # ``max_size`` prevents unbounded nesting that causes test timeouts.
        st.lists(elements=children, max_size=5)
        | st.dictionaries(keys=json_text, values=children, max_size=5)
    ),
)
# ``max_size`` prevents very large inputs that would slow down tests.
json_arrays = st.lists(elements=json_values, max_size=10)
json_objects = st.dictionaries(keys=json_text, values=json_values, max_size=10)


@given(data=json_arrays)
def test_roundtrip_array(data: list[_JSONValue]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == tuple(_lists_to_tuples(value=v) for v in data)


@given(data=json_scalars)
def test_roundtrip_scalar(data: _JSONScalar) -> None:
    """Scalar -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == data


# ``st.dictionaries`` internally filters draws to ensure unique keys, which
# can accumulate enough filtered examples to trigger the ``filter_too_much``
# health check on unlucky seeds.  The filtering is expected behavior here,
# so we suppress the check rather than change the strategy.
@given(data=json_objects)
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_roundtrip_dict(data: dict[str, _JSONValue]) -> None:
    """JSON object -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == _lists_to_tuples(value=data)


@given(data=st.binary())
def test_roundtrip_bytes_python(data: bytes) -> None:
    """Format_bytes_python -> ast.literal_eval round-trips."""
    result = format_bytes_python(value=data)
    assert ast.literal_eval(node_or_string=result) == data


@given(data=st.binary())
def test_roundtrip_bytes_hex(data: bytes) -> None:
    """Format_bytes_hex -> bytes.fromhex round-trips."""
    result = format_bytes_hex(value=data)
    assert bytes.fromhex(result.strip('"')) == data


@given(data=st.binary())
def test_roundtrip_yaml_binary_python(data: bytes) -> None:
    """YAML !!binary -> literalize_yaml (Python) -> ast.literal_eval round-
    trips.
    """
    encoded = base64.b64encode(s=data).decode()
    yaml_string = f"- !!binary |\n  {encoded}\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert ast.literal_eval(node_or_string=result.rstrip(",")) == data.hex()
