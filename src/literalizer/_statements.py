"""Grouping rendered lines back into whole statements.

A file wrapper receives its statements as one string with a newline
between them.  While every statement is one line that is the same thing,
but a collection rendered under
:attr:`~literalizer.CollectionLayout.MULTILINE` spans several, and a
wrapper that puts a prefix or a separator on each line then puts one on
each *part* of a statement instead of on the statement (issue #4548).
"""

import dataclasses
import functools
import re
from typing import Protocol, runtime_checkable

from beartype import beartype

_OPENING_BRACKETS = "([{"
_CLOSING_BRACKETS = ")]}"


@runtime_checkable
class LiteralSpanEnd(Protocol):
    """Recognize an additional literal at the scanner's current
    position.
    """

    def __call__(self, *, statement: str, cursor: int) -> int | None:
        """Return the position after a literal, or no match."""
        ...


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _TrailingLineComments:
    """An expression and its preserved trailing whitespace and
    comments.
    """

    code: str
    trailing_comments: str


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class CallLiteralSyntax:
    """The literal grammar used to locate a call's trailing comments."""

    prefix: str
    quotes: str
    regex_literals: bool
    backtick_strings: bool
    raw_string_prefixes: tuple[str, ...]
    verbatim_strings: bool
    interpolation_syntax: tuple[str, str] | None
    literal_span_end: LiteralSpanEnd | None

    @beartype
    def split(self, statement: str, /) -> _TrailingLineComments:
        """Separate final comments using this producer's actual
        grammar.
        """
        return split_trailing_line_comments(
            statement=statement,
            prefix=self.prefix,
            quotes=self.quotes,
            regex_literals=self.regex_literals,
            backtick_strings=self.backtick_strings,
            raw_string_prefixes=self.raw_string_prefixes,
            verbatim_strings=self.verbatim_strings,
            interpolation_syntax=self.interpolation_syntax,
            literal_span_end=self.literal_span_end,
        )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _CommentScanner:
    """Locate comments outside the configured string literal syntax."""

    statement: str
    prefix: str
    quotes: frozenset[str]
    regex_literals: bool
    backtick_strings: bool
    raw_string_prefixes: tuple[str, ...]
    verbatim_strings: bool
    interpolation_syntax: tuple[str, str] | None
    literal_span_end: LiteralSpanEnd | None

    @beartype
    def split(self) -> _TrailingLineComments:
        """Keep only the final run of line comments separate."""
        cursor = 0
        trailing_start = len(self.statement)
        while cursor < len(self.statement):
            if self.statement[cursor].isspace():
                cursor += 1
            elif self.statement.startswith(self.prefix, cursor):
                trailing_start = min(trailing_start, cursor)
                cursor = self._end_after(delimiter="\n", cursor=cursor)
            else:
                trailing_start = len(self.statement)
                end = self._span_end(cursor=cursor)
                cursor = cursor + 1 if end is None else end
        if trailing_start == len(self.statement):
            return _TrailingLineComments(
                code=self.statement, trailing_comments=""
            )
        code = self.statement[:trailing_start].rstrip()
        return _TrailingLineComments(
            code=code, trailing_comments=self.statement[len(code) :]
        )

    @beartype
    def _end_after(self, *, delimiter: str, cursor: int) -> int:
        """Advance through a delimiter, or to the end if it is absent."""
        end = self.statement.find(delimiter, cursor)
        return len(self.statement) if end == -1 else end + len(delimiter)

    @beartype
    def _span_end(self, *, cursor: int) -> int | None:
        """Skip a comment or literal starting at the cursor."""
        if self.statement.startswith(self.prefix, cursor):
            return self._end_after(delimiter="\n", cursor=cursor)
        if self.statement.startswith("/*", cursor):
            return self._end_after(delimiter="*/", cursor=cursor + 2)
        if self.regex_literals and self.statement.startswith("~/", cursor):
            return self._string_end(
                cursor=cursor + 2,
                delimiter="/",
                raw=False,
                verbatim=False,
                interpolate=False,
            )
        if self.backtick_strings and self.statement.startswith("`", cursor):
            return self._end_after(delimiter="`", cursor=cursor + 1)
        if self.literal_span_end is not None:
            end = self.literal_span_end(
                statement=self.statement, cursor=cursor
            )
            if end is not None:
                return end
        if self.statement[cursor] in self.quotes:
            end = self._quoted_end(cursor=cursor, raw=False, verbatim=False)
        else:
            end = self._prefixed_string_end(cursor=cursor)
        return end

    @beartype
    def _prefixed_string_end(self, *, cursor: int) -> int | None:
        """Skip raw and verbatim strings with a leading syntax marker."""
        if self.statement.startswith('R"', cursor):
            opening_parenthesis = self.statement.find("(", cursor + 2)
            delimiter = self.statement[cursor + 2 : opening_parenthesis]
            return self._end_after(
                delimiter=f'){delimiter}"',
                cursor=max(cursor + 2, opening_parenthesis + 1),
            )
        for marker in self.raw_string_prefixes:
            quote_start = cursor + len(marker)
            if not self.statement.startswith(marker, cursor):
                continue
            if self.statement[quote_start : quote_start + 1] in self.quotes:
                return self._quoted_end(
                    cursor=quote_start, raw=True, verbatim=False
                )
        for opening in ('@"', '@$"'):
            if self.verbatim_strings and self.statement.startswith(
                opening, cursor
            ):
                return self._quoted_end(
                    cursor=cursor + len(opening) - 1,
                    raw=False,
                    verbatim=True,
                )
        return None

    @beartype
    def _quoted_end(self, *, cursor: int, raw: bool, verbatim: bool) -> int:
        """Choose the quote delimiter and whether interpolation
        applies.
        """
        quote = self.statement[cursor]
        delimiter = quote
        if not verbatim and self.statement.startswith(quote * 3, cursor):
            delimiter = quote * 3
        syntax = self.interpolation_syntax
        preceding = self.statement[max(0, cursor - 2) : cursor]
        interpolate = (
            not raw
            and syntax is not None
            and quote in syntax[1]
            and (syntax[0] != "{" or "$" in preceding)
        )
        return self._string_end(
            cursor=cursor + len(delimiter),
            delimiter=delimiter,
            raw=raw,
            verbatim=verbatim,
            interpolate=interpolate,
        )

    @beartype
    def _string_end(
        self,
        *,
        cursor: int,
        delimiter: str,
        raw: bool,
        verbatim: bool,
        interpolate: bool,
    ) -> int:
        """Follow escapes and interpolation to the closing delimiter."""
        syntax = self.interpolation_syntax if interpolate else None
        while cursor < len(self.statement):
            if (verbatim and self.statement.startswith('""', cursor)) or (
                not raw and not verbatim and self.statement[cursor] == "\\"
            ):
                cursor += 2
            elif self.statement.startswith(delimiter, cursor):
                return cursor + len(delimiter)
            elif (
                syntax is not None
                and syntax[0] == "{"
                and self.statement.startswith("{{", cursor)
            ):
                cursor += 2
            elif syntax is not None and self.statement.startswith(
                syntax[0], cursor
            ):
                cursor = self._expression_end(cursor=cursor + len(syntax[0]))
            else:
                cursor += 1
        return len(self.statement)

    @beartype
    def _expression_end(self, *, cursor: int) -> int:
        """Balance interpolation brackets while skipping nested
        literals.
        """
        closing = ["}"]
        while cursor < len(self.statement):
            end = self._span_end(cursor=cursor)
            if end is not None:
                cursor = end
                continue
            character = self.statement[cursor]
            if character in _OPENING_BRACKETS:
                closing.append(
                    _CLOSING_BRACKETS[_OPENING_BRACKETS.index(character)]
                )
            elif character == closing[-1]:
                _ = closing.pop()
                if len(closing) == 0:
                    return cursor + 1
            elif (
                self.interpolation_syntax == ("{", '"')
                and character == ":"
                and len(closing) == 1
            ):
                # An interpolation format tail is text, not an expression.
                return self._end_after(delimiter="}", cursor=cursor)
            cursor += 1
        return len(self.statement)


