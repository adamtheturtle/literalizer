"""YAML and TOML comment extraction and formatting."""

import dataclasses
import datetime
import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, Protocol, assert_never, runtime_checkable

from beartype import beartype
from ruamel.yaml.comments import (
    CommentedBase,
    CommentedMap,
    CommentedSeq,
    CommentedSet,
    TaggedScalar,
)
from ruamel.yaml.tokens import CommentToken
from tomlkit.items import AoT, Comment, Item, Table, Whitespace
from tomlkit.toml_document import TOMLDocument

from literalizer._parsing import (
    unwrap_yaml_scalar,
)


class QuoteSensitiveCommentSuffix(str):
    """Mark a comment form whose lexer parses quotes inside comments."""

    __slots__ = ()


class EncodingCookieSafeCommentPrefix(str):
    """Mark comments that must not become Python encoding declarations."""

    __slots__ = ()


class ControlCharacterFreeCommentPrefix(str):
    """Mark comments whose text cannot carry a control character.

    Zig reports "comment contains invalid byte" for a tab, a DELETE,
    or any other C0 control inside a comment (issue #3962).
    """

    __slots__ = ()


_BIDI_COMMENT_CHARACTERS = (
    "\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069"
)
"""Bidirectional formatting characters, refused inside a comment.

Elixir raises a syntax error for one, ``rustc`` denies it and the Dart
analyzer warns, all under the "Trojan Source" heading.  A comment
carries no escapes, so each is replaced by a marker naming it, the way
the line and paragraph separators already are (issue #3963).
"""

_CONTROL_COMMENT_CHARACTERS = "".join(
    chr(code) for code in (*range(0x20), 0x7F)
)


_PYTHON_ENCODING_COOKIE = re.compile(
    pattern=(
        r"(?P<label>coding)(?P<separator>[:=])"
        r"(?P<encoding>[ \t]*[-_.a-zA-Z0-9]+)"
    ),
)


class NestingCommentSuffix(QuoteSensitiveCommentSuffix):
    """Mark a comment form whose opener starts a nested comment."""

    __slots__ = ()

    @property
    def opener(self) -> str:
        """Return the opening delimiter paired with this suffix."""
        return {
            "*)": "(*",
            "*/": "/*",
            "-}": "{-",
        }[self.strip()]


@dataclasses.dataclass(frozen=True)
class ElementComments:
    """Comments associated with a single top-level YAML element."""

    before: tuple[str, ...]
    inline: str


@beartype
def _yaml_set_sort_key(value: object) -> tuple[str, str]:
    """Return the rendering sort key for a wrapped YAML set member."""
    match value:
        case (
            bool()
            | int()
            | float()
            | str()
            | datetime.datetime()
            | datetime.date()
            | datetime.time()
            | bytes()
            | TaggedScalar()
            | None
        ):
            unwrapped = unwrap_yaml_scalar(value=value)
            return type(unwrapped).__name__, repr(unwrapped)
        case _:  # pragma: no cover - CommentedSet only accepts scalars
            return type(value).__name__, repr(value)


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
    # Source column of the first standalone line in *before_next*.
    # This is derived from that line when ruamel.yaml combines it with
    # an inline comment whose token column describes only the first line.
    standalone_column: int | None


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

    standalone_lines = [
        line for line in lines[start:] if line.strip().startswith("#")
    ]
    before_next = [
        _strip_comment_marker(text=line) for line in standalone_lines
    ]
    return _ParsedAfterToken(
        inline=inline,
        before_next=before_next,
        standalone_column=(
            len(standalone_lines[0]) - len(standalone_lines[0].lstrip())
            if standalone_lines
            else None
        ),
    )


@dataclasses.dataclass(frozen=True)
class CollectionComments:
    """Comments extracted from a YAML sequence or mapping string."""

    elements: tuple[ElementComments, ...]
    trailing: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class _CollectionTargets:
    """Iteration details for extracting collection comments."""

    token_idx: int
    keys: list[object]


@runtime_checkable
class _CommentAssociation(Protocol):
    """Typed boundary for ruamel.yaml comment association metadata."""

    comment: Sequence[Sequence[CommentToken] | None] | None
    items: Mapping[object, Sequence[CommentToken | None]]


@beartype
def _comment_association(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
) -> _CommentAssociation:
    """Return ruamel.yaml comment association metadata when available."""
    ca_descriptor: Any = CommentedBase.__dict__["ca"]
    ca: _CommentAssociation = ca_descriptor.fget(ruamel_data)
    return ca


