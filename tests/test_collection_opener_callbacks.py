"""Custom callable openers retain their public rendering behavior.

A case manifest cannot declare user-supplied collection callbacks.
"""

import dataclasses
from collections.abc import Callable
from functools import cached_property
from typing import override

import pytest

from literalizer import InputFormat, literalize
from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._language import DictFormatConfig, Language
from literalizer._types import Scalar, Value
from literalizer.languages import Cpp, Go, Jsonc


class _TextOnlyGo(Go):
    """A Go extension with ordinary callable collection openers."""

    @cached_property
    @override
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Expose a text-only callback, as existing extensions may do."""
        native = Go().sequence_open
        return lambda items: str(object=native(items))

    @cached_property
    @override
    def dict_format_config(self) -> DictFormatConfig:
        """Expose a text-only mapping callback."""
        native = Go().dict_format_config

        def _open(items: dict[Scalar, Value], /) -> str:
            """Return source text from the extension's map callback."""
            return str(object=native.dict_open(items))

        return dataclasses.replace(native, dict_open=_open)


class _TextOnlyCpp(Cpp):
    """A C++ extension with an ordinary array callback."""

    @cached_property
    @override
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Keep the selected standard and fixed-array format."""
        native = Cpp(sequence_format=self.sequence_format).sequence_open
        return lambda items: str(object=native(items))


class _TextOnlyJsonc(Jsonc):
    """A JSONC extension with an ordinary mapping callback."""

    @cached_property
    @override
    def dict_format_config(self) -> DictFormatConfig:
        """Expose its content-independent mapping callback."""
        native = Jsonc().dict_format_config

        def _open(items: dict[Scalar, Value], /) -> str:
            """Return source text from the extension's map callback."""
            return str(object=native.dict_open(items))

        return dataclasses.replace(native, dict_open=_open)


class _CustomTypedGo(Go):
    """A Go extension providing its own typed opener callback."""

    @cached_property
    @override
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Choose an integer opener through an ordinary type callback."""

        def _type_open(_element_type: type | ListType | DictType) -> str:
            """Spell the extension's integer collection opener."""
            return "[]int{"

        return typed_collection_open(
            type_to_opener=_type_open, fallback="[]any{"
        )


@pytest.mark.parametrize(
    argnames=("language", "native", "source"),
    argvalues=[
        (_TextOnlyGo(), Go(), '[[1], ["s"], []]'),
        (_TextOnlyGo(), Go(), '[{"a": 1}, {"b": "s"}]'),
        (_TextOnlyGo(), Go(), '{"a": {"x": 1}, "b": {"x": "s"}}'),
        (_TextOnlyCpp(), Cpp(), '[[1], ["s"], []]'),
        (
            _TextOnlyCpp(sequence_format=Cpp.sequence_formats.ARRAY),
            Cpp(sequence_format=Cpp.sequence_formats.ARRAY),
            '{"a": [1, 2], "b": []}',
        ),
        (_TextOnlyJsonc(), Jsonc(), '[{"a": 1}, {"b": "s"}]'),
        (_CustomTypedGo(), Go(), "[1, 2]"),
    ],
)
def test_custom_collection_callbacks_preserve_public_output(
    language: Language, native: Language, source: str
) -> None:
    """Custom openers preserve widening, empty siblings, and array lengths."""
    result = literalize(
        source=source, input_format=InputFormat.JSON, language=language
    )
    expected = literalize(
        source=source, input_format=InputFormat.JSON, language=native
    )
    assert result.code == expected.code
    assert result.preamble == expected.preamble
