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
    raw_string_prefixes: tuple[str, ...],
    verbatim_strings: bool,
    interpolation_syntax: tuple[str, str] | None,
) -> tuple[str, str]:
    """Separate trailing line comments from a C-style expression."""
    cursor = len(statement)
    pattern = _c_style_comment_pattern(
        prefix=prefix,
        regex_literals=regex_literals,
        backtick_strings=backtick_strings,
        raw_string_prefixes=raw_string_prefixes,
        verbatim_strings=verbatim_strings,
    )
    matches = _c_style_comment_matches(
        statement=statement,
        pattern=pattern,
        interpolation_syntax=interpolation_syntax,
        verbatim_strings=verbatim_strings,
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


def _c_style_comment_matches(
    *,
    statement: str,
    pattern: re.Pattern[str],
    interpolation_syntax: tuple[str, str] | None,
    verbatim_strings: bool,
) -> list[re.Match[str]]:
    """Skip complete interpolated strings before locating comments."""
    if (
        interpolation_syntax is None
        or interpolation_syntax[0] not in statement
    ):
        return list(pattern.finditer(string=statement))
    matches: list[re.Match[str]] = []
    cursor = 0
    while (match := pattern.search(string=statement, pos=cursor)) is not None:
        matches.append(match)
        cursor = _literal_span_end(
            statement=statement,
            match=match,
            pattern=pattern,
            interpolation_syntax=interpolation_syntax,
            verbatim_strings=verbatim_strings,
        )
    return matches


def _literal_span_end(
    *,
    statement: str,
    match: re.Match[str],
    pattern: re.Pattern[str],
    interpolation_syntax: tuple[str, str],
    verbatim_strings: bool,
) -> int:
    """Extend a quoted span across nested interpolation expressions."""
    literal = match.group()
    interpolation_start, quotes = interpolation_syntax
    if literal[:1] not in quotes and not literal.startswith("@"):
        return match.end()
    quote_start = match.start()
    if literal.startswith("@"):
        quote_start += literal.index('"')
    preceding = statement[max(0, quote_start - 2) : quote_start]
    if interpolation_start == "{" and "$" not in preceding:
        return match.end()
    if interpolation_start not in literal:
        return match.end()
    verbatim = verbatim_strings and "@" in preceding
    quote = statement[quote_start]
    delimiter = quote
    if not verbatim and statement.startswith(quote * 3, quote_start):
        delimiter = quote * 3
    return _interpolated_string_end(
        statement=statement,
        cursor=quote_start + len(delimiter),
        delimiter=delimiter,
        verbatim=verbatim,
        pattern=pattern,
        interpolation_syntax=interpolation_syntax,
        verbatim_strings=verbatim_strings,
    )


def _string_escape_width(
    *, statement: str, cursor: int, verbatim: bool
) -> int:
    """Return how many characters belong to a string escape."""
    if verbatim and statement.startswith('""', cursor):
        return 2
    if not verbatim and statement[cursor] == "\\":
        return 2
    return 0


def _interpolated_string_end(
    *,
    statement: str,
    cursor: int,
    delimiter: str,
    verbatim: bool,
    pattern: re.Pattern[str],
    interpolation_syntax: tuple[str, str],
    verbatim_strings: bool,
) -> int:
    """Find a string's closing delimiter outside interpolation."""
    interpolation_start = interpolation_syntax[0]
    while cursor < len(statement):
        escape_width = _string_escape_width(
            statement=statement, cursor=cursor, verbatim=verbatim
        )
        if escape_width != 0:
            cursor += escape_width
        elif statement.startswith(delimiter, cursor):
            return cursor + len(delimiter)
        elif interpolation_start == "{" and statement.startswith("{{", cursor):
            cursor += 2
        elif statement.startswith(interpolation_start, cursor):
            cursor = _interpolation_expression_end(
                statement=statement,
                cursor=cursor + len(interpolation_start),
                pattern=pattern,
                interpolation_syntax=interpolation_syntax,
                verbatim_strings=verbatim_strings,
            )
        else:
            cursor += 1
    return len(statement)


def _interpolation_expression_end(
    *,
    statement: str,
    cursor: int,
    pattern: re.Pattern[str],
    interpolation_syntax: tuple[str, str],
    verbatim_strings: bool,
) -> int:
    """Balance expression delimiters while skipping quoted contents."""
    interpolation_start = interpolation_syntax[0]
    closing = ["}"]
    while cursor < len(statement):
        match = pattern.match(string=statement, pos=cursor)
        if match is not None:
            cursor = _literal_span_end(
                statement=statement,
                match=match,
                pattern=pattern,
                interpolation_syntax=interpolation_syntax,
                verbatim_strings=verbatim_strings,
            )
            continue
        character = statement[cursor]
        if character in _OPENING_BRACKETS:
            closing.append(
                _CLOSING_BRACKETS[_OPENING_BRACKETS.index(character)]
            )
        elif character == closing[-1]:
            _ = closing.pop()
            if len(closing) == 0:
                return cursor + 1
        elif (
            interpolation_start == "{"
            and character == ":"
            and len(closing) == 1
        ):
            # A C# format tail is text, including slash comment markers.
            end = statement.find("}", cursor)
            return len(statement) if end == -1 else end + 1
        cursor += 1
    return len(statement)


@functools.cache
@beartype
def _c_style_comment_pattern(
    *,
    prefix: str,
    regex_literals: bool,
    backtick_strings: bool,
    raw_string_prefixes: tuple[str, ...],
    verbatim_strings: bool,
) -> re.Pattern[str]:
    """Match literals and comments without treating quoted markers as
    comments.
    """
    raw_prefix = "|".join(
        re.escape(pattern=marker) for marker in raw_string_prefixes
    )
    alternatives: list[str] = []
    if raw_prefix != "":
        alternatives.append(
            rf"(?:{raw_prefix})"
            r"(?:(?P<raw_triple_quote>\"\"\"|''')"
            r"[\s\S]*?(?P=raw_triple_quote)|\"[^\"]*\"|'[^']*')"
        )
    if verbatim_strings:
        alternatives.append(r'@\$?"(?:[^"]|"")*"')
    alternatives.extend(
        [
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
    )
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