@beartype
def _collection_targets(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
) -> _CollectionTargets:
    """Return comment-token index and iteration keys for a collection."""
    # Sequences and sets store after-element tokens at index 0,
    # mappings at index 2.
    match ruamel_data:
        case CommentedSet():
            return _CollectionTargets(token_idx=0, keys=list(ruamel_data))
        case CommentedMap():
            return _CollectionTargets(
                token_idx=2,
                keys=list(ruamel_data),
            )
        case CommentedSeq():
            return _CollectionTargets(
                token_idx=0,
                keys=list(range(len(ruamel_data))),
            )
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _header_comment_lines(*, ca: _CommentAssociation) -> list[str]:
    """Extract comments that appear before the first YAML element."""
    lines: list[str] = []
    if ca.comment is None or len(ca.comment) <= 1:
        return lines

    for header_token in ca.comment[1] or ():
        header_value: str = header_token.value
        lines.extend(
            _token_comment_lines(value=header_value),
        )
    return lines


@beartype
def _element_after_comments(
    *,
    ca: _CommentAssociation,
    key: object,
    token_idx: int,
) -> _ParsedAfterToken:
    """Extract inline and before-next comments after one element."""
    if key not in ca.items:
        return _ParsedAfterToken(
            inline="", before_next=[], standalone_column=None
        )

    item_tokens = ca.items[key]
    item_token = item_tokens[token_idx]
    if item_token is None:
        return _ParsedAfterToken(
            inline="", before_next=[], standalone_column=None
        )
    return _parse_after_token(token=item_token)


@runtime_checkable
class _CollectionValues(Protocol):
    """Typed boundary for ruamel.yaml collection value lookup."""

    def __getitem__(self, key: object, /) -> object:
        """Return a collection value by key or index."""
        ...  # pylint: disable=unnecessary-ellipsis


@beartype
def _collection_value(
    *,
    values: _CollectionValues,
    key: object,
) -> object:
    """Return a value through the typed collection lookup protocol."""
    return values[key]


@beartype
def _collection_element_value(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
    key: object,
) -> object:
    """Return the collection element identified by *key*."""
    match ruamel_data:
        case CommentedSet():
            return key
        case CommentedMap() | CommentedSeq():
            return _collection_value(values=ruamel_data, key=key)
        case _ as unreachable:
            assert_never(unreachable)


@runtime_checkable
class _LineCol(Protocol):
    """Typed boundary for ruamel.yaml source position metadata."""

    col: int


@beartype
def _collection_column(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
) -> int:
    """Return the source column this collection is written at."""
    lc_descriptor: Any = CommentedBase.__dict__["lc"]
    lc: _LineCol = lc_descriptor.fget(ruamel_data)
    return lc.col


@beartype
def _outdented_trailing_comments(
    *,
    value: object,
    own_column: int,
    intervening_columns: tuple[int, ...],
) -> ElementComments:
    """Return comments stored on *value* that belong to its parent.

    ruamel.yaml attaches a standalone comment written between two
    elements of an outer collection to the *last* element of the inner
    collection that precedes it.  Such a comment is written at or to the
    left of the outer collection's indentation, so it is outdented
    relative to the inner collection holding it, while a comment that
    genuinely trails the inner collection is indented to that
    collection's own column.

    Walk down the chain of last elements collecting the comments written
    at or to the right of *own_column*, so a comment stored several
    levels down still reaches the collection it was written for.  YAML
    puts no constraint on where a comment starts, so it need not line up
    with any collection exactly; the collection that claims it is the
    innermost enclosing one it is not outdented from.

    *intervening_columns* holds the columns of the collections walked
    through to reach *value*.  Any of them that the comment is also
    indented from is a closer claimant, and claims the comment through
    its own walk, so this one leaves it alone.
    """
    if not isinstance(value, CommentedSeq | CommentedMap | CommentedSet):
        return ElementComments(before=(), inline="")

    nested_column = _collection_column(ruamel_data=value)
    targets = _collection_targets(ruamel_data=value)
    if not targets.keys:
        return ElementComments(before=(), inline="")

    last_key = targets.keys[-1]
    deeper = _outdented_trailing_comments(
        value=_collection_element_value(ruamel_data=value, key=last_key),
        own_column=own_column,
        intervening_columns=(*intervening_columns, nested_column),
    )
    parsed = _element_after_comments(
        ca=_comment_association(ruamel_data=value),
        key=last_key,
        token_idx=targets.token_idx,
    )
    standalone_column = parsed.standalone_column
    claimed = (
        standalone_column is not None
        and own_column <= standalone_column < nested_column
        and not any(
            own_column < column <= standalone_column
            for column in intervening_columns
        )
    )
    if claimed:
        return ElementComments(
            before=(*deeper.before, *parsed.before_next),
            inline=parsed.inline or deeper.inline,
        )
    return deeper


