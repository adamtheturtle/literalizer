"""Internal whole-document formatting dispatch."""

from functools import singledispatch

from beartype import beartype

from literalizer._language import CollectionLayout
from literalizer._types import Value


@singledispatch
@beartype
# pylint: disable-next=useless-return
def format_document_fast(
    language: object,
    data: Value,
    *,
    line_prefix: str,
    include_delimiters: bool,
    collection_layout: CollectionLayout,
) -> str | None:
    """Render *data* with a registered formatter, if one is available."""
    _ = language, data, line_prefix, include_delimiters, collection_layout
    return None
