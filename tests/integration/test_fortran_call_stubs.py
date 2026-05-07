"""Targeted Fortran call-stub tests.

Covers no-parameter single-function stubs and empty-preamble paths in
``Fortran.wrap_calls_with_declarations`` and ``Fortran.wrap_in_file``.
"""

from literalizer._language import StubReturn
from literalizer.languages.fortran import Fortran


def test_no_param_void_stub() -> None:
    """Single-part void stub with no parameters omits the parameter
    declarations but keeps the empty argument list.
    """
    fortran = Fortran()
    result = fortran.format_call_stub(["process"], [], StubReturn.VOID, ())
    assert result == (
        "subroutine process()\n    implicit none\nend subroutine process",
    )


def test_no_param_value_stub() -> None:
    """Single-part value stub with no parameters omits the parameter
    declarations but keeps the empty argument list.
    """
    fortran = Fortran()
    result = fortran.format_call_stub(["fetch"], [], StubReturn.VALUE, ())
    assert result == (
        "function fetch() result(r)\n"
        "    implicit none\n"
        "    type(fval_t) :: r\n"
        "    r = fnull()\n"
        "end function fetch",
    )


def test_wrap_in_file_call_mode_empty_preamble() -> None:
    """Call-mode wrap_in_file with empty body_preamble omits the
    contains section.
    """
    fortran = Fortran(module_name="main")
    result = fortran.wrap_in_file(
        content="call process()",
        variable_name="",
        body_preamble=(),
    )
    assert result == (
        "program main\n"
        "    use fval_m\n"
        "    implicit none\n"
        "    call process()\n"
        "end program main"
    )


def test_wrap_calls_with_declarations_empty_bare_code() -> None:
    """Empty bare_code strings in declarations are skipped silently."""
    fortran = Fortran(module_name="main")
    result = fortran.wrap_calls_with_declarations(
        declarations=("",),
        calls="call process()",
        body_preamble=(),
    )
    assert result == (
        "program main\n"
        "    use fval_m\n"
        "    implicit none\n"
        "    call process()\n"
        "end program main"
    )