@beartype
def extract_yaml_comments(
    *,
    ruamel_data: CommentedSeq | CommentedMap | CommentedSet,
    nested: bool,
) -> CollectionComments:
    """Extract top-level comments from parsed ruamel.yaml data.

    Only works for sequences, mappings, and sets — *ruamel.yaml*'s
    round-trip loader preserves comment metadata in
    :class:`CommentedSeq` / :class:`CommentedMap` / :class:`CommentedSet`
    objects.
    Scalar values do not carry this metadata; use
    :func:`_extract_scalar_comments` for those.

    Set *nested* when *ruamel_data* is a collection inside a larger
    document.  A standalone comment written at an enclosing collection's
    indentation is stored by *ruamel.yaml* on the last element of the
    nested collection that precedes it, and belongs to that enclosing
    collection rather than to this one.  A root collection has no
    enclosing collection, so it keeps every comment stored on it.
    """
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ca = _comment_association(ruamel_data=ruamel_data)

    # Header comments (before the first element).
    pending_before = _header_comment_lines(ca=ca)
    targets = _collection_targets(ruamel_data=ruamel_data)
    own_column = _collection_column(ruamel_data=ruamel_data)

    # Iterate in insertion order so that pending_before propagation is
    # correct (a "before element N" comment is stored in the after-token
    # of element N-1 in insertion order).
    element_map: dict[object, ElementComments] = {}
    for key in targets.keys:
        before = list(pending_before)
        parsed = _element_after_comments(
            ca=ca,
            key=key,
            token_idx=targets.token_idx,
        )
        # A standalone comment outdented from this collection was
        # written for an enclosing one, which claims it through its own
        # walk over nested elements.  A root collection has no enclosing
        # collection to claim it, so it keeps everything stored on it.
        outdented = (
            nested
            and parsed.standalone_column is not None
            and parsed.standalone_column < own_column
        )
        inline = "" if outdented else parsed.inline
        pending_before = [] if outdented else parsed.before_next
        # ruamel.yaml stores a comment written between two elements of
        # this collection on the last element of the nested collection
        # that precedes it, so collect it from there.
        nested_comments = _outdented_trailing_comments(
            value=_collection_element_value(
                ruamel_data=ruamel_data,
                key=key,
            ),
            own_column=own_column,
            intervening_columns=(),
        )
        pending_before += list(nested_comments.before)
        inline = inline or nested_comments.inline

        element_map[key] = ElementComments(
            before=tuple(before),
            inline=inline,
        )

    # CommentedSet elements are emitted in sorted order by _literalize,
    # so reorder to match that sort key to keep comments aligned.
    if isinstance(ruamel_data, CommentedSet):
        output_keys: list[object] = sorted(
            targets.keys,
            key=_yaml_set_sort_key,
        )
    else:
        output_keys = targets.keys

    return CollectionComments(
        elements=tuple(element_map[k] for k in output_keys),
        trailing=tuple(pending_before),
    )


@beartype
def _toml_inline_comment(*, item: Item) -> str:
    """Return the comment written after *item* on its own line."""
    raw: str = item.trivia.comment
    if raw.startswith("#"):
        return _strip_comment_marker(text=raw)
    return ""


@dataclasses.dataclass(frozen=True)
class _TomlNestedComments:
    """Comments found below one top-level TOML item.

    Attributes:
        hoisted: Comments written above or beside a value inside the
            item.  A flat model of top-level elements has nowhere finer
            to put them, so they attach to the enclosing element rather
            than being dropped (issues #4482 and #4484).
        trailing: Comments written after the item's last value.  Those
            were written for whatever follows the item, so they belong
            to the next top-level element instead.
    """

    hoisted: tuple[str, ...]
    trailing: tuple[str, ...]


_NO_TOML_NESTED_COMMENTS = _TomlNestedComments(hoisted=(), trailing=())


