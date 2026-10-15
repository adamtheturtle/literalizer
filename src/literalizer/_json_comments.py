"""Shared comment trees and rendering policies for JSON-family
documents.
"""

import dataclasses

from beartype import beartype

from literalizer._comment_types import (
    CollectionComments,
    ScalarComments,
)
from literalizer._types import Value


@beartype
@dataclasses.dataclass(frozen=True)
class JsonComments:
    """Comment tree parallel to the parsed data, indexed by entry
    order.
    """

    collection: CollectionComments | None
    scalar: ScalarComments
    children: tuple["JsonComments", ...]

    def flattened(self) -> tuple[str, ...]:
        """Return all comments in source order for a fallback renderer."""
        if self.collection is None:
            inline = (self.scalar.inline,) if bool(self.scalar.inline) else ()
            return (*self.scalar.before, *inline, *self.scalar.after)
        lines: list[str] = []
        for element, child in zip(
            self.collection.elements, self.children, strict=True
        ):
            lines.extend(element.before)
            lines.extend(child.flattened())
            if bool(element.inline):
                lines.append(element.inline)
        lines.extend(self.collection.trailing)
        return tuple(lines)

    def call_comments(self) -> CollectionComments:
        """Hoist nested argument comments before their containing call."""
        if self.collection is None:
            raise NotImplementedError
        return CollectionComments(
            elements=tuple(
                dataclasses.replace(
                    element, before=(*element.before, *child.flattened())
                )
                for element, child in zip(
                    self.collection.elements, self.children, strict=True
                )
            ),
            trailing=self.collection.trailing,
        )


@beartype
def attach_document_comments(
    *,
    result: JsonComments,
    before: tuple[str, ...],
    inline: str,
    after: tuple[str, ...],
) -> JsonComments:
    """Attach comments surrounding a complete input document."""
    if result.collection is None:
        return dataclasses.replace(
            result,
            scalar=ScalarComments(
                before=list(before), inline=inline, after=list(after)
            ),
        )
    collection = result.collection
    elements = collection.elements
    if bool(elements):
        elements = (
            dataclasses.replace(
                elements[0], before=(*before, *elements[0].before)
            ),
            *elements[1:],
        )
        before = ()
    return dataclasses.replace(
        result,
        collection=CollectionComments(
            elements=elements,
            trailing=(
                *before,
                *collection.trailing,
                *((inline,) if bool(inline) else ()),
                *after,
            ),
        ),
    )


@beartype
def collection_comment_nodes(
    *, data: Value, comments: JsonComments
) -> dict[int, CollectionComments]:
    """Index a comment tree by the rendered collections' identities."""
    if comments.collection is None:
        return {}
    if not isinstance(data, (dict, list)):
        raise NotImplementedError
    if len(data) == 0:
        return {}
    result = {id(data): comments.collection}
    values = list(data.values()) if isinstance(data, dict) else data
    for value, child in zip(values, comments.children, strict=True):
        result.update(collection_comment_nodes(data=value, comments=child))
    return result
