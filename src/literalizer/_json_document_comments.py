"""Translate JSON document metadata into Literalizer comment policies."""

import dataclasses

import json5_document
import jsonc_document
from beartype import beartype

from literalizer._comment_types import (
    CollectionComments,
    ElementComments,
    ScalarComments,
)
from literalizer._json_comments import JsonComments, attach_document_comments

type _Token = jsonc_document.Token | json5_document.Token
type _Node = jsonc_document.Node | json5_document.Node
type _Document = jsonc_document.Document | json5_document.Document


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
@dataclasses.dataclass
class _Comments:
    """Consume comments using source spans supplied by the document
    parsers.
    """

    source: str
    comments: tuple[_Token, ...]
    index: int

    def before(self, *, position: int) -> tuple[_Token, ...]:
        """Take comments preceding a syntax node or separator."""
        start = self.index
        while (
            self.index < len(self.comments)
            and self.comments[self.index].start < position
        ):
            self.index += 1
        return self.comments[start : self.index]

    def node(self, *, node: _Node) -> JsonComments:
        """Read associations from syntax nodes and their source spans."""
        scalar = ScalarComments(before=[], inline="", after=[])
        if not isinstance(node.value, (dict, list)):
            return JsonComments(collection=None, scalar=scalar, children=())
        elements: list[ElementComments] = []
        children: list[JsonComments] = []
        pending: tuple[str, ...] = ()
        nodes: tuple[_Node, ...] = node.children
        keys: tuple[_Token, ...] = node.keys
        starts: tuple[_Node | _Token, ...] = keys if bool(keys) else nodes
        for index, child_node in enumerate(iterable=nodes):
            before = (
                *pending,
                *(
                    line
                    for token in self.before(position=child_node.start)
                    for line in _comment_lines(token=token)
                ),
            )
            child = self.node(node=child_node)
            if child.collection is not None and not bool(child.children):
                before += child.flattened()
                child = dataclasses.replace(
                    child,
                    collection=CollectionComments(elements=(), trailing=()),
                )
            children.append(child)
            boundary = (
                starts[index + 1].start
                if index + 1 < len(starts)
                else node.end - 1
            )
            if index < len(node.commas):
                comma = node.commas[index]
                inline, pending = _split_comments(
                    source=self.source,
                    comments=self.before(position=comma.start),
                    end=child_node.end,
                )
                after_comma, following = _split_comments(
                    source=self.source,
                    comments=self.before(position=boundary),
                    end=child_node.end,
                )
                if bool(pending) and bool(after_comma):
                    pending += (after_comma,)
                else:
                    inline = " ".join(
                        part for part in (inline, after_comma) if bool(part)
                    )
                pending += following
            else:
                inline, pending = _split_comments(
                    source=self.source,
                    comments=self.before(position=boundary),
                    end=child_node.end,
                )
            elements.append(ElementComments(before=before, inline=inline))
        pending += tuple(
            line
            for token in self.before(position=node.end)
            for line in _comment_lines(token=token)
        )
        return JsonComments(
            collection=CollectionComments(
                elements=tuple(elements), trailing=pending
            ),
            scalar=scalar,
            children=tuple(children),
        )


@beartype
def extract_json_document_comments(
    *, document: _Document
) -> JsonComments | None:
    """Adapt validated parser metadata to existing comment rendering."""
    if not bool(document.comments):
        return None
    reader = _Comments(
        source=document.source, comments=document.comments, index=0
    )
    before = tuple(
        line
        for token in reader.before(position=document.root.start)
        for line in _comment_lines(token=token)
    )
    result = reader.node(node=document.root)
    inline, after = _split_comments(
        source=document.source,
        comments=reader.before(position=len(document.source) + 1),
        end=document.root.end,
    )
    return attach_document_comments(
        result=result, before=before, inline=inline, after=after
    )
