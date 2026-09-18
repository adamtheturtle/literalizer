"""Parse JSON, JSONC, JSON5, YAML, and TOML input into ``Value`` data."""

import dataclasses
import datetime
import decimal
import enum
import json
import math
import re
import sys
import threading
from collections.abc import Callable, Iterable, Mapping
from typing import Protocol, assert_never, runtime_checkable

import json5
import tomlkit
from beartype import beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import (
    CommentedOrderedMap,
    CommentedSet,
    TaggedScalar,
)
from ruamel.yaml.error import YAMLError
from ruamel.yaml.events import (
    AliasEvent,
    CollectionEndEvent,
    CollectionStartEvent,
    ScalarEvent,
)
from tomlkit.exceptions import TOMLKitError
from tomlkit.items import Float as TomlFloat
from tomlkit.items import Integer as TomlInteger
from tomlkit.toml_document import TOMLDocument
from typing_extensions import TypeIs

from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    ExcessiveIntegerDigitsError,
    JSON5ParseError,
    JSONCParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)

type YamlCoercible = (
    Scalar
    | list[YamlCoercible]
    | tuple[Scalar | TaggedScalar, YamlCoercible]
    | dict[Scalar | TaggedScalar, YamlCoercible]
    | CommentedOrderedMap
    | CommentedSet
    | TaggedScalar
)

_HIGH_SURROGATE_START = 0xD800
_LOW_SURROGATE_END = 0xDFFF


@runtime_checkable
class _ParserMark(Protocol):
    """Line and column metadata exposed by parser exceptions."""

    line: int
    column: int


@beartype
def _parser_mark(*, exc: Exception) -> _ParserMark | None:
    """Return parser position metadata when an exception provides it."""
    mark = vars(exc).get("problem_mark")
    if isinstance(mark, _ParserMark):
        return mark
    return None


@runtime_checkable
class _YamlScalarToken(Protocol):
    """Plain scalar token data exposed by the ruamel scanner."""

    value: str
    style: str | None


class _YamlScalarNode(Protocol):
    """Scalar node value exposed to a ruamel constructor."""

    value: str


class _YamlConstructor(Protocol):
    """Constructor operations Literalizer configures on a YAML parser."""

    yaml_constructors: Mapping[
        str,
        Callable[[object, _YamlScalarNode], object],
    ]

    def add_constructor(
        self,
        tag: str,
        constructor: Callable[[object, _YamlScalarNode], object],
    ) -> None:
        """Register *constructor* for *tag*."""
        raise NotImplementedError


@runtime_checkable
class _Yaml(Protocol):
    """The ruamel operations used across Literalizer and its tests."""

    constructor: _YamlConstructor

    def scan(self, stream: object) -> Iterable[object]:
        """Yield tokens from *stream*."""
        raise NotImplementedError

    def parse(self, stream: object) -> Iterable[object]:
        """Yield parser events from *stream*."""
        raise NotImplementedError

    def load(self, stream: object) -> object:
        """Load one document from *stream*."""
        raise NotImplementedError

    def dump(self, data: object, stream: object) -> None:
        """Write *data* to *stream*."""
        raise NotImplementedError


@beartype
def require_yaml(*, yaml: object) -> _Yaml:
    """Validate the ruamel surface whose annotations currently return
    Any.
    """
    if isinstance(yaml, _Yaml):
        return yaml
    raise NotImplementedError


@runtime_checkable
class _AnchoredYamlEvent(Protocol):
    """Anchor metadata consumed from ruamel parser events."""

    anchor: str | None


@runtime_checkable
class _PositionedTomlError(Protocol):
    """A tomlkit exception carrying its parser cursor."""

    line: int
    col: int


class _DuplicateJSONKeyError(ValueError):
    """A JSON object contains the same member name more than once."""