@beartype
def split_trailing_line_comments(
    *,
    statement: str,
    prefix: str,
    regex_literals: bool,
    backtick_strings: bool,
    raw_string_prefixes: tuple[str, ...],
    verbatim_strings: bool,
    interpolation_syntax: tuple[str, str] | None,
    quotes: str,
    literal_span_end: LiteralSpanEnd | None,
) -> _TrailingLineComments:
    """Separate trailing line comments from a C-style expression."""
    if prefix not in statement:
        return _TrailingLineComments(code=statement, trailing_comments="")
    return _CommentScanner(
        statement=statement,
        prefix=prefix,
        quotes=frozenset(quotes),
        regex_literals=regex_literals,
        backtick_strings=backtick_strings,
        raw_string_prefixes=raw_string_prefixes,
        verbatim_strings=verbatim_strings,
        interpolation_syntax=interpolation_syntax,
        literal_span_end=literal_span_end,
    ).split()


@beartype
def split_double_quoted_line_comments(
    *, statement: str, prefix: str
) -> _TrailingLineComments:
    """Separate trailing comments where only double quotes delimit strings."""
    return _CommentScanner(
        statement=statement,
        prefix=prefix,
        quotes=frozenset({'"'}),
        regex_literals=False,
        backtick_strings=False,
        raw_string_prefixes=(),
        verbatim_strings=False,
        interpolation_syntax=None,
        literal_span_end=None,
    ).split()


