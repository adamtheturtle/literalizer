"""Parse JSON, JSON5, YAML, and TOML input into ``Value`` data."""

import dataclasses
import datetime
import enum
import functools
import json
from typing import assert_never

import pyjson5
import tomlkit
from beartype import beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import (
    CommentedOrderedMap,
    CommentedSet,
)
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError
from tomlkit.exceptions import TOMLKitError
from tomlkit.toml_document import TOMLDocument

from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    JSON5ParseError,
    JSONParseError,
    TOMLParseError,
    YAMLParseError,
)

type YamlCoercible = (
    Scalar
    | list[YamlCoercible]
    | dict[object, YamlCoercible]
    | CommentedOrderedMap
    | CommentedSet
)


class InputFormat(enum.Enum):
    """Supported input serialization formats."""

    JSON = enum.auto()
    JSON5 = enum.auto()
    YAML = enum.auto()
    TOML = enum.auto()


@dataclasses.dataclass(frozen=True)
class ParsedPlain:
    """Result of parsing a comment-free input (JSON or JSON5)."""

    data: Value


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


@dataclasses.dataclass(frozen=True)
class ParsedToml:
    """Result of parsing a TOML input string."""

    data: Value
    toml_doc: TOMLDocument


ParsedInput = ParsedPlain | ParsedYaml | ParsedToml


@beartype
def _unwrap_yaml_scalar(*, value: Scalar) -> Scalar:  # noqa: PLR0911
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
    match value:
        case bool():
            return bool(value)
        case int():
            return int(value)
        case float():
            return float(value)
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
        case datetime.date():
            return value
        case bytes():
            return value
        case None:
            return value
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _coerce_yaml_keys(*, data: YamlCoercible) -> Value:
    """Recursively convert non-string dict keys to their string form.

    YAML allows non-string mapping keys (e.g. integers); ``Value``
    requires ``dict[str, Value]``, so we normalise before passing
    loaded YAML data to :func:`_literalize`.

    The round-trip loader returns ``CommentedOrderedMap`` for YAML
    ``!!omap`` nodes; those are demoted to plain ``ordereddict`` so
    ordered-map detection in :func:`_literalize` still works.  Other
    mappings come through as ``CommentedMap`` and are demoted to plain
    ``dict``.  :class:`CommentedSet` does not subclass :class:`set`, so
    it is converted as well.  Scalar leaves are unwrapped to plain
    Python types so type-based dispatch sees ``int`` rather than
    ``ScalarInt`` and friends.
    """
    # ``CommentedMap`` and ``CommentedSeq`` are subclasses of ``dict``
    # and ``list`` respectively, so their cases collapse into the plain
    # ``dict()`` / ``list()`` arms below.  ``CommentedOrderedMap`` must
    # stay on its own arm because it is *also* a ``dict`` subclass but
    # represents ``!!omap`` and must be demoted to ``ordereddict``.
    match data:
        case CommentedOrderedMap():
            omap_src: dict[object, YamlCoercible] = dict(data)
            return ordereddict(
                [
                    (f"{k}", _coerce_yaml_keys(data=v))
                    for k, v in omap_src.items()
                ]
            )
        case dict():
            return {f"{k}": _coerce_yaml_keys(data=v) for k, v in data.items()}
        case list():
            return [_coerce_yaml_keys(data=item) for item in data]
        case CommentedSet():
            members: set[Scalar] = set(data)
            return {_unwrap_yaml_scalar(value=item) for item in members}
        case (
            bool()
            | int()
            | float()
            | str()
            | datetime.datetime()
            | datetime.date()
            | bytes()
            | None
        ):
            return _unwrap_yaml_scalar(value=data)
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _parse_json(*, source: str) -> ParsedInput:
    """Parse a JSON string into a ``ParsedInput``."""
    try:
        data = json.loads(s=source)
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        )
        raise JSONParseError(message) from exc
    return ParsedPlain(data=data)


@beartype
def _parse_json5(*, source: str) -> ParsedInput:
    """Parse a JSON5 string into a ``ParsedInput``."""
    try:
        data = pyjson5.decode(data=source)  # pylint: disable=no-member
    except pyjson5.Json5DecoderException as exc:  # pylint: disable=no-member
        message = f"Invalid JSON5: {exc}"
        raise JSON5ParseError(message) from exc
    return ParsedPlain(data=data)


