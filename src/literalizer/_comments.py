"""YAML and TOML comment extraction and formatting."""

import dataclasses
from collections.abc import Iterable
from typing import Any

from beartype import beartype
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.tokens import CommentToken
from tomlkit.items import Comment, Table, Whitespace
from tomlkit.toml_document import TOMLDocument


@dataclasses.dataclass(frozen=True)
class ElementComments:
    """Comments associated with a single top-level YAML element."""

    before: tuple[str, ...]
    inline: str


@beartype
def _strip_comment_marker(*, text: str) -> str:
    """Strip the leading ``#`` and one optional space from a comment line.

    Only the first ``#`` is removed so that ``## heading`` becomes
    ``# heading`` rather than ``heading``.

    The caller must ensure *text* starts with ``#`` (after stripping
    whitespace).
    """
    after_hash = text.strip()[1:]
    if after_hash.startswith(" "):
        return after_hash[1:]
    return after_hash


@beartype
def _token_comment_lines(*, value: str) -> list[str]:
    r"""Extract comment text lines from a ruamel.yaml token value.

    Token values look like ``"# text\n"`` or
    ``"# line1\n# line2\n"``.
    """
    return [
        _strip_comment_marker(text=line)
        for line in value.split(sep="\n")
        if line.strip().startswith("#")
    ]


@dataclasses.dataclass(frozen=True)
class _ParsedAfterToken:
    """Result of parsing an after-element comment token."""

    inline: str
    before_next: list[str]


@beartype
def _parse_after_token(
    *,
    token: CommentToken,
) -> _ParsedAfterToken:
    """Parse an after-element comment token.

    ruamel.yaml stores each comment as a ``CommentToken`` whose
    ``column`` attribute records the column position where the
    comment appeared in the original YAML source.  An inline
    comment (one that follows a value on the same line) always has
    ``column > 0`` because it appears after at least some content.
    A standalone comment that starts at the beginning of a line has
    ``column == 0``.  We use this to decide whether the first line
    of the token should be treated as an inline comment or as a
    standalone (before-next-element) comment.
    """
    value: str = token.value
    column: int = token.column
    lines = value.split(sep="\n")
    inline = ""
    start = 0

    if column > 0 and lines:
        inline = _strip_comment_marker(text=lines[0])
        start = 1

    before_next = [
        _strip_comment_marker(text=line)
        for line in lines[start:]
        if line.strip().startswith("#")
    ]
    return _ParsedAfterToken(inline=inline, before_next=before_next)


@dataclasses.dataclass(frozen=True)
class CollectionComments:
    """Comments extracted from a YAML sequence or mapping string."""

    elements: tuple[ElementComments, ...]
    trailing: tuple[str, ...]


@beartype
def extract_yaml_comments(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
) -> CollectionComments:
    """Extract top-level comments from parsed ruamel.yaml data.

    Only works for sequences, mappings, and sets — *ruamel.yaml*'s
    round-trip loader preserves comment metadata in
    :class:`CommentedSeq` / :class:`CommentedMap` / :class:`CommentedSet`
    objects.
    Scalar values do not carry this metadata; use
    :func:`_extract_scalar_comments` for those.
    """
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ca = ruamel_data.ca  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]

    # Header comments (before the first element).
    pending_before: list[str] = []
    if ca.comment and len(ca.comment) > 1 and ca.comment[1]:  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        for header_token in ca.comment[1]:  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            header_value: str = header_token.value  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            pending_before.extend(
                _token_comment_lines(value=header_value),  # pyright: ignore[reportUnknownArgumentType]
            )

    # Sequences and sets store after-element tokens at index 0,
    # mappings at index 2.
    match ruamel_data:
        case CommentedSeq():
            token_idx = 0
            keys: list[object] = list(range(len(ruamel_data)))
        case CommentedSet():
            token_idx = 0
            keys = list(ruamel_data)
        case _:
            token_idx = 2
            keys = list(ruamel_data.keys())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]

    # Iterate in insertion order so that pending_before propagation is
    # correct (a "before element N" comment is stored in the after-token
    # of element N-1 in insertion order).
    element_map: dict[object, ElementComments] = {}
    for key in keys:
        before = list(pending_before)
        inline = ""
        pending_before = []

        if key in ca.items:  # pyright: ignore[reportUnknownMemberType]
            item_token: CommentToken | None = ca.items[key][token_idx]  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            if item_token is not None:
                parsed = _parse_after_token(token=item_token)  # pyright: ignore[reportUnknownArgumentType]
                inline = parsed.inline
                pending_before = parsed.before_next

        element_map[key] = ElementComments(
            before=tuple(before),
            inline=inline,
        )

    # CommentedSet elements are emitted in sorted order by _literalize,
    # so reorder to match that sort key to keep comments aligned.
    if isinstance(ruamel_data, CommentedSet):
        output_keys: list[object] = sorted(
            keys,
            key=lambda v: (type(v).__name__, repr(v)),
        )
    else:
        output_keys = keys

    return CollectionComments(
        elements=tuple(element_map[k] for k in output_keys),
        trailing=tuple(pending_before),
    )


