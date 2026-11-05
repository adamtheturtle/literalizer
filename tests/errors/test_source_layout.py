"""Diagnostics for unsupported source policies and placement contracts."""

import subprocess
from unittest.mock import Mock

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    SourceContext,
    SourceFormat,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
    literalize_native_calls,
)
from literalizer.exceptions import SourceLayoutError
from literalizer.languages import ObjectiveC, Python


@pytest.mark.parametrize(argnames="position", argvalues=[-1, -20])
def test_negative_indentation(position: int) -> None:
    """A logical indentation level cannot precede the enclosing scope."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="nonnegative"
    ):
        _ = SourceContext(indent_level=position)


@pytest.mark.parametrize(argnames="position", argvalues=[-1, -20])
def test_negative_initial_column(position: int) -> None:
    """The first source column cannot be negative."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="nonnegative"
    ):
        _ = SourceContext(initial_column=position)


@pytest.mark.parametrize(argnames="position", argvalues=[-1, -20])
def test_negative_continuation_column(position: int) -> None:
    """Continuation lines cannot precede the start of the line."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="continuation"
    ):
        _ = SourceContext(continuation_column=position)


@pytest.mark.parametrize(argnames="width", argvalues=[-1, 0])
def test_nonpositive_column_limit(width: int) -> None:
    """Every layout must have an available source column."""
    with pytest.raises(expected_exception=SourceLayoutError, match="positive"):
        _ = SourceContext(column_limit=width)


def test_unsupported_language() -> None:
    """A source context cannot silently change an unconfigured
    language.
    """
    with pytest.raises(
        expected_exception=SourceLayoutError, match="does not support"
    ):
        _ = literalize(
            source="[]",
            input_format=InputFormat.JSON,
            language=Python(),
            source_context=SourceContext(),
        )


def test_legacy_policy() -> None:
    """Explicit placement requires the producer's canonical policy."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="requires canonical"
    ):
        _ = literalize(
            source="[]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(),
            source_context=SourceContext(),
        )


@pytest.mark.parametrize(argnames="wrapped", argvalues=[False, True])
def test_ambiguous_placement(*, wrapped: bool) -> None:
    """The old indentation argument cannot compete with a source
    context.
    """
    with pytest.raises(expected_exception=SourceLayoutError, match="not both"):
        _ = literalize(
            source="[]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(source_format=SourceFormat.CANONICAL),
            source_context=SourceContext(),
            pre_indent_level=1,
            wrap_in_file=wrapped,
            variable_form=NewVariable(name="data", modifiers=frozenset()),
        )


@pytest.mark.parametrize(
    argnames="context",
    argvalues=[
        SourceContext(indent_level=1),
        SourceContext(initial_column=1),
        SourceContext(continuation_column=1),
    ],
)
def test_complete_file_requires_zero_column(context: SourceContext) -> None:
    """A complete program carries its own file-scope placement."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="zero-column"
    ):
        _ = literalize(
            source="[]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(source_format=SourceFormat.CANONICAL),
            source_context=context,
            wrap_in_file=True,
            variable_form=NewVariable(name="data", modifiers=frozenset()),
        )


@pytest.mark.parametrize(argnames="indent", argvalues=["", "\t", " \t"])
def test_canonical_indentation_requires_spaces(indent: str) -> None:
    """Unsupported indentation gets a public, actionable diagnostic."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="made of spaces"
    ):
        _ = literalize(
            source="[]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(
                source_format=SourceFormat.CANONICAL, indent=indent
            ),
        )


def test_renderer_needs_no_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every public composition boundary works without process
    execution.
    """
    monkeypatch.setenv(name="PATH", value="")

    unavailable = Mock(
        side_effect=AssertionError("External process execution")
    )
    monkeypatch.setattr(target=subprocess, name="Popen", value=unavailable)
    language = ObjectiveC(source_format=SourceFormat.CANONICAL, indent="  ")
    declaration = literalize(
        source='["hello", 42]',
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="data", modifiers=frozenset()),
    )
    call = literalize_call(
        source='["hello", 42]',
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("value",),
    )
    _ = literalize_call_with_declarations(
        language=language,
        declarations=[declaration],
        call=call,
    )
    _ = literalize_native_calls(
        source="[[42]]",
        input_format=InputFormat.JSON,
        language=language,
        invocation={
            "function": "consumeInteger",
            "parameter-types": ["integer"],
            "return-type": "void",
            "arguments": [{"input": 0}],
        },
    )

    unavailable.assert_not_called()


def test_native_batch_rejects_inline_context() -> None:
    """A caller prefix cannot apply to several independent statements."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="exactly one native call"
    ):
        _ = literalize_native_calls(
            source="[[1],[2]]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(source_format=SourceFormat.CANONICAL),
            source_context=SourceContext(initial_column=4),
            invocation={
                "function": "consume",
                "parameter-types": ["integer"],
                "return-type": "void",
                "arguments": [{"input": 0}],
            },
        )


def test_generic_batch_rejects_inline_context() -> None:
    """Explicit expression placement must not join call statements."""
    with pytest.raises(
        expected_exception=SourceLayoutError, match="one statement"
    ):
        _ = literalize_call(
            source="[1,2]",
            input_format=InputFormat.JSON,
            language=ObjectiveC(source_format=SourceFormat.CANONICAL),
            source_context=SourceContext(initial_column=4),
            target_function="consume",
            parameter_names=("value",),
        )
