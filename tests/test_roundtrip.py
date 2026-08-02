"""Hypothesis roundtrip tests for literalizer converter."""

import ast
import json
import re

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from literalizer import (
    BothVariableForms,
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.languages import Erlang, Python

# Use LIST sequence format so that ast.literal_eval returns plain lists,
# matching the JSON input directly without any conversion step.
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.LIST,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)
PYTHON_BYTES = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.PYTHON,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)
PYTHON_MULTILINE = Python(
    sequence_format=Python.sequence_formats.LIST,
    string_format=Python.string_formats.MULTILINE,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
)
_MULTILINE_VALUE = "\nfirst line\n  indented\n\nlast line\n"

type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]


# Characters valid in JSON strings: Unicode letters (L), marks (M), numbers
# (N), punctuation (P), symbols (S), and separators (Z). Control characters
# (category C) are excluded because JSON forbids raw control characters,
# and ``\x00`` is excluded explicitly because json.dumps refuses null bytes.
json_text = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"
    ),
    max_size=20,
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
        st.lists(elements=children, max_size=3)
        | st.dictionaries(keys=json_text, values=children, max_size=3)
    ),
    # ``max_leaves`` caps total nodes generated; the recursive strategy
    # is by far the dominant cost in these tests, so a tight bound here
    # is the biggest single performance lever without losing
    # meaningful coverage.
    max_leaves=15,
)
json_arrays = st.lists(elements=json_values, max_size=5)
json_objects = st.dictionaries(keys=json_text, values=json_values, max_size=5)


@settings(deadline=None)
@given(data=json_arrays)
def test_roundtrip_array(data: list[_JSONValue]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data


@given(data=json_scalars)
def test_roundtrip_scalar(data: _JSONScalar) -> None:
    """Scalar -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data


def test_roundtrip_multiline_string_contexts() -> None:
    """Multiline root and nested values preserve their exact contents."""
    value = "\nfirst line\n  indented\n\nlast line\n"
    for data in (value, [[[value]]]):
        result = literalize(
            source=json.dumps(obj=data),
            input_format=InputFormat.JSON,
            language=PYTHON_MULTILINE,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )

        assert ast.literal_eval(node_or_string=result.code) == data


# ``st.dictionaries`` internally filters draws to ensure unique keys, which
# can accumulate enough filtered examples to trigger the ``filter_too_much``
# health check on unlucky seeds.  The filtering is expected behavior here,
# so we suppress the check rather than change the strategy.
@given(data=json_objects)
@settings(deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_roundtrip_dict(data: dict[str, _JSONValue]) -> None:
    """JSON object -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    parsed = ast.literal_eval(node_or_string=result.code)
    assert parsed == data


def test_multiline_string_root_and_nested_round_trip() -> None:
    """Multiline syntax preserves scalar and nested collection values."""
    for value in (_MULTILINE_VALUE, [[_MULTILINE_VALUE]]):
        result = literalize(
            source=json.dumps(obj=value),
            input_format=InputFormat.JSON,
            language=PYTHON_MULTILINE,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )

        assert ast.literal_eval(node_or_string=result.code) == value


def test_multiline_string_new_and_existing_variable_round_trip() -> None:
    """Declaration and assignment forms preserve multiline values."""
    for variable_form, expected_assignment_count in (
        (NewVariable(name="my_data", modifiers=frozenset()), 1),
        (BothVariableForms(name="my_data", modifiers=frozenset()), 2),
    ):
        result = literalize(
            source=json.dumps(obj=_MULTILINE_VALUE),
            input_format=InputFormat.JSON,
            language=PYTHON_MULTILINE,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=variable_form,
            wrap_in_file=True,
        )
        assignments = [
            node
            for node in ast.parse(source=result.code).body
            if isinstance(node, ast.Assign)
        ]

        assert len(assignments) == expected_assignment_count
        assert all(
            ast.literal_eval(node_or_string=node.value) == _MULTILINE_VALUE
            for node in assignments
        )


def test_multiline_string_pre_indent_round_trip() -> None:
    """Generated code indentation does not become string indentation."""
    result = literalize(
        source=json.dumps(obj=_MULTILINE_VALUE),
        input_format=InputFormat.JSON,
        language=PYTHON_MULTILINE,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )
    tree = ast.parse(source=f"if True:\n{result.code}")
    if_statement = tree.body[0]

    assert isinstance(if_statement, ast.If)
    assignment = if_statement.body[0]
    assert isinstance(assignment, ast.Assign)
    assert (
        ast.literal_eval(node_or_string=assignment.value) == _MULTILINE_VALUE
    )


@given(data=st.binary())
def test_roundtrip_bytes_python(data: bytes) -> None:
    """Format_bytes_python -> ast.literal_eval round-trips."""
    result = PYTHON_BYTES.format_bytes(data)
    assert ast.literal_eval(node_or_string=result) == data


@given(data=st.binary())
def test_roundtrip_bytes_hex(data: bytes) -> None:
    """Format_bytes_hex -> bytes.fromhex round-trips."""
    result = PYTHON.format_bytes(data)
    assert result.startswith('"')
    assert result.endswith('"')
    assert bytes.fromhex(result[1:-1]) == data


# YAML ``!!binary`` parsing and per-language bytes-format wiring are covered
# across the language/version matrix by ``tests/integration/cases/binary``.
# Keep only unique formatter semantics in this property-test module.
ERLANG_LANG = Erlang()


@given(data=st.binary())
def test_roundtrip_bytes_erlang_binary(data: bytes) -> None:
    """Erlang binary literal round-trips."""
    result = ERLANG_LANG.format_bytes(data)
    if not data:
        assert result == "<<>>"
        return
    match = re.fullmatch(pattern=r"<<(.+)>>", string=result)
    assert match is not None
    byte_values = [int(x.strip()) for x in match.group(1).split(sep=",")]
    assert bytes(byte_values) == data