@beartype
def _toml_body_comments(
    *,
    body: Iterable[tuple[object, Item]],
) -> _TomlNestedComments:
    """Collect the comments written inside one TOML container body."""
    hoisted: list[str] = []
    pending: list[str] = []
    for _key, child in body:
        match child:
            case Comment():
                raw: str = child.trivia.comment
                pending.extend(_token_comment_lines(value=raw))
            case Whitespace():
                pass
            case _:
                inner = _toml_nested_comments(item=child)
                inline = _toml_inline_comment(item=child)
                hoisted.extend(pending)
                pending = list(inner.trailing)
                hoisted.extend((inline,) if inline else ())
                hoisted.extend(inner.hoisted)
    return _TomlNestedComments(
        hoisted=tuple(hoisted),
        trailing=tuple(pending),
    )


@beartype
def _toml_nested_comments(*, item: Item) -> _TomlNestedComments:
    """Collect the comments written below one TOML item.

    A table body, an array of tables and a dotted key's implicit table
    all hold comments belonging to a key nested inside a top-level
    element, none of which this extractor used to read.
    """
    match item:
        case AoT():
            entries: list[Item] = list(item.body)
            return _toml_body_comments(
                body=[(None, entry) for entry in entries],
            )
        case Table():
            return _toml_body_comments(body=item.value.body)
        case _:
            return _NO_TOML_NESTED_COMMENTS


