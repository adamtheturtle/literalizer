"""Pure Python layout for the Objective-C syntax emitted by Literalizer.

This module does not load or execute a formatter. The independently pinned
clang-format profile is an oracle in development and CI only.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from literalizer.exceptions import SourceLayoutError

_TOKEN = re.compile(
    pattern=(
        "(?P<directive>^[ \\t]*\\#[^\\n]*)|(?P<comment>//"
        '[^\\n]*|/\\*[\\s\\S]*?\\*/)|(?P<string>@?"(?:\\\\.|['
        "^\"\\\\])*\"|\\'(?:\\\\.|[^\\'\\\\])*\\')|(?P<number>0[x"
        "X][0-9a-fA-F]+(?:[uUlL]*)|(?:\\d+(?:\\.\\d*)?|\\."
        "\\d+)(?:[eE][+-]?\\d+)?[fFuUlL]*)|(?P<word>@?[A"
        "-Za-z_]\\w*)|(?P<op>@[\\[({]|==|!=|<=|>=|&&|\\|\\"
        "||<<|>>|\\+\\+|--|->|\\S)"
    ),
    flags=re.MULTILINE,
)


@dataclass
class Token:
    """A lexical token with the source newline retained for comments."""

    text: str
    kind: str
    newline: bool


@dataclass
class Group:
    """A balanced syntax group with a cached flat representation."""

    opening: str
    nodes: list[Node]
    newline: bool
    kind: str
    computed: bool
    flat_value: str | None


CLOSE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "@(": ")",
    "@[": "]",
    "@{": "}",
    "<": ">",
}
type Node = Token | Group


class Layout:
    """Layout state shared by one immutable rendering request."""

    def __init__(self, *, indent_width: int) -> None:
        """Set the indentation width for this rendering."""
        self.indent_width = indent_width

    def _parse(self, *, text: str) -> list[Node]:
        """Read generated source tokens without interpreting string
        contents.
        """
        tokens: list[Token] = []
        end = 0
        for m in _TOKEN.finditer(string=text):
            tokens.append(
                Token(
                    text=m.group(),
                    kind=m.lastgroup if m.lastgroup is not None else "op",
                    newline="\n" in text[end : m.start()],
                )
            )
            end = m.end()

        def block(*, i: int, closing: str | None) -> tuple[list[Node], int]:
            """Read one balanced group and classify initializer braces."""
            out: list[Node] = []
            while i < len(tokens):
                tok = tokens[i]
                if tok.text == closing:
                    return (out, i + 1)
                if tok.text in CLOSE:
                    children, j = block(i=i + 1, closing=CLOSE[tok.text])
                    out.append(
                        Group(
                            opening=tok.text,
                            computed=False,
                            flat_value=None,
                            nodes=children,
                            newline=tok.newline,
                            kind="initializer"
                            if tok.text == "{"
                            and bool(out)
                            and (
                                self._textof(n=out[-1]) == "="
                                or (
                                    len(out) == 1
                                    and isinstance(out[-1], Group)
                                    and (out[-1].opening == "(")
                                )
                            )
                            else "parameters"
                            if tok.text == "<"
                            or (
                                tok.text == "("
                                and j < len(tokens)
                                and (tokens[j].text == "{")
                            )
                            else "normal",
                        )
                    )
                    i = j
                else:
                    out.append(tok)
                    i += 1
            return (out, i)

        return block(i=0, closing=None)[0]

    @staticmethod
    def _split(*, nodes: list[Node], sep: str) -> list[list[Node]]:
        """Split at one group level, retaining nested expressions."""
        parts: list[list[Node]] = [[]]
        for n in nodes:
            if isinstance(n, Token) and n.text == sep:
                parts.append([])
            else:
                parts[-1].append(n)
        return parts

    @staticmethod
    def _textof(*, n: Node) -> str:
        """Return the leading token of a syntax node."""
        return n.text if isinstance(n, Token) else n.opening

    @staticmethod
    def _iscast(*, g: Group) -> bool:
        """Distinguish a generated type cast from ordinary parentheses."""
        if g.opening != "(" or not bool(g.nodes):
            return False
        words = [n.text for n in g.nodes if isinstance(n, Token)]
        return bool(words) and (
            words[0]
            in {
                "const",
                "id",
                "void",
                "double",
                "float",
                "int",
                "unsigned",
                "long",
                "char",
                "BOOL",
                "NSInteger",
                "NSUInteger",
                "Class",
                "instancetype",
            }
            or any(w[0].isupper() for w in words)
        )

    @staticmethod
    def _punctuation_gap(*, previous: str, current: str) -> str | None:
        """Apply token-independent punctuation spacing in precedence order."""
        if current == ":":
            return " "
        if current in {",", ";", ".", "->", ">", "++", "--"}:
            return ""
        if previous == ",":
            return " "
        if previous in {".", "->", "<", "@"} or current == "<":
            return ""
        return None

    def _group_gap(self, *, prev: Node, n: Node, a: str, b: str) -> str | None:
        """Distinguish casts, pointer types, calls, and array
        subscripts.
        """
        if b == "{" and isinstance(prev, Group) and self._iscast(g=prev):
            return ""
        if b == "*":
            return " "
        if a == "*":
            return ""
        if b == "(":
            spaced = a in {
                "if",
                "while",
                "for",
                "switch",
                "return",
                "sizeof",
                "=",
            }
            pointer = (
                isinstance(n, Group)
                and bool(n.nodes)
                and (self._textof(n=n.nodes[0]) == "*")
            )
            return " " if spaced or pointer else ""
        if b == "[":
            subscript = isinstance(prev, Group) or (
                prev.kind == "word" and (a != "return")
            )
            return "" if subscript else " "
        return None

    def _gap(self, *, prev: Node | None, n: Node) -> str:
        """Choose a space without joining identifiers or changing
        operators.
        """
        if prev is None:
            return ""
        a = CLOSE[prev.opening] if isinstance(prev, Group) else prev.text
        b = self._textof(n=n)
        punctuation = self._punctuation_gap(previous=a, current=b)
        if punctuation is not None:
            return punctuation
        grouped = self._group_gap(prev=prev, n=n, a=a, b=b)
        if grouped is not None:
            return grouped
        cast = isinstance(prev, Group) and self._iscast(g=prev)
        unary = a in {"!", "~"} or (
            a in {"+", "-"} and isinstance(prev, Token) and prev.newline
        )
        return "" if cast or unary else " "

    def _flat(self, *, nodes: list[Node]) -> str | None:
        """Return a one-line rendering or signal a hard line."""
        out = ""
        prev: Node | None = None
        before_prev = None
        for n in nodes:
            if isinstance(n, Token):
                if n.kind in {"comment", "directive"}:
                    return None
                val = n.text
            else:
                value = self._flat_group(n=n)
                if value is None:
                    return None
                val = value
            space = self._gap(prev=prev, n=n)
            if (
                isinstance(prev, Token)
                and prev.text in {"-", "+"}
                and (
                    before_prev is None
                    or self._textof(n=before_prev) in {"=", ",", ":", "return"}
                )
            ):
                space = ""
            out += space + val
            before_prev = prev
            prev = n
        return out

    @staticmethod
    def _labels(*, nodes: list[Node]) -> list[int]:
        """Find selector labels at the message's outer scope."""
        return [
            i - 1
            for i, n in enumerate(iterable=nodes)
            if isinstance(n, Token) and n.text == ":" and (i > 0)
        ]

    def _message(
        self, *, g: Group, start: int, anchor: int, width: int, flat_only: bool
    ) -> str | None:
        """Align and wrap an Objective-C selector and its arguments."""
        inds = self._labels(nodes=g.nodes)
        if not bool(inds):
            inner = self._flat(nodes=g.nodes)
            if inner is not None:
                return "[" + inner + "]"
            if flat_only:
                return None
            return (
                "["
                + self._expr(
                    nodes=g.nodes,
                    start=start + 1,
                    anchor=anchor,
                    width=width,
                    suffix=0,
                    container=False,
                )
                + "]"
            )
        receiver = g.nodes[: inds[0]]
        args: list[tuple[str, list[Node]]] = []
        for j, idx in enumerate(iterable=inds):
            end = inds[j + 1] if j + 1 < len(inds) else len(g.nodes)
            args.append((self._textof(n=g.nodes[idx]), g.nodes[idx + 2 : end]))
        rflat = self._flat(nodes=receiver)
        vals = [self._flat(nodes=arg) for _, arg in args]
        if rflat is not None and all(v is not None for v in vals):
            one = (
                "["
                + rflat
                + " "
                + " ".join(
                    (
                        name + ":" + v
                        for (name, _), v in zip(args, vals, strict=True)
                        if v is not None
                    )
                )
                + "]"
            )
            if flat_only or start + len(one) <= width:
                return one
        if flat_only:
            return None
        rec = self._expr(
            nodes=receiver,
            start=start + 1,
            anchor=anchor,
            width=width,
            suffix=0,
            container=False,
        )
        prefix = "[" + rec + " " + args[0][0] + ":"
        colon = (
            start + len(prefix) - 1
            if "\n" not in prefix
            else len(prefix.rsplit(sep="\n", maxsplit=1)[1]) - 1
        )
        out = prefix + self._expr(
            nodes=args[0][1],
            start=colon + 1,
            anchor=anchor,
            width=width,
            suffix=0,
            container=False,
        )
        for name, arg in args[1:]:
            labelcol = max(anchor + 4, colon - len(name))
            out += (
                "\n"
                + " " * labelcol
                + name
                + ":"
                + self._expr(
                    nodes=arg,
                    start=labelcol + len(name) + 1,
                    anchor=anchor,
                    width=width,
                    suffix=0,
                    container=False,
                )
            )
        return out + "]"

    def _group(
        self, *, g: Group, start: int, anchor: int, width: int, suffix: int
    ) -> str:
        """Choose flat or expanded layout within the available width."""
        f = self._flat(nodes=[g])
        if f is not None and start + len(f) + suffix <= width:
            return f
        if g.opening == "[":
            result = self._message(
                g=g, start=start, anchor=anchor, width=width, flat_only=False
            )
            if result is None:
                raise NotImplementedError
            return result
        if g.opening in {"@[", "@{", "{"}:
            return self._collection(g=g, anchor=anchor, width=width)
        return self._arguments(
            g=g, start=start, anchor=anchor, width=width, suffix=suffix
        )

    @staticmethod
    def _display_width(*, value: str) -> int:
        """Count source columns without splitting Unicode characters."""
        return sum(
            0
            if bool(unicodedata.combining(c))
            or unicodedata.category(c) in {"Cf", "Mn", "Me"}
            else 2
            if unicodedata.east_asian_width(c) in {"W", "F"}
            else 1
            for c in value
        )

    def _string_literal(self, *, token: str, start: int, width: int) -> str:
        """Split only at complete character or escape boundaries."""
        prefix = '@"' if token.startswith('@"') else '"'
        body = token[len(prefix) : -1]
        units = re.findall(
            pattern="\\\\(?:x[0-9a-fA-F]+|[0-7]{1,3}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|.)|[^\\\\]",
            string=body,
        )
        capacity = max(1, width - start - len(prefix) - 1)
        chunks: list[str] = []
        part: list[str] = []
        used = 0
        for unit in units:
            size = self._display_width(value=unit)
            if bool(part) and used + size > capacity:
                chunks.append("".join(part))
                part = []
                used = 0
            part.append(unit)
            used += size
        chunks.append("".join(part))
        return ("\n" + " " * start).join(prefix + p + '"' for p in chunks)

    def _expr(
        self,
        *,
        nodes: list[Node],
        start: int,
        anchor: int,
        width: int,
        suffix: int,
        container: bool,
    ) -> str:
        """Render an expression at its actual starting column."""
        parts = self._split(nodes=nodes, sep=",")
        if len(parts) > 1:
            return self._comma_expression(
                parts=parts,
                start=start,
                anchor=anchor,
                width=width,
                suffix=suffix,
            )
        conditional = self._conditional(
            nodes=nodes, start=start, anchor=anchor, width=width, suffix=suffix
        )
        if conditional is not None:
            return conditional
        out = ""
        prev: Node | None = None
        before_prev = None
        question_column: int | None = None
        col = start
        for index, n in enumerate(iterable=nodes):
            space = self._gap(prev=prev, n=n)
            if (
                bool(out)
                and out.rsplit(sep="\n", maxsplit=1)[-1].strip() == ""
            ):
                space = ""
            if (
                isinstance(prev, Token)
                and prev.text in {"-", "+"}
                and (
                    before_prev is None
                    or self._textof(n=before_prev) in {"=", ",", ":", "return"}
                )
            ):
                space = ""
            if (
                isinstance(n, Group)
                and n.kind == "initializer"
                and container
                and (prev is not None)
                and (self._textof(n=prev) == "=")
            ):
                space = "\n" + " " * (anchor + 4)
                col = 0
            out += space
            col += len(space)
            question_column = (
                col
                if isinstance(n, Token) and n.text == "?"
                else question_column
            )
            if isinstance(n, Group):
                tail = self._flat(nodes=nodes[index + 1 :])
                reserve = (
                    len(tail) + len(self._gap(prev=n, n=nodes[index + 1]))
                    if tail is not None
                    and len(tail) > 0
                    and bool(nodes[index + 1 :])
                    else 0
                ) + suffix
                val = self._group(
                    g=n,
                    start=col,
                    anchor=anchor + 4
                    if n.kind == "initializer" and container
                    else anchor,
                    width=width,
                    suffix=reserve,
                )
            elif n.kind == "comment":
                val = self._comment(
                    text=n.text,
                    anchor=anchor,
                    question_column=question_column,
                )
                prev = None
            elif (
                n.kind == "string"
                and (not container)
                and (self._display_width(value=n.text) + col + suffix > width)
            ):
                val = self._string_literal(
                    token=n.text, start=col, width=width - suffix
                )
            else:
                val = n.text
            out += val
            col = (
                col + len(val)
                if "\n" not in val
                else len(val.rsplit(sep="\n", maxsplit=1)[1])
            )
            before_prev = prev
            prev = n
        return out

    def _statements(
        self, *, nodes: list[Node], indent: int, width: int
    ) -> str:
        """Traverse generated scopes without changing statement order."""
        lines: list[str] = []
        pending: list[Node] = []
        for n in nodes:
            if isinstance(n, Token) and n.kind == "directive":
                lines.extend(
                    self._pending_lines(
                        pending=pending, indent=indent, width=width
                    )
                )
                pending = []
                lines.append(n.text.strip())
            elif isinstance(n, Token) and n.kind == "comment":
                if bool(pending):
                    pending.append(n)
                    continue
                if bool(lines) and (not n.newline):
                    lines[-1] += " " + n.text
                else:
                    lines.append(" " * indent + n.text)
            elif (
                isinstance(n, Group)
                and n.opening == "{"
                and (n.kind != "initializer")
            ):
                signature = self._signature(
                    pending=pending, indent=indent, width=width
                )
                lines.append(signature)
                child = self._statements(
                    nodes=n.nodes,
                    indent=indent + self.indent_width,
                    width=width,
                )
                if bool(child):
                    lines.append(child)
                lines.append(" " * indent + "}")
                pending = []
            elif isinstance(n, Token) and n.text == ";":
                pending.append(n)
                line = self._statement(
                    pending=pending, indent=indent, width=width
                )
                if (
                    bool(lines)
                    and (not bool(pending[:-1]))
                    and (lines[-1].strip() == "}")
                ):
                    lines[-1] += ";"
                else:
                    lines.append(line)
                pending = []
            else:
                pending.append(n)
        lines.extend(
            self._pending_lines(pending=pending, indent=indent, width=width)
        )
        return "\n".join(lines)

    def format_code(self, *, code: str, base: int, width: int) -> str:
        """Render complete statements at the enclosing indentation."""
        return self._statements(
            nodes=self._parse(text=code), indent=base, width=width
        )

    def _collection(self, *, g: Group, anchor: int, width: int) -> str:
        """Render vertical entries with legal trailing commas."""
        entries = self._collection_entries(g=g)
        out = g.opening
        child = anchor + (4 if g.opening == "{" else self.indent_width)
        for prefix, p, comments in entries:
            for c in prefix:
                out += "\n" + " " * child + c.text
            row = child
            out += "\n" + " " * row
            if g.opening == "@{":
                out += self._dictionary_entry(p=p, row=row, width=width)
            else:
                out += self._expr(
                    nodes=p,
                    start=row,
                    anchor=row,
                    width=width,
                    container=True,
                    suffix=0,
                )
            out += ","
            for j, c in enumerate(iterable=comments):
                out += (
                    "\n" + " " * child if bool(j) or c.newline else " "
                ) + c.text
        return out + "\n" + " " * anchor + CLOSE[g.opening]

    def _arguments(
        self, *, g: Group, start: int, anchor: int, width: int, suffix: int
    ) -> str:
        """Lay out parameters and call arguments within their scopes."""
        parts = self._split(nodes=g.nodes, sep=",")
        col = start + len(g.opening)
        first_array = (
            len(parts[0]) == 1
            and isinstance(parts[0][0], Group)
            and (parts[0][0].opening in {"@[", "@{"})
        )
        first = parts[0][0] if bool(parts[0]) else None
        single_dict = (
            first_array
            and isinstance(first, Group)
            and (first.opening == "@{")
            and (
                len(
                    [
                        p
                        for p in self._split(nodes=first.nodes, sep=",")
                        if bool(p)
                    ]
                )
                == 1
            )
        )
        first_flat = self._flat(nodes=parts[0])
        broken_first = len(parts) > 1 and (
            (
                first_flat is not None
                and anchor + 4 + len(first_flat) + 1 <= width
                and col + len(first_flat) + 4 > width
            )
            or (
                first_array
                and (not single_dict)
                and (self._flat(nodes=parts[0]) is None)
            )
            or (
                not first_array
                and any(
                    self._flat(nodes=p) is None
                    and (
                        not (
                            len(p) == 1
                            and isinstance(p[0], Group)
                            and (p[0].opening == "@[")
                        )
                    )
                    for p in parts
                )
            )
        )
        if broken_first:
            col = anchor + 4
        last = ""
        out = g.opening + ("\n" + " " * col if broken_first else "")
        current = col
        for i, p in enumerate(iterable=parts):
            new_line = False
            if bool(i):
                if self._pack_argument(
                    kind=g.kind,
                    broken=broken_first,
                    part=p,
                    previous=last,
                    current=current,
                    width=width,
                    suffix=suffix,
                    last=i == len(parts) - 1,
                ):
                    out += ", "
                    current += 2
                else:
                    out += ",\n" + " " * col
                    current = col
                    new_line = True
            last = self._expr(
                nodes=p,
                start=current,
                anchor=anchor
                if len(parts) == 1
                or (i == 0 and single_dict and (not broken_first))
                or (
                    not broken_first
                    and not new_line
                    and not first_array
                    and len(p) == 1
                    and isinstance(p[0], Group)
                    and (p[0].opening == "@[")
                )
                else col,
                width=width,
                suffix=1 + suffix if i == len(parts) - 1 else 1,
                container=False,
            )
            out += last
            current = (
                current + len(last)
                if "\n" not in last
                else len(last.rsplit(sep="\n", maxsplit=1)[1])
            )
        return (
            out.rstrip()
            + (
                "\n" + " " * anchor
                if bool(g.nodes)
                and isinstance(g.nodes[-1], Token)
                and (g.nodes[-1].kind == "comment")
                else ""
            )
            + CLOSE[g.opening]
        )

    def _flat_group(self, *, n: Group) -> str | None:
        """Cache context-independent flat group layout."""
        value: str | None
        if n.computed:
            return n.flat_value
        n.computed = True
        if not bool(n.nodes):
            value = n.opening + CLOSE[n.opening]
        elif n.opening in {"{", "@[", "@{"}:
            return None
        elif n.opening == "[":
            value = self._message(
                g=n, start=0, anchor=0, width=100000, flat_only=True
            )
        else:
            inner = self._flat(nodes=n.nodes)
            value = (
                None if inner is None else n.opening + inner + CLOSE[n.opening]
            )
        n.flat_value = value
        return value

    def _collection_entries(
        self, *, g: Group
    ) -> list[tuple[list[Token], list[Node], list[Token]]]:
        """Keep leading and trailing comment ownership while adding commas."""
        self._ensure_trailing_comma(g=g)
        parts = self._split(nodes=g.nodes, sep=",")
        if not bool(parts[-1]):
            _ = parts.pop()
        entries: list[tuple[list[Token], list[Node], list[Token]]] = []
        for part in parts:
            if (
                bool(entries)
                and bool(part)
                and isinstance(part[0], Token)
                and (part[0].kind == "comment")
                and (not part[0].newline)
            ):
                comment = part.pop(0)
                if not isinstance(comment, Token):
                    raise NotImplementedError
                entries[-1][2].append(comment)
            prefix: list[Token] = []
            while (
                bool(part)
                and isinstance(part[0], Token)
                and (part[0].kind == "comment")
            ):
                comment = part.pop(0)
                if not isinstance(comment, Token):
                    raise NotImplementedError
                prefix.append(comment)
            if bool(part):
                entries.append((prefix, part, []))
            elif bool(prefix) and bool(entries):
                entries[-1][2].extend(prefix)
        return entries

    def _dictionary_entry(self, *, p: list[Node], row: int, width: int) -> str:
        """Wrap a value after its key when the available width requires it."""
        out = ""
        kv = self._split(nodes=p, sep=":")
        key = self._expr(
            nodes=kv[0],
            start=row,
            anchor=row,
            width=width,
            suffix=0,
            container=False,
        )
        valflat = self._flat(nodes=kv[1])
        col = row + len(key) + 3
        if self._move_dictionary_value(
            value=valflat, nodes=kv[1], column=col, row=row, width=width
        ):
            out += (
                key
                + " :\n"
                + " " * (row + 4)
                + self._expr(
                    nodes=kv[1],
                    start=row + 4,
                    anchor=row + 4,
                    width=width,
                    suffix=0,
                    container=False,
                )
            )
        else:
            out += (
                key
                + " : "
                + self._expr(
                    nodes=kv[1],
                    start=col,
                    anchor=row,
                    width=width,
                    container=True,
                    suffix=0,
                )
            )
        return out

    def _comma_expression(
        self,
        *,
        parts: list[list[Node]],
        start: int,
        anchor: int,
        width: int,
        suffix: int,
    ) -> str:
        """Pack comma expressions independently of function argument
        policy.
        """
        result = self._expr(
            nodes=parts[0],
            start=start,
            anchor=anchor,
            width=width,
            suffix=1,
            container=False,
        )
        col = start + len(result)
        for i, p in enumerate(start=1, iterable=parts[1:]):
            val = self._flat(nodes=p)
            if val is not None and col + 2 + len(val) + suffix <= width:
                result += ", " + val
                col += 2 + len(val)
            else:
                col = anchor + 4
                part = self._expr(
                    nodes=p,
                    start=col,
                    anchor=col,
                    width=width,
                    suffix=suffix if i == len(parts) - 1 else 1,
                    container=False,
                )
                result += ",\n" + " " * col + part
                col = len(part.rsplit(sep="\n", maxsplit=1)[-1]) + col
        return result

    @staticmethod
    def _comment(
        *, text: str, anchor: int, question_column: int | None
    ) -> str:
        """Align a commented conditional with its rendered question
        mark.
        """
        target = anchor if question_column is None else question_column
        return text + "\n" + " " * target

    def _conditional(
        self,
        *,
        nodes: list[Node],
        start: int,
        anchor: int,
        width: int,
        suffix: int,
    ) -> str | None:
        """Keep a multiline conditional's branches aligned with its
        value.
        """
        questions = [
            i
            for i, n in enumerate(iterable=nodes)
            if isinstance(n, Token) and n.text == "?"
        ]
        if not bool(questions):
            return None
        question = questions[0]
        if self._flat(nodes=nodes[:question]) is not None:
            return None
        colon = next(
            i
            for i, node in enumerate(iterable=nodes)
            if i > question and isinstance(node, Token) and node.text == ":"
        )
        condition = self._expr(
            nodes=nodes[:question],
            start=start,
            anchor=anchor,
            width=width,
            suffix=0,
            container=False,
        )
        assignments = [
            i
            for i, n in enumerate(iterable=nodes[:question])
            if isinstance(n, Token) and n.text == "="
        ]
        prefix = (
            ""
            if not bool(assignments)
            else self._expr(
                nodes=nodes[: assignments[-1] + 1],
                start=start,
                anchor=anchor,
                width=width,
                suffix=0,
                container=False,
            )
            + " "
        )
        target = start + len(prefix) + 4
        truth = self._expr(
            nodes=nodes[question + 1 : colon],
            start=target + 2,
            anchor=target + 2,
            width=width,
            suffix=0,
            container=False,
        ).rstrip()
        falsehood = self._expr(
            nodes=nodes[colon + 1 :],
            start=target + 2,
            anchor=target + 2,
            width=width,
            suffix=suffix,
            container=False,
        ).rstrip()
        return (
            condition
            + "\n"
            + " " * target
            + "? "
            + truth
            + "\n"
            + " " * target
            + ": "
            + falsehood
        )

    def _ensure_trailing_comma(self, *, g: Group) -> None:
        """Use legal trailing commas to keep nonempty collections vertical."""
        at = len(g.nodes)
        while (
            bool(at)
            and isinstance(g.nodes[at - 1], Token)
            and (g.nodes[at - 1].kind == "comment")
        ):
            at -= 1
        if bool(at) and self._textof(n=g.nodes[at - 1]) != ",":
            g.nodes.insert(at, Token(text=",", kind="op", newline=False))

    def _signature(
        self, *, pending: list[Node], indent: int, width: int
    ) -> str:
        """Break before a function name if its return type cannot share the
        line.
        """
        signature = (
            " " * indent
            + self._expr(
                nodes=pending,
                start=indent,
                anchor=indent,
                width=width,
                suffix=2,
                container=False,
            )
            + " {"
        )
        if (
            "\n" not in signature
            and len(signature) > width
            and bool(pending)
            and isinstance(pending[-1], Group)
            and (pending[-1].opening == "(")
        ):
            name = len(pending) - 2
            signature = (
                " " * indent
                + self._expr(
                    nodes=pending[:name],
                    start=indent,
                    anchor=indent,
                    width=width,
                    suffix=0,
                    container=False,
                )
                + "\n"
                + " " * indent
                + self._expr(
                    nodes=pending[name:],
                    start=indent,
                    anchor=indent,
                    width=width,
                    suffix=2,
                    container=False,
                )
                + " {"
            )
        return signature

    def _statement(
        self, *, pending: list[Node], indent: int, width: int
    ) -> str:
        """Wrap a long assignment before its value."""
        line = " " * indent + self._expr(
            nodes=pending,
            start=indent,
            anchor=indent,
            width=width,
            suffix=0,
            container=False,
        )
        assignments = [
            i
            for i, x in enumerate(iterable=pending)
            if isinstance(x, Token) and x.text == "="
        ]
        if "\n" not in line and len(line) > width and bool(assignments):
            i = assignments[0]
            left = self._expr(
                nodes=pending[:i],
                start=indent,
                anchor=indent,
                width=width,
                suffix=0,
                container=False,
            )
            rhs = self._expr(
                nodes=pending[i + 1 :],
                start=indent + 4,
                anchor=indent + 4,
                width=width,
                suffix=0,
                container=False,
            )
            line = " " * indent + left + " =\n" + " " * (indent + 4) + rhs
        return line

    def _pending_lines(
        self, *, pending: list[Node], indent: int, width: int
    ) -> list[str]:
        """Emit only a nonempty pending statement."""
        if not bool(pending):
            return []
        return [
            " " * indent
            + self._expr(
                nodes=pending,
                start=indent,
                anchor=indent,
                width=width,
                suffix=0,
                container=False,
            )
        ]

    def format_expression(
        self, *, code: str, start: int, anchor: int, width: int
    ) -> str:
        """Render an expression following caller-owned first-line text."""
        nodes = self._parse(text=code)
        if any(
            isinstance(node, Token) and node.text == ";" for node in nodes[:-1]
        ):
            message = "An initial-column context describes one statement"
            raise SourceLayoutError(message)
        return self._expr(
            nodes=nodes,
            start=start,
            anchor=anchor,
            width=width,
            suffix=0,
            container=False,
        )

    def _pack_argument(
        self,
        *,
        kind: str,
        broken: bool,
        part: list[Node],
        previous: str,
        current: int,
        width: int,
        suffix: int,
        last: bool,
    ) -> bool:
        """Pack only parameter lists and LLVM's inline trailing array
        argument.
        """
        array = (
            len(part) == 1
            and isinstance(part[0], Group)
            and (part[0].opening == "@[")
        )
        if "\n" in previous or not (kind == "parameters" or broken or array):
            return False
        value = self._flat(nodes=part)
        if value is None:
            return last and (broken or array)
        return current + 2 + len(value) + (1 + suffix if last else 1) <= width

    def _move_dictionary_value(
        self,
        *,
        value: str | None,
        nodes: list[Node],
        column: int,
        row: int,
        width: int,
    ) -> bool:
        """Move a value when its key leaves too few columns on the
        line.
        """
        if value is None:
            return False
        length = self._display_width(value=value)
        if column + length + 1 <= width:
            return False
        string = (
            len(nodes) == 1
            and isinstance(nodes[0], Token)
            and (nodes[0].kind == "string")
        )
        return row + 4 + length + 1 <= width or string