@beartype
def extract_toml_comments(
    *,
    toml_doc: object,
) -> CollectionComments:
    """Extract top-level comments from a parsed tomlkit document.

    Iterates over the document body and collects standalone comment
    nodes as "before" comments for the next keyed item, and inline
    ``trivia.comment`` values as inline comments.
    """
    if not isinstance(toml_doc, TOMLDocument):
        return CollectionComments(elements=(), trailing=())

    pending_before: list[str] = []
    elements: list[ElementComments] = []

    for _key, item in toml_doc.body:
        match item:
            case Comment():
                raw: str = item.trivia.comment
                pending_before.extend(
                    _token_comment_lines(value=raw),
                )
                continue
            case Whitespace():
                continue
            case _:
                pass
        inline = ""
        if not isinstance(item, Table):
            raw_inline: str = item.trivia.comment
            if raw_inline.startswith("#"):
                inline = _strip_comment_marker(text=raw_inline)
        elements.append(
            ElementComments(
                before=tuple(pending_before),
                inline=inline,
            ),
        )
        pending_before = []

    return CollectionComments(
        elements=tuple(elements),
        trailing=tuple(pending_before),
    )


@beartype
def _format_comment(
    *,
    text: str,
    comment_prefix: str,
    comment_suffix: str,
    line_prefix: str,
) -> str:
    """Format a single comment line."""
    if text:
        return f"{line_prefix}{comment_prefix} {text}{comment_suffix}"
    return f"{line_prefix}{comment_prefix}{comment_suffix}"


@dataclasses.dataclass(frozen=True)
class _ScalarComments:
    """Comments extracted from a scalar YAML string."""

    before: list[str]
    inline: str


@beartype
def _extract_scalar_comments(
    *,
    tokens: Iterable[Any],
) -> _ScalarComments:
    """Extract comments from scanned YAML tokens for a scalar value.

    *ruamel.yaml*'s round-trip loader returns plain Python objects
    for scalars with no comment metadata.  The token scanner,
    however, attaches :class:`CommentToken` objects to tokens,
    so we use that instead.

    *tokens* should come from ``YAML().scan()``.
    """
    before_comments: list[str] = []
    inline = ""
    for token in tokens:
        comment: list[Any] | None = token.comment
        if not comment:
            continue
        inline_token: CommentToken | None = comment[0]
        before_tokens: list[CommentToken] = comment[1] or []
        if inline_token is not None:
            value: str = inline_token.value
            inline = _strip_comment_marker(text=value)
        for bt in before_tokens:
            bt_value: str = bt.value
            before_comments.extend(
                _token_comment_lines(value=bt_value),
            )
        break
    return _ScalarComments(before=before_comments, inline=inline)


@dataclasses.dataclass(frozen=True)
class YamlCollectionContext:
    """Context for formatting sequence/mapping YAML with comments."""

    base: str
    element_comments: tuple[ElementComments, ...]
    trailing: tuple[str, ...]
    comment_prefix: str
    comment_suffix: str
    comment_line_prefix: str
    include_delimiters: bool


@dataclasses.dataclass(frozen=True)
class ScalarCommentResult:
    """Result of formatting scalar YAML comments.

    Attributes:
        result: The formatted scalar value, possibly with inline and
            before-comments embedded.
        pending_before: Already-formatted comment lines that should be
            emitted before the variable declaration.  Non-empty
            only when ``supports_scalar_before_comments`` is
            ``False``.
    """

    result: str
    pending_before: tuple[str, ...]


@beartype
def literalize_yaml_scalar(
    *,
    tokens: Iterable[Any],
    base: str,
    comment_prefix: str,
    comment_suffix: str,
    line_prefix: str,
    supports_scalar_before_comments: bool,
    supports_scalar_inline_comments: bool,
) -> ScalarCommentResult:
    """Preserve comments for scalar YAML values.

    Uses :func:`_extract_scalar_comments` to obtain comments
    from pre-scanned *ruamel.yaml* tokens.  Collection values
    use :func:`_extract_yaml_comments` instead.

    When *supports_scalar_before_comments* is ``False``, any
    comments that appear before the scalar value are returned in
    :attr:`ScalarCommentResult.pending_before` instead of being
    embedded in the result.

    When *supports_scalar_inline_comments* is ``False``, any
    inline comment on the scalar value is also returned in
    :attr:`ScalarCommentResult.pending_before` instead of being
    appended after the value.

    The caller is responsible for emitting pending comments
    before the variable declaration.
    """
    scalar_comments = _extract_scalar_comments(
        tokens=tokens,
    )

    if not scalar_comments.before and not scalar_comments.inline:
        return ScalarCommentResult(result=base, pending_before=())

    formatted_before = tuple(
        _format_comment(
            text=comment_text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )
        for comment_text in scalar_comments.before
    )

    pending: tuple[str, ...] = ()

    if scalar_comments.inline and supports_scalar_inline_comments:
        inline_value = (
            f"{base}  {comment_prefix} {scalar_comments.inline}"
            f"{comment_suffix}"
        )
    elif scalar_comments.inline:
        inline_value = base
        formatted_inline = _format_comment(
            text=scalar_comments.inline,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )
        pending = (formatted_inline,)
    else:
        inline_value = base

    if supports_scalar_before_comments:
        parts = [*formatted_before, inline_value]
        return ScalarCommentResult(
            result="\n".join(parts),
            pending_before=pending,
        )

    return ScalarCommentResult(
        result=inline_value,
        pending_before=(*formatted_before, *pending),
    )