@beartype
def _json_object_without_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    """Build a JSON object while rejecting repeated member names."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            msg = f"duplicate key {key!r}"
            raise _DuplicateJSONKeyError(msg)
        result[key] = value
    return result


class InputFormat(enum.Enum):
    """Supported input serialization formats.

    YAML and TOML comments are preserved for rendering in the target
    language. JSON, JSONC and JSON5 are parsed as plain data, so their
    comments are discarded.
    """

    JSON = enum.auto()
    JSONC = enum.auto()
    JSON5 = enum.auto()
    YAML = enum.auto()
    TOML = enum.auto()


@beartype
@dataclasses.dataclass(frozen=True)
class ParsedPlain:
    """Result of parsing JSON, JSONC or JSON5 input as plain data."""

    data: Value


@beartype
@dataclasses.dataclass(frozen=True)
class ParsedYaml:
    """Result of parsing a YAML input string."""

    data: Value
    raw_data: object
    needs_comment_resolve: bool
    """Whether the YAML comment-resolution phase must run.

    False for the YAML fast path (no comment or tag markers in the
    source).  When False, ``raw_data`` carries no round-trip metadata
    and must not be passed to ``resolve_yaml_comments``.
    """


@beartype
@dataclasses.dataclass(frozen=True)
class ParsedToml:
    """Result of parsing a TOML input string."""

    data: Value
    toml_doc: TOMLDocument


ParsedInput = ParsedPlain | ParsedYaml | ParsedToml


@beartype
def _find_surrogate(*, data: Value) -> str | None:
    """Return the first UTF-16 surrogate code point in *data*, if any.

    Python strings can contain surrogate code points even though they
    are not Unicode scalar values and cannot be encoded as strict
    UTF-8.  Some of the input parsers accept them in values or mapping
    keys, so inspect the complete parsed tree before any target-language
    formatter sees it.
    """
    match data:
        case str():
            return next(
                (
                    character
                    for character in data
                    if (
                        _HIGH_SURROGATE_START
                        <= ord(character)
                        <= _LOW_SURROGATE_END
                    )
                ),
                None,
            )
        case dict():
            for key, value in data.items():
                for child in (key, value):
                    if (surrogate := _find_surrogate(data=child)) is not None:
                        return surrogate
            return None
        case list() | set():
            for item in data:
                if (surrogate := _find_surrogate(data=item)) is not None:
                    return surrogate
            return None
        case _:
            return None


@beartype
def _format_parse_error(
    *, input_format: InputFormat, detail: str
) -> ParseError:
    """Build a format-specific parse error with exhaustive dispatch."""
    match input_format:
        case InputFormat.JSON:
            return JSONParseError(f"Invalid JSON: {detail}")
        case InputFormat.JSONC:
            return JSONCParseError(f"Invalid JSONC: {detail}")
        case InputFormat.JSON5:
            return JSON5ParseError(f"Invalid JSON5: {detail}")
        case InputFormat.YAML:
            return YAMLParseError(f"Invalid YAML: {detail}")
        case InputFormat.TOML:
            return TOMLParseError(f"Invalid TOML: {detail}")
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _surrogate_parse_error(
    *,
    input_format: InputFormat,
    surrogate: str,
) -> ParseError:
    """Build the format-specific error for an invalid surrogate."""
    return _format_parse_error(
        input_format=input_format,
        detail=(
            f"input contains unpaired UTF-16 surrogate U+{ord(surrogate):04X}"
        ),
    )


@beartype
def recursion_parse_error(*, input_format: InputFormat) -> ParseError:
    """Build the format-specific error for excessively nested input."""
    return _format_parse_error(
        input_format=input_format,
        detail="input exceeds the supported nesting depth",
    )


@beartype
def unwrap_yaml_scalar(*, value: Scalar | TaggedScalar) -> Scalar:
    """Convert a *ruamel.yaml* scalar wrapper to its plain Python type.

    The round-trip loader returns subclasses (``ScalarInt``, ``HexInt``,
    ``ScalarFloat``, ``LiteralScalarString``, ``TimeStamp``, ...) that
    preserve source-style metadata.  The literalizer's type-inference
    paths compare ``type(value)`` against the plain Python classes,
    so these wrappers are demoted to
    ``int``/``float``/``str``/``datetime`` before they reach those code
    paths.  Built-in constructors short-circuit when given an
    already-plain instance, so this is essentially free for unwrapped
    values.  YAML dates parse as plain :class:`date` already, so they
    pass through unchanged.
    """
    # ``bool`` and ``datetime.datetime`` come before their bases (``int``
    # and ``date``) because match arms test class membership in order.
    # ``ruamel`` always returns its own ``TimeStamp`` subclass for
    # datetimes, so we always reconstruct.
    if isinstance(value, TaggedScalar):
        # ``TaggedScalar.__str__`` returns ``value`` but avoids its unknown
        # upstream type until https://sourceforge.net/p/ruamel-yaml/tickets/571/
        # is released.
        value = str(object=value)
    match value:
        case bool():
            return value
        case int():
            return value.real
        case float():
            return value.real
        case str():
            return str(object=value)
        case datetime.datetime():
            return datetime.datetime(
                year=value.year,
                month=value.month,
                day=value.day,
                hour=value.hour,
                minute=value.minute,
                second=value.second,
                microsecond=value.microsecond,
                tzinfo=value.tzinfo,
            )
        case datetime.date() | datetime.time() | bytes() | None:
            return value
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _is_object_dict(value: object, /) -> TypeIs[dict[object, object]]:
    """Return whether a value is a dictionary with object-typed
    contents.
    """
    return isinstance(value, dict)


@beartype
def _is_object_list(value: object, /) -> TypeIs[list[object]]:
    """Return whether a value is a list with object-typed contents."""
    return isinstance(value, list)


@beartype
def _is_object_sequence(
    value: object,
    /,
) -> TypeIs[list[object] | set[object]]:
    """Return whether a value is a list or set with object-typed
    contents.
    """
    return isinstance(value, (list, set))


@beartype
def _is_object_pair(
    value: object,
    /,
) -> TypeIs[tuple[object, object]]:
    """Return whether a value is a ``!!pairs`` entry."""
    return isinstance(value, tuple)


@beartype
def _is_object_commented_set(value: object, /) -> TypeIs[Iterable[object]]:
    """Return whether *value* is an object-typed ruamel YAML set."""
    return isinstance(value, CommentedSet)


@beartype
def _validate_yaml_mapping_key(*, key: object) -> None:
    """Reject one non-scalar YAML mapping or set key."""
    if _is_yaml_scalar(key):
        return
    msg = (
        "Invalid YAML: mapping keys must be scalar values; "
        f"got {type(key).__name__}"
    )
    raise YAMLParseError(msg)


@beartype
def _is_yaml_scalar(value: object, /) -> TypeIs[Scalar | TaggedScalar]:
    """Return whether *value* is a scalar produced by ruamel."""
    return isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
            datetime.date,
            datetime.datetime,
            datetime.time,
            bytes,
            TaggedScalar,
            type(None),
        ),
    )


@beartype
def _is_yaml_coercible(data: object, /) -> TypeIs[YamlCoercible]:
    """Validate and narrow one recursively loaded YAML value."""
    if _is_yaml_scalar(data):
        return True
    if _is_object_dict(data):
        for key, value in data.items():
            _validate_yaml_mapping_key(key=key)
            if not _is_yaml_coercible(value):
                raise NotImplementedError
        return True
    if _is_object_commented_set(data):
        for key in data:
            _validate_yaml_mapping_key(key=key)
        return True
    if _is_object_pair(data):
        pair_key, pair_value = data
        _validate_yaml_mapping_key(key=pair_key)
        return _is_yaml_coercible(pair_value)
    if _is_object_sequence(data):
        return all(_is_yaml_coercible(item) for item in data)
    raise NotImplementedError


@beartype
def _require_yaml_data(*, data: object) -> YamlCoercible:
    """Return validated parser data or reject an unsupported value."""
    if _is_yaml_coercible(data):
        return data
    raise NotImplementedError


@beartype
def _unwrap_yaml_data(*, data: YamlCoercible) -> Value:
    """Recursively unwrap ruamel YAML wrappers to plain Python types.

    The round-trip loader returns ``CommentedOrderedMap`` for YAML
    ``!!omap`` nodes; those are converted to literalizer's own
    :class:`OrderedMap` so ordered-map detection in :func:`_literalize`
    does not depend on the ruamel class hierarchy.  Other mappings come
    through as ``CommentedMap`` and are demoted to plain ``dict``.
    :class:`CommentedSet` does not subclass :class:`set`, so
    it is converted as well.  Scalar leaves (including dict keys) are
    unwrapped to plain Python types so type-based dispatch sees
    ``int`` rather than ``ScalarInt`` and friends.

    Non-string dict keys are preserved as their native scalar type;
    languages that cannot represent them are gated by
    :attr:`Language.supports_non_string_dict_keys` in
    :mod:`literalizer._literalize`.
    """
    if isinstance(
        data,
        (
            TaggedScalar,
            bool,
            int,
            float,
            str,
            datetime.datetime,
            datetime.date,
            datetime.time,
            bytes,
            type(None),
        ),
    ):
        return unwrap_yaml_scalar(value=data)
    # ``CommentedOrderedMap`` is a ``dict`` subclass, but represents
    # ``!!omap`` and must become an ``OrderedMap`` rather than a plain dict.
    if isinstance(data, CommentedOrderedMap):
        omap_src: dict[Scalar | TaggedScalar, YamlCoercible] = dict(data)
        return OrderedMap(
            [
                (
                    unwrap_yaml_scalar(value=k),
                    _unwrap_yaml_data(data=v),
                )
                for k, v in omap_src.items()
            ]
        )
    # ``CommentedMap`` and ``CommentedSeq`` are subclasses of ``dict`` and
    # ``list`` respectively, so ordinary collection checks unwrap them too.
    if isinstance(data, dict):
        unwrapped: dict[Scalar, Value] = {
            unwrap_yaml_scalar(value=k): _unwrap_yaml_data(data=v)
            for k, v in data.items()
        }
        return unwrapped
    if isinstance(data, list):
        return [_unwrap_yaml_data(data=item) for item in data]
    if isinstance(data, tuple):
        # A ``!!pairs`` node resolves to a list of two-tuples.  The tag is
        # defined as a sequence of single-key mappings, and unlike ``!!omap``
        # it admits a repeated key, so each pair becomes its own mapping
        # rather than one merged map (issue #3922).
        pair_key, pair_value = data
        return {
            unwrap_yaml_scalar(value=pair_key): _unwrap_yaml_data(
                data=pair_value
            )
        }
    members: set[Scalar | TaggedScalar] = set(data)
    return {unwrap_yaml_scalar(value=item) for item in members}


class _InvalidJSONConstantError(ValueError):
    """Raised when strict JSON contains NaN or infinity."""


class _FiniteFloatRangeError(ValueError):
    """Raised when a finite token cannot survive binary64 conversion."""


@beartype
def _parse_finite_float(value: str) -> float:
    """Convert *value* without silent overflow or underflow."""
    normalized = value.replace("_", "")
    exact = decimal.Decimal(value=normalized)
    converted = float(normalized)
    if exact.is_finite() and (
        math.isinf(converted) or (converted == 0 and exact != 0)
    ):
        msg = f"finite numeric token {value!r} is outside binary64 range"
        raise _FiniteFloatRangeError(msg)
    return converted


_DECIMAL_BASE = 10

_BITS_PER_DECIMAL_DIGIT_FLOOR = 3
"""A conservative lower bound on the bits one decimal digit carries.

