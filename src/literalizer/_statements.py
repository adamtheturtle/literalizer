"""Grouping rendered lines back into whole statements.

A file wrapper receives its statements as one string with a newline
between them.  While every statement is one line that is the same thing,
but a collection rendered under
:attr:`~literalizer.CollectionLayout.MULTILINE` spans several, and a
wrapper that puts a prefix or a separator on each line then puts one on
each *part* of a statement instead of on the statement (issue #4548).
"""

import functools
import re

from beartype import beartype

_OPENING_BRACKETS = "([{"
_CLOSING_BRACKETS = ")]}"


@beartype
def split_trailing_line_comments(
    *,
    statement: str,
    prefix: str,
    regex_literals: bool,
    backtick_strings: bool,
) -> tuple[str, str]:
    """Separate trailing line comments from a C-style expression."""
    cursor = len(statement)
    matches = list(
        _c_style_comment_pattern(
            prefix=prefix,
            regex_literals=regex_literals,
            backtick_strings=backtick_strings,
        ).finditer(string=statement)
    )
    for match in reversed(matches):
        if not match.group().startswith(prefix):
            break
        if statement[match.end() : cursor].strip() != "":
            break
        cursor = match.start()
    if cursor == len(statement):
        return statement, ""
    code = statement[:cursor].rstrip()
    return code, statement[len(code) :]


@functools.cache
@beartype
def _c_style_comment_pattern(
    *, prefix: str, regex_literals: bool, backtick_strings: bool
) -> re.Pattern[str]:
    """Match literals and comments without treating quoted markers as
    comments.
    """
    alternatives = [
        (
            r'R"(?P<raw_delimiter>[^ ()\\\t\r\n]{0,16})\('
            r'[\s\S]*?\)(?P=raw_delimiter)"'
        ),
        r"(?P<triple_quote>\"\"\"|''')[\s\S]*?(?P=triple_quote)",
        r'"(?:[^"\\]|\\[\s\S])*"',
        r"'(?:[^'\\]|\\[\s\S])*'",
        r"/\*[\s\S]*?\*/",
        rf"{re.escape(pattern=prefix)}[^\n]*",
    ]
    if regex_literals:
        alternatives.append(r"~/(?:[^/\\]|\\[\s\S])*/[a-z]*")
    if backtick_strings:
        alternatives.append(r"`[^`]*`")
    return re.compile(pattern="|".join(alternatives))


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