@beartype
def literalize_yaml_collection(
    *,
    ctx: YamlCollectionContext,
) -> str:
    """Preserve comments for sequence/mapping YAML values."""
    effective_indent = ctx.comment_line_prefix
    all_lines = ctx.base.split(sep="\n")

    if ctx.include_delimiters and len(all_lines) > 1:
        header = all_lines[0]
        footer = all_lines[-1]
        body_lines = all_lines[1:-1]
    else:
        header = None
        footer = None
        body_lines = all_lines

    _empty = ElementComments(before=(), inline="")
    padded = ctx.element_comments + (_empty,) * (
        len(body_lines) - len(ctx.element_comments)
    )

    result: list[str] = []
    for body_line, element_comment in zip(body_lines, padded, strict=True):
        result.extend(
            _format_comment(
                text=comment_text,
                comment_prefix=ctx.comment_prefix,
                comment_suffix=ctx.comment_suffix,
                line_prefix=effective_indent,
            )
            for comment_text in element_comment.before
        )
        if element_comment.inline:
            inline_text = element_comment.inline
            output_line = (
                f"{body_line}  {ctx.comment_prefix} {inline_text}"
                f"{ctx.comment_suffix}"
            )
        else:
            output_line = body_line
        result.append(output_line)

    result.extend(
        _format_comment(
            text=comment_text,
            comment_prefix=ctx.comment_prefix,
            comment_suffix=ctx.comment_suffix,
            line_prefix=effective_indent,
        )
        for comment_text in ctx.trailing
    )

    if ctx.include_delimiters and header is not None and footer is not None:
        return "\n".join([header, *result, footer])
    return "\n".join(result)


@beartype
def prepend_collection_comments(
    *,
    collection_comments: CollectionComments,
    base: str,
    comment_prefix: str,
    comment_suffix: str,
    line_prefix: str,
) -> str:
    """Flatten all collection comments as lines before *base*.

    Used for languages that do not support comments inside collection
    initializers.  All element comments (before and inline) and trailing
    comments are flattened into standalone comment lines emitted
    immediately before *base*.

    Returns *base* unchanged when there are no comments.
    """

    def _fmt(text: str) -> str:
        """Delegate to module-level implementation."""
        return _format_comment(
            text=text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )

    lines: list[str] = []
    for ec in collection_comments.elements:
        lines.extend(_fmt(text=text) for text in ec.before)
        if ec.inline:
            lines.append(_fmt(text=ec.inline))
    lines.extend(_fmt(text=text) for text in collection_comments.trailing)
    if not lines:
        return base
    return "\n".join(lines) + "\n" + base


@beartype
def apply_collection_comments(
    *,
    collection_comments: CollectionComments,
    base: str,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> str:
    """Apply extracted comments to a collection literal.

    Returns *base* unchanged when there are no comments to apply.
    """
    has_comments = (
        any(
            element_comment.before or element_comment.inline
            for element_comment in collection_comments.elements
        )
        or collection_comments.trailing
    )
    if not has_comments:
        return base
    ctx = YamlCollectionContext(
        base=base,
        element_comments=collection_comments.elements,
        trailing=collection_comments.trailing,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
    return literalize_yaml_collection(ctx=ctx)


@beartype
def apply_collection_comments_to_elements(
    *,
    rendered_elements: list[str],
    collection_comments: CollectionComments,
    comment_prefix: str,
    comment_suffix: str,
) -> str:
    """Apply comments to a list of pre-rendered element strings.

    Unlike :func:`apply_collection_comments`, this function operates at
    element granularity rather than line granularity.  Each entry in
    *rendered_elements* may span multiple lines (e.g. a multi-line call
    expression), and comments are still attached to the correct element.

    Before-comments are emitted as standalone lines immediately before
    their element.  Inline comments are appended to the last line of
    their element.  Trailing comments follow all elements.
    """
    _empty = ElementComments(before=(), inline="")
    padded: list[ElementComments] = list(collection_comments.elements) + [
        _empty
    ] * max(0, len(rendered_elements) - len(collection_comments.elements))

    result: list[str] = []
    for element_str, ec in zip(rendered_elements, padded, strict=True):
        result.extend(
            _format_comment(
                text=comment_text,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
                line_prefix="",
            )
            for comment_text in ec.before
        )
        if ec.inline:
            element_lines = element_str.split("\n")
            element_lines[-1] = (
                f"{element_lines[-1]}  {comment_prefix} {ec.inline}"
                f"{comment_suffix}"
            )
            result.append("\n".join(element_lines))
        else:
            result.append(element_str)

    result.extend(
        _format_comment(
            text=comment_text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix="",
        )
        for comment_text in collection_comments.trailing
    )

    return "\n".join(result)
