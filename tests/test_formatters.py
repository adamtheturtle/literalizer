"""Tests for literalizer formatters."""

import inspect

import pytest

from literalizer._formatters import (
    TypedOpenerConfig,
)
from literalizer.languages import (
    VisualBasic,
)

_VB = VisualBasic()


@pytest.mark.parametrize(
    argnames=("value", "expected"),
    argvalues=[
        pytest.param("", '""', id="empty"),
        pytest.param("hello", '"hello"', id="plain"),
        pytest.param('say "hi"', '"say ""hi"""', id="quotes"),
        pytest.param(
            "line1\r\nline2", '"line1" & vbCrLf & "line2"', id="crlf"
        ),
        pytest.param("\r\nline2", 'vbCrLf & "line2"', id="crlf_at_start"),
        pytest.param("line1\nline2", '"line1" & Chr(10) & "line2"', id="lf"),
        pytest.param("\nline2", 'Chr(10) & "line2"', id="lf_at_start"),
        pytest.param("line1\rline2", '"line1" & Chr(13) & "line2"', id="cr"),
        pytest.param("\rline2", 'Chr(13) & "line2"', id="cr_at_start"),
        pytest.param("col1\tcol2", '"col1" & vbTab & "col2"', id="tab"),
        pytest.param("\tcol2", 'vbTab & "col2"', id="tab_at_start"),
        pytest.param("\x01", "Chr(1)", id="control_char"),
        pytest.param(
            "\x01text",
            'Chr(1) & "text"',
            id="control_char_then_text",
        ),
        pytest.param(
            "text\x01",
            '"text" & Chr(1)',
            id="text_then_control_char",
        ),
    ],
)
def test_format_string_vb(value: str, expected: str) -> None:
    """``format_string_vb`` formats strings using VB.NET escaping
    rules.
    """
    assert _VB.format_string(value) == expected


def test_typed_opener_config_build_requires_scalar_type_overrides() -> None:
    """``TypedOpenerConfig.build`` has no default override mapping."""
    scalar_type_overrides = inspect.signature(
        obj=TypedOpenerConfig.build,
    ).parameters["scalar_type_overrides"]
    assert scalar_type_overrides.default is inspect.Signature.empty