@functools.cache
@beartype
def get_yaml() -> YAML:
    """Return the cached round-trip ``YAML`` instance.

    The round-trip loader is used everywhere so a single parse covers
    both data extraction and comment metadata.  Constructing ``YAML()``
    globs the package directory for plug-ins on every call; caching
    avoids that cost on every parse.  ``ruamel`` parsers are not safe
    for concurrent use within a single instance, so ``literalize`` is
    not safe to call from multiple threads.
    """
    return YAML()


@functools.cache
@beartype
def _get_safe_yaml() -> YAML:
    """Return the cached safe (C-backed when available) ``YAML`` instance.

    Used for the comment-free fast path in :func:`_parse_yaml`: the
    round-trip loader is pure Python and ~8x slower than the safe
    loader backed by ``ruamel.yaml.clib``.  When the source contains
    none of the constructs that require round-trip fidelity (comments,
    explicit tags, merge keys), the data parsed by the safe loader is
    structurally identical to the demoted round-trip data.
    """
    return YAML(typ="safe", pure=False)


@beartype
def _yaml_needs_roundtrip(*, source: str) -> bool:
    """Return True when *source* needs the comment-preserving loader.

    The fast path is only safe when the source has none of the
    constructs that either carry metadata the safe loader drops
    (``#`` comments) or resolve differently between the two loaders
    (explicit ``!``/``!!`` tags such as ``!!omap``/``!!set``,
    anchors/aliases, and merge keys).  The checks are intentionally
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
    if _yaml_needs_roundtrip(source=source):
        ruamel_yaml = get_yaml()
        try:
            # https://sourceforge.net/p/ruamel-yaml/tickets/564/
            raw_data = ruamel_yaml.load(stream=source)  # pyright: ignore[reportUnknownMemberType]
        except YAMLError as exc:
            message = f"Invalid YAML: {exc}"
            raise YAMLParseError(message) from exc
        data = _coerce_yaml_keys(data=raw_data)
        return ParsedYaml(
            data=data,
            raw_data=raw_data,
            needs_comment_resolve=True,
        )

    safe_yaml = _get_safe_yaml()
    try:
        plain_data = safe_yaml.load(stream=source)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    data = _coerce_yaml_keys(data=plain_data)
    return ParsedYaml(
        data=data,
        raw_data=plain_data,
        needs_comment_resolve=False,
    )


@beartype
def _parse_toml(*, source: str) -> ParsedInput:
    """Parse a TOML string into a ``ParsedInput``."""
    try:
        toml_doc = tomlkit.parse(string=source)
    except TOMLKitError as exc:
        message = f"Invalid TOML: {exc}"
        raise TOMLParseError(message) from exc
    unwrapped: _TomlData = toml_doc.unwrap()
    toml_data = _coerce_toml_values(data=unwrapped)
    return ParsedToml(data=toml_data, toml_doc=toml_doc)


@beartype
def parse_input(*, source: str, input_format: InputFormat) -> ParsedInput:
    """Parse and coerce an input string according to its format."""
    match input_format:
        case InputFormat.JSON:
            return _parse_json(source=source)
        case InputFormat.JSON5:
            return _parse_json5(source=source)
        case InputFormat.YAML:
            return _parse_yaml(source=source)
        case InputFormat.TOML:
            return _parse_toml(source=source)
        case _ as unreachable:
            assert_never(unreachable)


type _TomlData = (
    dict[str, _TomlData] | list[_TomlData] | datetime.time | Scalar
)


@beartype
def _coerce_toml_values(*, data: _TomlData) -> Value:
    """Recursively convert TOML-specific types to ``Value`` types.

    ``tomlkit`` produces ``datetime.time`` values which cannot be
    expressed in the ``Value`` type, so they are converted to
    their ISO-format string form.
    """
    match data:
        case dict():
            return {k: _coerce_toml_values(data=v) for k, v in data.items()}
        case list():
            return [_coerce_toml_values(data=item) for item in data]
        case datetime.time():
            return data.isoformat()
        case _:
            return data
