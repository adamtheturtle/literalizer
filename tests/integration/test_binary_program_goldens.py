"""Binary property inputs and golden files execute as Python programs."""

import base64
import enum
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python

from .language_specs import make_golden_path, make_spec


def _run_program(*, program: str, expected: object) -> None:
    """Check the binding in the native interpreter, including its type."""
    completed = subprocess.run(  # noqa: S603 - execute generated test programs
        args=[
            sys.executable,
            "-I",
            "-c",
            program + f"\nassert my_data == {expected!r}\n",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def _expected(*, data: bytes, bytes_format: enum.Enum) -> bytes | str:
    """Compute each format's value independently of its renderer."""
    expected: dict[str, bytes | str] = {
        "HEX": data.hex(),
        "BASE64": base64.b64encode(s=data).decode(encoding="ascii"),
        "PYTHON": data,
    }
    return expected[bytes_format.name]


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="bytes_format", argvalues=list(Python.BytesFormats)
)
@example(data=b"")
@example(data=bytes(range(256)))
@given(data=st.binary())
def test_binary_documents_execute_as_programs(
    bytes_format: enum.Enum, version: enum.Enum, data: bytes
) -> None:
    """Retain the unbounded binary strategy and original wrapped API
    call.
    """
    encoded = base64.b64encode(s=data).decode(encoding="ascii")
    result = literalize(
        source=f'!!binary "{encoded}"\n',
        input_format=InputFormat.YAML,
        language=make_spec(
            lang_cls=Python,
            bytes_format=bytes_format,
            language_version=version,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert result.source_data == data
    _run_program(
        program=result.code,
        expected=_expected(data=data, bytes_format=bytes_format),
    )


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="bytes_format", argvalues=list(Python.BytesFormats)
)
def test_binary_octet_goldens_execute(
    *, cases_dir: Path, bytes_format: enum.Enum, version: enum.Enum
) -> None:
    """Compare and run the empty, complete and reversed byte corpus."""
    spec = make_spec(
        lang_cls=Python, bytes_format=bytes_format, language_version=version
    )
    case_dir = cases_dir / "binary_octets"
    result = literalize(
        source=(case_dir / "input.yaml").read_text(encoding="utf-8"),
        input_format=InputFormat.YAML,
        language=spec,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    name = (
        "Python"
        if bytes_format is Python.bytes_formats.HEX
        else f"Python_bytes_format_{bytes_format.name.lower()}"
    )
    golden = make_golden_path(
        parent=case_dir,
        name=name,
        lang_cls=Python,
        version=version,
    )
    assert result.code + "\n" == golden.read_text(encoding="utf-8")
    expected = tuple(
        _expected(data=data, bytes_format=bytes_format)
        for data in (b"", bytes(range(256)), bytes(reversed(range(256))))
    )
    _run_program(program=result.code, expected=expected)
