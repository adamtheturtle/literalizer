"""Adapt JSON syntax spans to Literalizer's comment-placement policies."""

import dataclasses
from bisect import bisect_left

import json5_document
import jsonc_document
from beartype import beartype

from literalizer._comment_types import (
    CollectionComments,
    ElementComments,
    ScalarComments,
)
from literalizer._types import Value

type _Token = jsonc_document.Token | json5_document.Token
type _Node = jsonc_document.Node | json5_document.Node
type _Document = jsonc_document.Document | json5_document.Document


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
def _comment_lines(*, token: _Token) -> tuple[str, ...]:
    """Remove comment delimiters using the existing whitespace policy."""
    text = token.text[2:]
    if token.text.startswith("/*"):
        text = text[:-2]
    return (
        tuple(line.strip() for line in text.splitlines())
        if bool(text)
        else ("",)
    )


@beartype
def _split_comments(
    *, source: str, comments: tuple[_Token, ...], end: int
) -> tuple[str, tuple[str, ...]]:
    """Separate inline comments from following standalone comment
    lines.
    """
    inline: list[str] = []
    trailing: list[str] = []
    for token in comments:
        lines = _comment_lines(token=token)
        gap = source[end : token.start]
        if (
            bool(lines[0])
            and not bool(trailing)
            and not any(char in gap for char in "\r\n\u2028\u2029")
        ):
            inline.append(lines[0])
            trailing.extend(lines[1:])
        else:
            trailing.extend(lines)
        end = token.end
    return " ".join(inline), tuple(trailing)


@beartype
def _merge_comment_groups(
    *,
    inline: str,
    pending: tuple[str, ...],
    following_inline: str,
    following: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    """Keep comments after a comma behind preceding standalone
    comments.
    """
    if bool(pending) and bool(following_inline):
        return inline, (*pending, following_inline, *following)
    return (
        " ".join(part for part in (inline, following_inline) if bool(part)),
        (*pending, *following),
    )


@beartype
def extract_json_comments(*, document: _Document) -> JsonComments | None:
    """Associate parser-owned comments using explicit source intervals."""
    comments = document.comments
    if not bool(comments):
        return None
    positions = tuple(token.start for token in comments)

    @beartype
    def between(*, start: int, end: int) -> tuple[_Token, ...]:
        """Select comments beginning in a half-open source interval."""
        return comments[
            bisect_left(a=positions, x=start) : bisect_left(a=positions, x=end)
        ]

    @beartype
    def lines(*, start: int, end: int) -> tuple[str, ...]:
        """Normalize the comments in one source interval."""
        return tuple(
            line
            for token in between(start=start, end=end)
            for line in _comment_lines(token=token)
        )

    @beartype
    def read(*, node: _Node, start: int, end: int) -> JsonComments:
        """Attach surrounding comments while walking a syntax tree."""
        pending = lines(start=start, end=node.start)
        footer_inline, footer = _split_comments(
            source=document.source,
            comments=between(start=node.end, end=end),
            end=node.end,
        )
        if not isinstance(node.value, (dict, list)):
            return JsonComments(
                collection=None,
                scalar=ScalarComments(
                    before=list(pending),
                    inline=footer_inline,
                    after=list(footer),
                ),
                children=(),
            )
        elements: list[ElementComments] = []
        children: list[JsonComments] = []
        nodes: tuple[_Node, ...] = node.children
        keys: tuple[_Token, ...] = node.keys
        starts: tuple[_Node | _Token, ...] = keys if bool(keys) else nodes
        entry_start = node.start
        for index, child_node in enumerate(iterable=nodes):
            before = (
                *pending,
                *lines(start=entry_start, end=child_node.start),
            )
            child = read(
                node=child_node, start=child_node.start, end=child_node.end
            )
            if child.collection is not None and not bool(child.children):
                before += child.flattened()
                child = dataclasses.replace(
                    child,
                    collection=CollectionComments(elements=(), trailing=()),
                )
            children.append(child)
            entry_start = (
                starts[index + 1].start
                if index + 1 < len(starts)
                else node.end - 1
            )
            comma = node.commas[index] if index < len(node.commas) else None
            inline, pending = _split_comments(
                source=document.source,
                comments=between(
                    start=child_node.end,
                    end=entry_start if comma is None else comma.start,
                ),
                end=child_node.end,
            )
            if comma is not None:
                after_comma, following = _split_comments(
                    source=document.source,
                    comments=between(start=comma.end, end=entry_start),
                    end=child_node.end,
                )
                inline, pending = _merge_comment_groups(
                    inline=inline,
                    pending=pending,
                    following_inline=after_comma,
                    following=following,
                )
            elements.append(ElementComments(before=before, inline=inline))
        if not bool(nodes):
            pending += lines(start=node.start, end=node.end)
        return JsonComments(
            collection=CollectionComments(
                elements=tuple(elements),
                trailing=(
                    *pending,
                    *((footer_inline,) if bool(footer_inline) else ()),
                    *footer,
                ),
            ),
            scalar=ScalarComments(before=[], inline="", after=[]),
            children=tuple(children),
        )

    return read(node=document.root, start=0, end=len(document.source))


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