@functools.cache
@beartype
def _skipped_span_pattern(
    *,
    quotes: str,
    line_comment_prefixes: tuple[str, ...],
) -> re.Pattern[str]:
    """Return a pattern matching what a bracket may hide inside.

    A bracket written in a string literal or a comment is text rather
    than structure, so those spans are removed before counting.
    """
    alternatives = [
        rf"{re.escape(pattern=quote)}"
        rf"(?:[^{re.escape(pattern=quote)}\\]|\\.)*"
        rf"{re.escape(pattern=quote)}"
        for quote in quotes
    ]
    alternatives.extend(
        rf"{re.escape(pattern=prefix)}.*" for prefix in line_comment_prefixes
    )
    return re.compile(pattern="|".join(alternatives))


@beartype
def _bracket_delta(
    *,
    line: str,
    quotes: str,
    line_comment_prefixes: tuple[str, ...],
) -> int:
    """Return how many brackets *line* leaves open."""
    code = _skipped_span_pattern(
        quotes=quotes,
        line_comment_prefixes=line_comment_prefixes,
    ).sub(repl="", string=line)
    opened = sum(code.count(bracket) for bracket in _OPENING_BRACKETS)
    closed = sum(code.count(bracket) for bracket in _CLOSING_BRACKETS)
    return opened - closed


@beartype
def split_statements(
    *,
    content: str,
    quotes: str,
    line_comment_prefixes: tuple[str, ...],
) -> list[str]:
    """Return the whole statements *content* holds, blank lines dropped.

    A statement ends where the brackets it opened have all closed, so a
    multiline collection argument keeps the lines it spans.  *quotes*
    names the string delimiters of the target language and
    *line_comment_prefixes* its comment leaders; brackets inside either
    are content rather than structure.
    """
    grouped: list[list[str]] = [[]]
    depth = 0
    for line in content.split(sep="\n"):
        grouped[-1].append(line)
        depth += _bracket_delta(
            line=line,
            quotes=quotes,
            line_comment_prefixes=line_comment_prefixes,
        )
        if depth <= 0:
            depth = 0
            grouped.append([])
    joined = ["\n".join(group) for group in grouped]
    return [statement for statement in joined if statement.strip() != ""]


@beartype
def line_comment_start(
    *,
    line: str,
    quotes: str,
    line_comment_prefixes: tuple[str, ...],
) -> int:
    """Return where *line*'s trailing comment begins, or its length.

    A comment marker inside a string literal is content, so the scan
    steps over string literals to find the real one.
    """
    for match in _skipped_span_pattern(
        quotes=quotes,
        line_comment_prefixes=line_comment_prefixes,
    ).finditer(string=line):
        if match.group()[:1] not in quotes:
            return match.start()
    return len(line)


@beartype
def insert_before_line_comment(
    *,
    statement: str,
    text: str,
    quotes: str,
    line_comment_prefixes: tuple[str, ...],
) -> str:
    """Return *statement* with *text* placed before its comment.

    A separator or terminator written after an inline comment is inside
    the comment, so the parser never sees it (issue #4664).  The
    whitespace between the code and the comment is preserved, so the
    comment stays where it was written.
    """
    lines = statement.split(sep="\n")
    last = lines[-1]
    start = line_comment_start(
        line=last,
        quotes=quotes,
        line_comment_prefixes=line_comment_prefixes,
    )
    code = last[:start].rstrip()
    gap = last[len(code) : start]
    lines[-1] = f"{code}{text}{gap}{last[start:]}"
    return "\n".join(lines)