An integer of at most ``limit * 3`` bits is below ``10 ** limit``, so it
is always inside the interpreter's conversion limit and needs no check.
"""


@beartype
def reject_excessive_integer_digits(*, value: int) -> None:
    """Reject an integer the interpreter refuses to write out as text.

    CPython caps ``int``-to-``str`` conversion and raises a bare
    ``ValueError`` naming ``sys.set_int_max_str_digits``, which
    describes the interpreter rather than the input (issue #4558).
    """
    limit = sys.get_int_max_str_digits()
    if limit == 0:
        return
    if value.bit_length() <= limit * _BITS_PER_DECIMAL_DIGIT_FLOOR:
        return
    try:
        _ = str(object=value)
    except ValueError as exc:
        raise ExcessiveIntegerDigitsError(limit=limit) from exc


@beartype
def reject_excessive_decimal_token(*, token: str) -> None:
    """Reject a decimal integer token too wide to write back out.

    Checked on the spelling rather than on the value, because ``int``
    refuses a wide token with the same bare ``ValueError`` that writing
    one out raises, so there is no value to inspect (issue #4558).  A
    token that is not a plain run of decimal digits is left alone: a
    float or a non-decimal base carries its own magnitude.
    """
    limit = sys.get_int_max_str_digits()
    digits = token.lstrip("+-").replace("_", "").lstrip("0")
    if limit != 0 and len(digits) > limit and digits.isdigit():
        raise ExcessiveIntegerDigitsError(limit=limit)


@beartype
def _parse_integer_preserving_negative_zero(value: str) -> int | float:
    """Parse an integer token while retaining negative zero's sign."""
    if value == "-0":
        return -0.0
    reject_excessive_decimal_token(token=value)
    return int(value, base=_DECIMAL_BASE)


@beartype
def _parse_json5_integer(  # noqa: NOD001
    value: str, base: int = 10
) -> int | float:
    """Parse a JSON5 integer token, decimal or hexadecimal.

    ``json5`` calls this hook with the number base for a hexadecimal
    token (``0xdeadbeef``) and without one for a decimal token, so the
    parameter carries the default the library relies on rather than
    being passed explicitly (issue #3921).
    """
    if base != _DECIMAL_BASE:
        parsed = int(value, base=base)
        reject_excessive_integer_digits(value=parsed)
        return parsed
    return _parse_integer_preserving_negative_zero(value=value)


@beartype
def _validate_yaml_float_tokens(*, source: str) -> None:
    """Check plain YAML numeric tokens before their value is rounded."""
    if "e" not in source.lower():
        return
    tokens = get_yaml().scan(stream=source)
    for token in tokens:
        if not isinstance(token, _YamlScalarToken) or token.style is not None:
            continue
        value = token.value
        if (
            re.fullmatch(
                pattern=(
                    r"[-+]?(?:[0-9][0-9_]*)(?:\.[0-9_]*)?"
                    r"[eE][-+]?[0-9][0-9_]*"
                ),
                string=value,
            )
            is not None
        ):
            _ = _parse_finite_float(value=value)


@beartype
def _reject_json_constant(value: str) -> Value:
    """Reject Python's non-standard JSON numeric constants."""
    msg = f"Invalid JSON constant: {value}"
    raise _InvalidJSONConstantError(msg)


@beartype
def _parse_json_data(*, source: str, input_format: InputFormat) -> ParsedInput:
    """Parse JSON syntax with the error type of *input_format*."""
    try:
        data = json.loads(
            s=source,
            object_pairs_hook=_json_object_without_duplicate_keys,
            parse_constant=_reject_json_constant,
            parse_float=_parse_finite_float,
            parse_int=_parse_integer_preserving_negative_zero,
        )
    except (
        _DuplicateJSONKeyError,
        _InvalidJSONConstantError,
        _FiniteFloatRangeError,
    ) as exc:
        raise _format_parse_error(
            input_format=input_format, detail=str(object=exc)
        ) from exc
    except json.JSONDecodeError as exc:
        error_type = (
            JSONParseError
            if input_format == InputFormat.JSON
            else JSONCParseError
        )
        message = (
            f"Invalid {input_format.name}: {exc.msg} "
            f"at line {exc.lineno} column {exc.colno}"
        )
        raise error_type(
            message,
            line=exc.lineno,
            column=exc.colno,
        ) from exc
    return ParsedPlain(data=data)


@beartype
def _parse_json(*, source: str) -> ParsedInput:
    """Parse a JSON string into a ``ParsedInput``."""
    return _parse_json_data(source=source, input_format=InputFormat.JSON)


@beartype
def _jsonc_comment_end(*, source: str, index: int) -> int | None:
    """Return the end of a comment starting at *index*, if present."""
    if index + 1 >= len(source):
        return None
    next_char = source[index + 1]
    if next_char == "/":
        end = index + 2
        while end < len(source) and source[end] not in "\r\n":
            end += 1
        return end
    if next_char != "*":
        return None
    close = source.find("*/", index + 2)
    if close == -1:
        prefix = source[:index]
        line = len(re.findall(pattern=r"\r\n|\r|\n", string=prefix)) + 1
        column = index - max(prefix.rfind("\n"), prefix.rfind("\r"))
        message = (
            f"Invalid JSONC: unterminated comment "
            f"at line {line} column {column}"
        )
        raise JSONCParseError(message, line=line, column=column)
    return close + 2


@beartype
def _strip_jsonc_comments(*, source: str) -> str:
    """Replace comments with spaces while keeping JSON error positions."""
    result = list(source)
    index = 0
    in_string = False
    while index < len(source):
        char = source[index]
        if in_string:
            if char == "\\":
                index += 2
                continue
            if char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            index += 1
            continue
        if char == "/":
            end = _jsonc_comment_end(source=source, index=index)
            if end is not None:
                for position in range(index, end):
                    if source[position] not in "\r\n":
                        result[position] = " "
                index = end
                continue
        index += 1
    return "".join(result)


@beartype
def _parse_jsonc(*, source: str) -> ParsedInput:
    """Parse JSON with comments, retaining JSON's strict syntax."""
    return _parse_json_data(
        source=_strip_jsonc_comments(source=source),
        input_format=InputFormat.JSONC,
    )


type _Json5Value = (
    str
    | int
    | float
    | bool
    | list[_Json5Value]
    | dict[str, _Json5Value]
    | None
)
"""The shape ``json5.loads`` returns: its object keys are always
strings.
"""


@beartype
def _combine_surrogate_pairs_in_text(*, text: str) -> str:
    r"""Return *text* with well-formed UTF-16 surrogate pairs combined.

    The ``json5`` package leaves a ``\uD83D\uDE00`` escape pair as two
    separate code points, which the shared lone-surrogate check then
    refuses even though the pair is well formed.  Re-encoding through
    UTF-16 joins a pair and leaves a genuinely lone surrogate alone, so
    that check still catches one (issue #4519).
    """
    return text.encode(encoding="utf-16", errors="surrogatepass").decode(
        encoding="utf-16",
        errors="surrogatepass",
    )


@beartype
def _combine_surrogate_pairs(*, data: _Json5Value) -> Value:
    """Return *data* with every string's surrogate pairs combined."""
    match data:
        case str():
            return _combine_surrogate_pairs_in_text(text=data)
        case dict():
            combined: dict[Scalar, Value] = {}
            for key, value in data.items():
                combined_key = _combine_surrogate_pairs_in_text(text=key)
                # Two keys spelled differently -- one as the astral
                # character, one as its escape pair -- name the same
                # member once combined.  The JSON parser calls that a
                # duplicate, so this one does too rather than silently
                # keeping the last (issue #4519).
                if combined_key in combined:
                    msg = f"duplicate key {combined_key!r}"
                    raise _format_parse_error(
                        input_format=InputFormat.JSON5,
                        detail=msg,
                    )
                combined[combined_key] = _combine_surrogate_pairs(data=value)
            return combined
        case list():
            return [_combine_surrogate_pairs(data=item) for item in data]
        case _:
            return data


_JSON5_STRING_OR_COMMENT = re.compile(
    pattern=(
        r"\"(?:[^\"\\]|\\.)*\""
        r"|'(?:[^'\\]|\\.)*'"
        r"|//[^\n\r\u2028\u2029]*"
        r"|/\*.*?\*/"
    ),
    flags=re.DOTALL,
)

_JSON5_ESCAPE_OR_SEPARATOR = re.compile(
    pattern=r"\\.|[\u2028\u2029]",
    flags=re.DOTALL,
)

_JSON5_RAW_LINE_SEPARATORS = {
    "\u2028": "\\u2028",
    "\u2029": "\\u2029",
}


@beartype
def escape_json5_line_separators(*, source: str) -> str:
    r"""Escape raw U+2028 and U+2029 inside JSON5 string literals.

    JSON5 allows both of them raw inside a string, precisely so that
    every JSON document is also a JSON5 document, but the ``json5``
    package refuses one while reading the string.  Escaping them
    before the parse restores the guarantee, and the parser turns the
    escapes back into the same two characters (issue #4518).

    Outside a string both are line terminators, which end a ``//``
    comment, so only the ones a string literal encloses are rewritten.
    """
    if not any(
        separator in source for separator in _JSON5_RAW_LINE_SEPARATORS
    ):
        return source

    def _escape_separator(match: re.Match[str]) -> str:
        """Return the escape for a bare separator, or the text as-is."""
        return _JSON5_RAW_LINE_SEPARATORS.get(match.group(), match.group())

    def _escape_token(match: re.Match[str]) -> str:
        """Return the matched token with any enclosed separator
        escaped.
        """
        token = match.group()
        if token[0] not in {"'", '"'}:
            return token
        # A backslash before a separator is a line continuation, which
        # escaping the separator would turn into an escaped backslash
        # followed by the text "u2028", so escape pairs are matched
        # first and passed through whole.
        return _JSON5_ESCAPE_OR_SEPARATOR.sub(
            repl=_escape_separator,
            string=token,
        )

    return _JSON5_STRING_OR_COMMENT.sub(repl=_escape_token, string=source)


@beartype
def _parse_json5(*, source: str) -> ParsedInput:
    """Parse a JSON5 string into a ``ParsedInput``."""
    try:
        data = json5.loads(
            s=escape_json5_line_separators(source=source),
            allow_duplicate_keys=False,
            parse_float=_parse_finite_float,
            parse_int=_parse_json5_integer,
        )
    except ValueError as exc:
        message = f"Invalid JSON5: {exc}"
        position = re.search(
            pattern=r"<string>:(?P<line>\d+).* column (?P<column>\d+)",
            string=str(object=exc),
        )
        effective_line = None
        if position is not None:
            effective_line = int(position["line"])
        effective_column = None
        if position is not None:
            effective_column = int(position["column"])
        raise JSON5ParseError(
            message,
            line=effective_line,
            column=(effective_column),
        ) from exc
    return ParsedPlain(data=_combine_surrogate_pairs(data=data))


@beartype
def _configure_negative_zero_yaml_constructor(*, ruamel_yaml: _Yaml) -> None:
    """Teach a ruamel loader to retain signed integer zero as ``-0.0``."""
    tag = "tag:yaml.org,2002:int"
    constructor = ruamel_yaml.constructor
    original = constructor.yaml_constructors[tag]

    def _construct(constructor_obj: object, node: _YamlScalarNode) -> object:
        """Construct a YAML integer while preserving signed zero.

        ruamel converts the token itself, so the digit count is checked
        first: otherwise the interpreter's conversion limit surfaces as
        its own bare ``ValueError`` (issue #4558).
        """
        value: str = node.value
        if re.fullmatch(pattern=r"-0(?:_?0)*", string=value) is not None:
            return -0.0
        reject_excessive_decimal_token(token=value)
        return original(constructor_obj, node)

    constructor.add_constructor(
        tag=tag,
        constructor=_construct,
    )


class _YamlParserCache(threading.local):
    """One pair of mutable ruamel parsers per calling thread."""

    round_trip: _Yaml | None = None
    safe: _Yaml | None = None


_YAML_PARSERS = _YamlParserCache()


@beartype
def get_yaml() -> _Yaml:
    """Return this thread's cached round-trip ``YAML`` instance.

    The round-trip loader is used everywhere so a single parse covers
    both data extraction and comment metadata.  Constructing ``YAML()``
    globs the package directory for plug-ins on every call. A thread-local
    cache avoids that cost without sharing mutable parser state between
    concurrent calls.
    """
    cached = _YAML_PARSERS.round_trip
    if cached is None:
        cached = require_yaml(yaml=YAML())
        _configure_negative_zero_yaml_constructor(ruamel_yaml=cached)
        _YAML_PARSERS.round_trip = cached
    return cached


@beartype
def _get_safe_yaml() -> _Yaml:
    """Return this thread's safe (C-backed) ``YAML`` instance.

    Used for the comment-free fast path in :func:`_parse_yaml`: the
    round-trip loader is pure Python and ~8x slower than the safe
    loader backed by ``ruamel.yaml.clib``.  When the source contains
    none of the constructs that require round-trip fidelity (comments,
    explicit tags, merge keys), the data parsed by the safe loader is
    structurally identical to the demoted round-trip data.
    """
    cached = _YAML_PARSERS.safe
    if cached is None:
        cached = require_yaml(yaml=YAML(typ="safe", pure=False))
        _configure_negative_zero_yaml_constructor(ruamel_yaml=cached)
        _YAML_PARSERS.safe = cached
    return cached


@beartype
def _yaml_load_detail(*, exc: Exception) -> object:
    """Describe one ruamel failure for the public error message.

    ``ruamel`` reports a repeated key in an ``!!omap`` by asserting
    rather than by raising a parser error, and that assertion carries
    no message of its own (issue #3967).  An ``IndexError`` or
    ``AttributeError`` out of the scanner carries none either.
    """
    if isinstance(exc, AssertionError):
        return "duplicate key in an ordered mapping"
    if isinstance(exc, (IndexError, AttributeError)):
        return "malformed input"
    return exc


@beartype
def _yaml_needs_roundtrip(*, source: str) -> bool:
    """Return True when *source* needs the comment-preserving loader.

    The fast path is only safe when the source has none of the
    constructs that either carry metadata the safe loader drops
    (``#`` comments) or resolve differently between the two loaders
    (explicit ``!``/``!!`` tags such as ``!!omap``/``!!set``,
    anchors/aliases, merge keys, and ``=`` plain scalars that the safe
    loader resolves as a legacy value tag).  The checks are intentionally
    conservative text-presence checks — a ``#`` inside a quoted string
    still forces the slow path, which is correct but slightly
    pessimistic.
    """
    return (
        "#" in source
        or "!" in source
        or "&" in source
        or "*" in source
        or "<<" in source
        or "=" in source
    )


@beartype
def _record_anchor_binding(
    *,
    anchor: str,
    binding: int,
    latest_binding: dict[str, int],
) -> None:
    """Note that *anchor* now names the node numbered *binding*."""
    if anchor != "":
        latest_binding[anchor] = binding


@beartype
def _yaml_event_anchor(*, event: _AnchoredYamlEvent) -> str:
    """Return *event*'s anchor, or the empty string when absent."""
    if event.anchor is None:
        return ""
    return event.anchor


@beartype
def _self_referential_alias(*, source: str) -> str | None:
    """Return the anchor of an alias written inside the node it names.

    An anchor name can be bound again further in, and an alias takes the
    most recent binding, so each binding is numbered rather than tracked
    by name alone: ``[1, &x 2, *x]`` names the scalar and is not a cycle
    even while the sequence that first bound ``x`` is still open.
    """
    binding_count = 0
    latest_binding: dict[str, int] = {}
    open_bindings: set[int] = set()
    open_collections: list[int] = []
    try:
        for event in require_yaml(yaml=YAML()).parse(stream=source):
            match event:
                case CollectionStartEvent():
                    opened = _yaml_event_anchor(event=event)
                    binding_count += 1
                    _record_anchor_binding(
                        anchor=opened,
                        binding=binding_count,
                        latest_binding=latest_binding,
                    )
                    open_bindings.add(binding_count)
                    open_collections.append(binding_count)
                case CollectionEndEvent():
                    open_bindings.discard(open_collections.pop())
                case ScalarEvent():
                    named = _yaml_event_anchor(event=event)
                    binding_count += 1
                    _record_anchor_binding(
                        anchor=named,
                        binding=binding_count,
                        latest_binding=latest_binding,
                    )
                case AliasEvent():
                    alias = _yaml_event_anchor(event=event)
                    if latest_binding.get(alias) in open_bindings:
                        return alias
                case _:
                    pass
    except (YAMLError, ValueError, IndexError, AttributeError):
        # Malformed input: the load reports it with a position instead.
        return None
    return None


@beartype
def _reject_yaml_alias_cycle(*, source: str) -> None:
    """Reject a YAML alias written inside the node it names.

    ruamel cannot build a value for such an alias: it leaves ``None``
    where the alias was, so the document silently loses the reference,
    or descends without end and the failure is reported as excessive
    nesting.  The event stream still shows it, because the alias arrives
    while the collection carrying its anchor is open (issue #4562).
    """
    if "&" not in source or "*" not in source:
        return
    anchor = _self_referential_alias(source=source)
    if anchor is None:
        return
    raise _format_parse_error(
        input_format=InputFormat.YAML,
        detail=f"alias *{anchor} refers to the node that defines it",
    )


@beartype
def _parse_yaml(*, source: str) -> ParsedInput:
    """Parse a YAML string into a ``ParsedInput``.

    When the source contains no comments or other round-trip-only
    constructs, uses a C-backed safe loader and marks the result with
    ``yaml_needs_comment_resolve=False`` so the comment-resolution
    phase can be skipped.  Otherwise uses the comment-preserving
    (round-trip) loader so the same parse can later feed comment
    extraction without a second pass through the YAML source.
    """
    _reject_yaml_alias_cycle(source=source)
    try:
        _validate_yaml_float_tokens(source=source)
    except (
        YAMLError,
        ValueError,
        IndexError,
        AttributeError,
    ) as exc:
        # The scan is abandoned part way through whenever it raises, so
        # the thread's parser keeps whatever state it had reached.
        # Never hand that to the next public call (issue #3959).
        _YAML_PARSERS.round_trip = None
        message = f"Invalid YAML: {_yaml_load_detail(exc=exc)}"
        raise YAMLParseError(message) from exc
    if _yaml_needs_roundtrip(source=source):
        ruamel_yaml = get_yaml()
        try:
            # https://sourceforge.net/p/ruamel-yaml/tickets/564/
            raw_data = ruamel_yaml.load(stream=source)
        except (
            YAMLError,
            ValueError,
            IndexError,
            AttributeError,
            AssertionError,
        ) as exc:
            # A failed ruamel load leaves mutable scanner/parser state
            # behind. Never expose that partial state to the next public
            # call on this thread.
            _YAML_PARSERS.round_trip = None
            detail = _yaml_load_detail(exc=exc)
            message = f"Invalid YAML: {detail}"
            mark = _parser_mark(exc=exc)
            effective_line_4 = None
            effective_column_4 = None
            if mark is not None:
                effective_line_4 = mark.line + 1
                effective_column_4 = mark.column + 1
            raise YAMLParseError(
                message,
                line=effective_line_4,
                column=effective_column_4,
            ) from exc
        data = _unwrap_yaml_data(data=_require_yaml_data(data=raw_data))
        return ParsedYaml(
            data=data,
            raw_data=raw_data,
            needs_comment_resolve=True,
        )

    safe_yaml = _get_safe_yaml()
    try:
        plain_data = safe_yaml.load(stream=source)
    except (
        YAMLError,
        ValueError,
        IndexError,
        AttributeError,
        AssertionError,
    ) as exc:
        _YAML_PARSERS.safe = None
        detail = _yaml_load_detail(exc=exc)
        message = f"Invalid YAML: {detail}"
        mark = _parser_mark(exc=exc)
        effective_line_2 = None
        effective_column_2 = None
        if mark is not None:
            effective_line_2 = mark.line + 1
            effective_column_2 = mark.column + 1
        raise YAMLParseError(
            message,
            line=effective_line_2,
            column=effective_column_2,
        ) from exc
    data = _unwrap_yaml_data(data=_require_yaml_data(data=plain_data))
    return ParsedYaml(
        data=data,
        raw_data=plain_data,
        needs_comment_resolve=False,
    )


type _TomlData = dict[str, _TomlData] | list[_TomlData] | Scalar


@beartype
def _validate_toml_float_tokens(*, data: object) -> None:
    """Check TOML numeric tokens before unwrapping discards their
    spelling.
    """
    if isinstance(data, TomlFloat | TomlInteger):
        # tomlkit reads a decimal integer too wide for ``int`` as a
        # float, so checking the spelling first reports the real cause
        # rather than a binary64 range complaint (issue #4558).
        reject_excessive_decimal_token(token=data.as_string())
    if isinstance(data, TomlFloat):
        _ = _parse_finite_float(value=data.as_string())
    elif _is_object_dict(data):
        for value in data.values():
            _validate_toml_float_tokens(data=value)
    elif _is_object_list(data):
        for value in data:
            _validate_toml_float_tokens(data=value)


@beartype
def _preserve_toml_negative_zero(
    *, data: _TomlData, raw_data: object
) -> _TomlData:
    """Rebuild TOML data with signed integer zero represented as a
    float.
    """
    if isinstance(raw_data, TomlInteger) and raw_data.as_string() == "-0":
        return -0.0
    if isinstance(data, dict) and _is_object_dict(raw_data):
        return {
            key: _preserve_toml_negative_zero(
                data=value,
                raw_data=raw_data[key],
            )
            for key, value in data.items()
        }
    if isinstance(data, list) and _is_object_list(raw_data):
        return [
            _preserve_toml_negative_zero(
                data=value,
                raw_data=raw_data[index],
            )
            for index, value in enumerate(iterable=data)
        ]
    return data


@beartype
def _toml_data_to_value(*, data: _TomlData) -> Value:
    """Re-shape ``tomlkit`` output as a ``Value``.

    ``tomlkit.TOMLDocument.unwrap`` returns ``dict[str, Any]`` (modeled
    as ``_TomlData`` here); its dict and list arms have narrower static
    types than ``Value`` so dicts/lists are rebuilt to widen them.
    Scalar leaves -- including ``datetime.time`` now that it's part of
    ``Scalar`` -- are passed through unchanged.
    """
    match data:
        case dict():
            coerced: dict[Scalar, Value] = {
                k: _toml_data_to_value(data=v) for k, v in data.items()
            }
            return coerced
        case list():
            return [_toml_data_to_value(data=item) for item in data]
        case _:
            return data


@beartype
def _parse_toml(*, source: str) -> ParsedInput:
    """Parse a TOML string into a ``ParsedInput``."""
    try:
        toml_doc = tomlkit.parse(string=source)
    except TOMLKitError as exc:
        message = f"Invalid TOML: {exc}"
        effective_line_3 = None
        effective_column_3 = None
        if isinstance(exc, _PositionedTomlError):
            effective_line_3 = exc.line
            effective_column_3 = exc.col + 1
        raise TOMLParseError(
            message,
            line=effective_line_3,
            column=effective_column_3,
        ) from exc
    try:
        _validate_toml_float_tokens(data=toml_doc)
    except _FiniteFloatRangeError as exc:
        message = f"Invalid TOML: {exc}"
        raise TOMLParseError(message) from exc
    return ParsedToml(
        data=_toml_data_to_value(
            data=_preserve_toml_negative_zero(
                data=toml_doc.unwrap(),
                raw_data=toml_doc,
            ),
        ),
        toml_doc=toml_doc,
    )


@beartype
def _parse_by_format(
    *,
    source: str,
    input_format: InputFormat,
) -> ParsedInput:
    """Dispatch to the parser selected by *input_format*."""
    match input_format:
        case InputFormat.JSON:
            return _parse_json(source=source)
        case InputFormat.JSONC:
            return _parse_jsonc(source=source)
        case InputFormat.JSON5:
            return _parse_json5(source=source)
        case InputFormat.YAML:
            return _parse_yaml(source=source)
        case InputFormat.TOML:
            return _parse_toml(source=source)
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def parse_input(*, source: str, input_format: InputFormat) -> ParsedInput:
    """Parse and coerce an input string according to its format."""
    if (source_surrogate := _find_surrogate(data=source)) is not None:
        raise _surrogate_parse_error(
            input_format=input_format,
            surrogate=source_surrogate,
        )

    try:
        parsed = _parse_by_format(source=source, input_format=input_format)
        surrogate = _find_surrogate(data=parsed.data)
    except RecursionError as exc:
        raise recursion_parse_error(input_format=input_format) from exc
    if surrogate is not None:
        raise _surrogate_parse_error(
            input_format=input_format,
            surrogate=surrogate,
        )
    return parsed
