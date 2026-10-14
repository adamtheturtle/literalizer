"""Formatter contracts for combinations outside the golden corpus."""

import dataclasses
from collections.abc import Callable
from functools import cached_property
from textwrap import dedent
from typing import override

from literalizer import (
    DictFormatConfig,
    FileWrapperContext,
    InputFormat,
    literalize,
)
from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Scalar, Value
from literalizer.languages import Go, Roc


def test_roc_call_wrapper_without_preamble() -> None:
    """An empty call preamble does not add separator lines."""
    # Wrapped public calls always generate a stub in the body preamble.
    # Only the wrapper itself accepts a call with no stub or declarations.
    language = Roc()
    assert language.wrap_calls_with_declarations(
        declarations=(),
        calls="call",
        context=FileWrapperContext(
            bound_variable_names=(),
            variable_name="",
            modifiers=frozenset(),
            body_preamble=(),
            class_preamble=(),
            has_literal_declarations=False,
            generated_body_preamble=(),
            call_stub_names=frozenset(),
            root_is_object_literal=False,
        ),
    ) == dedent(
        text="""\
        module [main]

        main =
            dbg (call)
            {}"""
    )


def test_plain_collection_callbacks_preserve_public_rendering() -> None:
    """Custom-language callbacks preserve widening and empty siblings."""
    native = Go()

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class CallbackGo(Go):
        """Use ordinary callbacks through the language extension
        contract.
        """

        plain_callbacks: bool

        @cached_property
        @override
        def sequence_open(self) -> Callable[[list[Value]], str]:
            """Expose an ordinary sequence callback."""
            if self.plain_callbacks:
                return lambda items: str(object=native.sequence_open(items))

            def _type_open(_element_type: type | ListType | DictType) -> str:
                """Provide the extension's integer collection opener."""
                return "[]int{"

            return typed_collection_open(
                type_to_opener=_type_open, fallback="[]any{"
            )

        @cached_property
        @override
        def dict_format_config(self) -> DictFormatConfig:
            """Expose an ordinary mapping callback."""

            def _open(items: dict[Scalar, Value], /) -> str:
                """Keep the callback result as plain source text."""
                return str(object=native.dict_format_config.dict_open(items))

            return dataclasses.replace(
                native.dict_format_config, dict_open=_open
            )

    source = (
        '{"lists": [[1], ["x"], []], '
        '"maps": [{"x": 1}, {"x": "s"}], '
        '"empties": {"a": [1], "b": []}}'
    )
    for language, input_source in (
        (CallbackGo(plain_callbacks=True), source),
        (CallbackGo(plain_callbacks=False), "[1, 2]"),
    ):
        result = literalize(
            source=input_source,
            input_format=InputFormat.JSON,
            language=language,
        )
        expected = literalize(
            source=input_source, input_format=InputFormat.JSON, language=native
        )
        assert result.code == expected.code
        assert result.preamble == expected.preamble