@beartype
def extract_toml_comments(
    *,
    toml_doc: TOMLDocument,
) -> CollectionComments:
    """Extract top-level comments from a parsed tomlkit document.

    Iterates over the document body and collects standalone comment
    nodes as "before" comments for the next keyed item, and inline
    ``trivia.comment`` values as inline comments.

    A dotted key is stored as one implicit table per entry, so ``a.b``
    and ``a.c`` are two body items for the single rendered element
    ``a``.  Items sharing a key are merged into one, wherever in the
    document they are written, so that the result has exactly one entry
    per rendered element (issue #4482).
    """
    pending_before: list[str] = []
    elements: dict[object, ElementComments] = {}

    for key, item in toml_doc.body:
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
        inline = (
            "" if isinstance(item, Table) else _toml_inline_comment(item=item)
        )
        nested = _toml_nested_comments(item=item)
        before = (*pending_before, *nested.hoisted)
        pending_before = list(nested.trailing)
        merged = elements.get(key, ElementComments(before=(), inline=""))
        elements[key] = ElementComments(
            before=(*merged.before, *before),
            inline=merged.inline or inline,
        )

    return CollectionComments(
        elements=tuple(elements.values()),
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
        if isinstance(comment_prefix, EncodingCookieSafeCommentPrefix):
            text = _PYTHON_ENCODING_COOKIE.sub(
                repl=r"\g<label> \g<separator>\g<encoding>",
                string=text,
                count=1,
            )
        escaped = neutralize_comment_terminator(
            text=text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
        )
        if not comment_suffix and escaped.endswith("\\"):
            # A final backslash can splice the following physical line in
            # C-family source processing (and continues lines in several
            # shells).
            escaped += " ."
        return f"{line_prefix}{comment_prefix} {escaped}{comment_suffix}"
    return f"{line_prefix}{comment_prefix}{comment_suffix}"


@beartype
def _mark_code_points(*, text: str, characters: str) -> str:
    """Replace each of *characters* with a marker naming it."""
    for character in characters:
        if character in text:
            text = text.replace(character, f"<U+{ord(character):04X}>")
    return text


@beartype
def neutralize_comment_terminator(
    *,
    text: str,
    comment_prefix: str,
    comment_suffix: str,
) -> str:
    """Prevent *text* from closing a suffix-delimited target comment.

    Multi-character terminators remain readable with a space inserted
    between their characters (``*/`` becomes ``* /``). A one-character
    terminator cannot appear at all inside its comment form, so represent
    it with an ASCII Unicode-code-point marker (``)`` becomes
    ``<U+0029>``). Line-comment formats have an empty suffix and leave
    the source text unchanged.
    """
    text = _mark_code_points(
        text=text,
        characters=f"\u2028\u2029{_BIDI_COMMENT_CHARACTERS}",
    )
    if isinstance(comment_prefix, ControlCharacterFreeCommentPrefix):
        text = _mark_code_points(
            text=text,
            characters=_CONTROL_COMMENT_CHARACTERS,
        )
    if isinstance(comment_suffix, QuoteSensitiveCommentSuffix):
        text = text.translate(str.maketrans("", "", "\"'"))
    terminator = comment_suffix.strip()
    if isinstance(comment_suffix, NestingCommentSuffix):
        opener = comment_suffix.opener
        text = text.replace(opener, " ".join(opener))
    if not terminator or terminator not in text:
        return text
    replacement = (
        " ".join(terminator)
        if len(terminator) > 1
        else f"<U+{ord(terminator):04X}>"
    )
    return text.replace(terminator, replacement)


@dataclasses.dataclass(frozen=True)
class _ScalarComments:
    """Comments extracted from a scalar YAML string."""

    before: list[str]
    inline: str
    after: list[str]


@beartype
def _split_scalar_after_token(*, value: str) -> _ScalarComments:
    r"""Split a trailing comment token into its comment position classes.

    *ruamel.yaml* hands the whole run of comments that follow a scalar
    over as one token.  Only its first line can be an inline comment,
    and only when the token starts on the same line as the value, which the
    token value records by having no leading newline.  ``"# c\n"`` is
    therefore inline while ``"\n# c\n"`` and ``"\n  # c\n"`` are
    standalone comments on the lines after the value.  Every line
    beyond the first is standalone whatever the first one is.
    """
    lines = value.split(sep="\n")
    head, tail = lines[0], lines[1:]
    if head.strip().startswith("#"):
        return _ScalarComments(
            before=[],
            inline=_strip_comment_marker(text=head),
            after=_token_comment_lines(value="\n".join(tail)),
        )
    return _ScalarComments(
        before=[],
        inline="",
        after=_token_comment_lines(value=value),
    )


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
    trailing = _ScalarComments(before=[], inline="", after=[])
    for token in tokens:
        comment: list[Any] | None = token.comment
        if not comment:
            continue
        inline_token: CommentToken | None = comment[0]
        before_tokens: list[CommentToken] = comment[1] or []
        if inline_token is not None:
            value: str = inline_token.value
            trailing = _split_scalar_after_token(value=value)
        for bt in before_tokens:
            bt_value: str = bt.value
            before_comments.extend(
                _token_comment_lines(value=bt_value),
            )
        break
    return _ScalarComments(
        before=before_comments,
        inline=trailing.inline,
        after=trailing.after,
    )


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

    if (
        not scalar_comments.before
        and not scalar_comments.inline
        and not scalar_comments.after
    ):
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
    formatted_after = tuple(
        _format_comment(
            text=comment_text,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )
        for comment_text in scalar_comments.after
    )

    pending: tuple[str, ...] = ()

    match bool(scalar_comments.inline), supports_scalar_inline_comments:
        case True, True:
            escaped_inline = neutralize_comment_terminator(
                text=scalar_comments.inline,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
            )
            inline_value = (
                f"{base}  {comment_prefix} {escaped_inline}{comment_suffix}"
            )
        case True, False:
            inline_value = base
            formatted_inline = _format_comment(
                text=scalar_comments.inline,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
                line_prefix=line_prefix,
            )
            pending = (formatted_inline,)
        case _:
            inline_value = base

    # Trailing standalone comments can only follow the value where an
    # inline comment could: both need the value to end the declaration,
    # or the rest of the declaration would land inside the comment.
    trailing = formatted_after if supports_scalar_inline_comments else ()
    pending += () if supports_scalar_inline_comments else formatted_after

    if supports_scalar_before_comments:
        parts = [*formatted_before, inline_value, *trailing]
        return ScalarCommentResult(
            result="\n".join(parts),
            pending_before=pending,
        )

    return ScalarCommentResult(
        result="\n".join([inline_value, *trailing]),
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
    # Every extractor now emits one entry per rendered element, so no
    # surplus entry has to be folded into the last line (issue #4482).
    element_comments = ctx.element_comments
    padded = (
        element_comments
        + (_empty,) * (len(body_lines) - len(element_comments))
    )[: len(body_lines)]

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
            inline_text = neutralize_comment_terminator(
                text=element_comment.inline,
                comment_prefix=ctx.comment_prefix,
                comment_suffix=ctx.comment_suffix,
            )
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
    line_prefix: str,
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
                line_prefix=line_prefix,
            )
            for comment_text in ec.before
        )
        if ec.inline:
            escaped_inline = neutralize_comment_terminator(
                text=ec.inline,
                comment_prefix=comment_prefix,
                comment_suffix=comment_suffix,
            )
            element_lines = element_str.split(sep="\n")
            element_lines[-1] = (
                f"{element_lines[-1]}  {comment_prefix} {escaped_inline}"
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
            line_prefix=line_prefix,
        )
        for comment_text in collection_comments.trailing
    )

    return "\n".join(result)
