"""Targeted Ada call-stub tests.

Covers no-parameter single-function stubs and empty-preamble paths in
``Ada.wrap_calls_with_declarations`` and ``Ada.wrap_in_file``.
"""

from literalizer._language import StubReturn
from literalizer.languages.ada import Ada


def test_no_param_void_stub() -> None:
    """Single-part void stub with no parameters omits the parameter
    list.
    """
    ada = Ada()
    result = ada.format_call_stub(["process"], [], StubReturn.VOID)
    assert result == ("procedure Process is begin null; end Process;",)


def test_no_param_value_stub() -> None:
    """Single-part value stub with no parameters omits the parameter
    list.
    """
    ada = Ada()
    result = ada.format_call_stub(["fetch"], [], StubReturn.VALUE)
    assert result == ("function Fetch return A_Val is (ANull);",)


def test_wrap_calls_with_declarations_empty_preamble() -> None:
    """Empty body_preamble and declarations omit the declarative
    section.
    """
    ada = Ada()
    result = ada.wrap_calls_with_declarations(
        declarations=(),
        calls="process;",
        body_preamble=(),
    )
    assert result == (
        "with A_Stub; use A_Stub;\n"
        "procedure Check is\n"
        "begin\n"
        "    process;\n"
        "end Check;"
    )


def test_wrap_in_file_call_mode_empty_preamble() -> None:
    """Call-mode wrap_in_file with empty body_preamble omits declarative
    section.
    """
    ada = Ada()
    result = ada.wrap_in_file(
        content="process;",
        variable_name="",
        body_preamble=(),
    )
    assert result == (
        "with A_Stub; use A_Stub;\n"
        "procedure Check is\n"
        "begin\n"
        "    process;\n"
        "end Check;"
    )
