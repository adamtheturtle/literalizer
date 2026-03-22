"""YAML comment extraction and formatting."""

import dataclasses
from collections.abc import Iterable
from typing import Any

from beartype import beartype
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.tokens import CommentToken


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

    The *column* of the token determines whether its first line
    is an inline comment (column > 0) or a standalone comment.
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
    token_idx = 2 if isinstance(ruamel_data, CommentedMap) else 0

    if isinstance(ruamel_data, CommentedSeq):
        keys: list[object] = list(range(len(ruamel_data)))
    elif isinstance(ruamel_data, CommentedSet):
        keys = list(ruamel_data)
    else:
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


@beartype
def literalize_yaml_scalar(
    *,
    tokens: Iterable[Any],
    base: str,
    comment_prefix: str,
    comment_suffix: str,
    line_prefix: str,
) -> str:
    """Preserve comments for scalar YAML values.

    Uses :func:`_extract_scalar_comments` to obtain comments
    from pre-scanned *ruamel.yaml* tokens.  Collection values
    use :func:`_extract_yaml_comments` instead.
    """
    scalar_comments = _extract_scalar_comments(
        tokens=tokens,
    )

    if not scalar_comments.before and not scalar_comments.inline:
        return base

    parts: list[str] = [
        _format_comment(
            text=comment_text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )
        for comment_text in scalar_comments.before
    ]
    if scalar_comments.inline:
        parts.append(
            f"{base}  {comment_prefix} {scalar_comments.inline}"
            f"{comment_suffix}",
        )
    else:
        parts.append(base)
    return "\n".join(parts)


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

    @beartype
    def _fmt(text: str) -> str:
        """Format *text* as a comment line using the outer parameters."""
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
