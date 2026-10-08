"""Formatter contracts for combinations outside the golden corpus."""

from textwrap import dedent

from literalizer import FileWrapperContext
from literalizer.languages import Roc


def test_roc_call_wrapper_without_preamble() -> None:
    """An empty call preamble does not add separator lines."""
    # Wrapped public calls always generate a stub in the body preamble.
    # Only the wrapper itself accepts a call with no stub or declarations.
    language = Roc()
    assert language.wrap_calls_with_declarations(
        declarations=(),
        calls="call",
        context=FileWrapperContext(
            variable_name="",
            modifiers=frozenset(),
            body_preamble=(),
            class_preamble=(),
        ),
    ) == dedent(
        text="""\
        module [main]

        main =
            dbg (call)
            {}"""
    )
