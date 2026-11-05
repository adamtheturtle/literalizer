"""Binary documents survive parsing, public rendering and native syntax.

The shared binary_octets fixtures additionally compile the empty value,
every octet and reversed octets across the language/version matrix.
"""

import ast
import base64
import enum
import re

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Erlang, Python


def _binary_source(*, data: bytes) -> str:
    """Encode an independent YAML binary document, including empty
    data.
    """
    encoded = base64.b64encode(s=data).decode(encoding="ascii")
    return f'!!binary "{encoded}"\n'


@pytest.mark.parametrize(
    argnames="bytes_format", argvalues=list(Python.BytesFormats)
)
@example(data=b"")
@example(data=bytes(range(256)))
@given(data=st.binary())
def test_python_binary_document_roundtrip(
    bytes_format: enum.Enum, data: bytes
) -> None:
    """Parse a complete emitted program and recover its binary binding."""
    assert isinstance(bytes_format, Python.BytesFormats)
    result = literalize(
        source=_binary_source(data=data),
        input_format=InputFormat.YAML,
        language=Python(bytes_format=bytes_format),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert result.source_data == data
    program = ast.parse(source=result.code)
    (assignment,) = program.body
    assert isinstance(assignment, ast.Assign)
    value = ast.literal_eval(node_or_string=assignment.value)
    expected = {
        "HEX": data.hex(),
        "BASE64": base64.b64encode(s=data).decode(encoding="ascii"),
        "PYTHON": data,
    }[bytes_format.name]
    assert value == expected


@example(data=b"")
@example(data=bytes(range(256)))
@given(data=st.binary())
def test_erlang_binary_document_roundtrip(data: bytes) -> None:
    """Recover the octets from the complete emitted Erlang module."""
    result = literalize(
        source=_binary_source(data=data),
        input_format=InputFormat.YAML,
        language=Erlang(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert result.source_data == data
    match = re.search(
        pattern=r"\bMy_data = <<(?P<octets>[\d,\s]*)>>,",
        string=result.code,
    )
    assert match is not None
    assert (
        bytes(
            int(value)
            for value in match["octets"].split(sep=",")
            if bool(value.strip())
        )
        == data
    )
