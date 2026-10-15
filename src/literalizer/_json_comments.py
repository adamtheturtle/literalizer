"""Associate comments with values in already-validated JSONC."""

import dataclasses
from collections.abc import Iterator

from beartype import beartype

from literalizer._comment_types import (
    CollectionComments,
    ElementComments,
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


@dataclasses.dataclass(frozen=True)
class _Token:
    """One source token with offsets in the unmodified input."""

    text: str
    start: int
    end: int

    @property
    def is_comment(self) -> bool:
        """Whether this token contains a source comment."""
        return self.text.startswith(("//", "/*"))

    def lines(self) -> tuple[str, ...]:
        """Remove the comment delimiters and surrounding whitespace."""
        text = self.text[2:]
        if self.text.startswith("/*"):
            text = text[:-2]
        return (
            tuple(line.strip() for line in text.splitlines())
            if bool(text)
            else ("",)
        )


@beartype
def _string_end(*, source: str, start: int) -> int:
    """Skip a validated quoted token, including escaped quotes."""
    index = start + 1
    while source[index] != source[start]:
        if source[index] == "\\":
            index += 1
        index += 1
    return index + 1


@beartype
def _tokens(*, source: str) -> Iterator[_Token]:
    """Scan valid source without interpreting string or number values."""
    index = 0
    line_endings = "\r\n"
    while index < len(source):
        char = source[index]
        if char.isspace() or char == "\ufeff":
            index += 1
            continue
        start = index
        if char in "\"'":
            index = _string_end(source=source, start=index)
        elif source.startswith("//", index):
            index += 2
            while index < len(source) and source[index] not in line_endings:
                index += 1
        elif source.startswith("/*", index):
            index = source.index("*/", index + 2) + 2
        elif char in "{}[]:,":
            index += 1
        else:
            index += 1
            while (
                index < len(source)
                and not source[index].isspace()
                and source[index] not in "{}[]:,/\ufeff"
            ):
                index += 1
        yield _Token(text=source[start:index], start=start, end=index)


@dataclasses.dataclass
class _CommentReader:
    """Walk lexical tokens alongside the data tree from the canonical
    parser.
    """

    source: str
    tokens: list[_Token]
    index: int

    def comments(self) -> tuple[str, ...]:
        """Consume a run of comments before the next syntax token."""
        lines: list[str] = []
        while self.tokens[self.index].is_comment:
            lines.extend(self.tokens[self.index].lines())
            self.index += 1
        return tuple(lines)

    def after(self, *, end: int) -> tuple[str, tuple[str, ...]]:
        """Split same-line comments from standalone following comments."""
        inline: list[str] = []
        trailing: list[str] = []
        while self.index < len(self.tokens):
            token = self.tokens[self.index]
            if not token.is_comment:
                break
            lines = token.lines()
            gap = self.source[end : token.start]
            if (
                bool(lines[0])
                and not bool(trailing)
                and not any(c in gap for c in "\r\n\u2028\u2029")
            ):
                inline.append(lines[0])
                trailing.extend(lines[1:])
            else:
                trailing.extend(lines)
            end = token.end
            self.index += 1
        return " ".join(inline), tuple(trailing)

    def value(self, *, data: Value) -> JsonComments:
        """Read one value whose syntax has already been validated."""
        self.index += 1
        empty_scalar = ScalarComments(before=[], inline="", after=[])
        if not isinstance(data, (dict, list)):
            return JsonComments(
                collection=None, scalar=empty_scalar, children=()
            )
        values = list(data.values()) if isinstance(data, dict) else data
        elements: list[ElementComments] = []
        children: list[JsonComments] = []
        pending = self.comments()
        for value in values:
            before = pending
            if isinstance(data, dict):
                self.index += 1  # member name
                before += self.comments()
                self.index += 1  # colon
                before += self.comments()
            child = self.value(data=value)
            if child.collection is not None and len(child.children) == 0:
                before += child.flattened()
                child = dataclasses.replace(
                    child,
                    collection=CollectionComments(elements=(), trailing=()),
                )
            children.append(child)
            end = self.tokens[self.index - 1].end
            inline, pending = self.after(end=end)
            if self.tokens[self.index].text == ",":
                self.index += 1
                after_comma, following = self.after(end=end)
                if bool(pending) and bool(after_comma):
                    pending += (after_comma,)
                else:
                    inline = " ".join(
                        part for part in (inline, after_comma) if bool(part)
                    )
                pending += following
            elements.append(ElementComments(before=before, inline=inline))
        self.index += 1  # closing delimiter
        return JsonComments(
            collection=CollectionComments(
                elements=tuple(elements), trailing=pending
            ),
            scalar=empty_scalar,
            children=tuple(children),
        )


@beartype
def extract_jsonc_comments(*, source: str, data: Value) -> JsonComments | None:
    """Read comments after successful parsing, leaving diagnostics
    intact.
    """
    if "/" not in source:
        return None
    tokens = list(_tokens(source=source))
    if not any(token.is_comment for token in tokens):
        return None
    reader = _CommentReader(source=source, tokens=tokens, index=0)
    before = reader.comments()
    result = reader.value(data=data)
    inline, after = reader.after(end=tokens[reader.index - 1].end)
    return attach_document_comments(
        result=result, before=before, inline=inline, after=after
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
