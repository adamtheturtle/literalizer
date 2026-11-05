"""Source-layout dispatch at the public rendering boundary."""

import dataclasses
from typing import Protocol, runtime_checkable

from literalizer._language import Language
from literalizer._literalize import LiteralizeResult
from literalizer._types import Value
from literalizer.exceptions import SourceLayoutError
from literalizer.source_format import SourceContext, SourceFormat


@runtime_checkable
class _SourceLanguage(Protocol):
    """An explicitly selected language-owned source layout."""

    @property
    def source_format(self) -> SourceFormat:
        """Selected source formatting contract."""
        ...

    def layout_source(
        self,
        code: str,
        /,
        *,
        context: SourceContext,
        include_delimiters: bool,
        data: Value,
    ) -> str:
        """Lay out one generated fragment without changing its tokens."""
        ...


def format_result(
    *,
    result: LiteralizeResult,
    language: Language,
    source_context: SourceContext | None,
    pre_indent_level: int,
    include_delimiters: bool,
    wrapped: bool,
) -> LiteralizeResult:
    """Apply a producer's source contract and retain result metadata."""
    if not isinstance(language, _SourceLanguage):
        if source_context is not None:
            msg = "This language does not support source_context"
            raise SourceLayoutError(msg)
        return result
    if language.source_format is SourceFormat.PRESERVE:
        if source_context is not None:
            msg = "source_context requires canonical source formatting"
            raise SourceLayoutError(msg)
        return result
    if source_context is not None and pre_indent_level != 0:
        msg = "Use source_context or pre_indent_level, not both"
        raise SourceLayoutError(msg)
    context = (
        source_context
        if source_context is not None
        else SourceContext(indent_level=0 if wrapped else pre_indent_level)
    )
    if wrapped and (
        context.indent_level != 0
        or context.initial_column != 0
        or context.continuation_column not in (None, 0)
    ):
        msg = "A complete source file requires a zero-column source context"
        raise SourceLayoutError(msg)
    header_context = SourceContext(column_limit=context.column_limit)
    return dataclasses.replace(
        result,
        declaration_code=language.layout_source(
            result.declaration_code,
            context=context,
            include_delimiters=include_delimiters,
            data=result.source_data,
        ),
        preamble=tuple(
            language.layout_source(
                entry,
                context=header_context,
                include_delimiters=True,
                data=result.source_data,
            )
            for entry in result.preamble
        ),
        data_dependent_preamble=tuple(
            language.layout_source(
                entry,
                context=header_context,
                include_delimiters=True,
                data=result.source_data,
            )
            for entry in result.data_dependent_preamble
        ),
        body_preamble=tuple(
            language.layout_source(
                entry,
                context=context,
                include_delimiters=True,
                data=result.source_data,
            )
            for entry in result.body_preamble
        ),
        pre_declaration_comments=tuple(
            language.layout_source(
                entry,
                context=context,
                include_delimiters=True,
                data=result.source_data,
            )
            for entry in result.pre_declaration_comments
        ),
    )
