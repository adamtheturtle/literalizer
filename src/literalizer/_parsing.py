"""Parse JSON, JSON5, YAML, and TOML input into ``Value`` data."""

import dataclasses
import datetime
import enum
import functools
import json
from typing import assert_never, cast

import pyjson5
import tomlkit
from beartype import beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import (
    CommentedMap,
    CommentedOrderedMap,
    CommentedSeq,
    CommentedSet,
)
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError
from tomlkit.exceptions import TOMLKitError

from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    JSON5ParseError,
    JSONParseError,
    TOMLParseError,
    YAMLParseError,
)


class InputFormat(enum.Enum):
    """Supported input serialization formats."""

    JSON = enum.auto()
    JSON5 = enum.auto()
    YAML = enum.auto()
    TOML = enum.auto()


@dataclasses.dataclass(frozen=True)
class _ParsedInput:
    """Result of parsing an input string."""

    data: Value
    raw_data: object


@beartype
def _unwrap_yaml_scalar(*, value: object) -> object:
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
        case _:
            return value


@beartype
def _coerce_yaml_keys(*, data: object) -> Value:
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
    match data:
        case CommentedOrderedMap():
            omap_src = cast("dict[object, object]", data)
            omap = ordereddict(
                [
                    (f"{k}", _coerce_yaml_keys(data=v))
                    for k, v in omap_src.items()
                ]
            )
            return cast("Value", omap)
        case CommentedMap():
            return {
                f"{k}": _coerce_yaml_keys(data=v)
                for k, v in cast("dict[object, object]", data).items()
            }
        case CommentedSeq():
            return [
                _coerce_yaml_keys(data=item)
                for item in cast("list[object]", data)
            ]
        case CommentedSet():
            members = cast("set[object]", set(data))
            return {
                cast("Scalar", _unwrap_yaml_scalar(value=item))
                for item in members
            }
        case _:
            return cast("Value", _unwrap_yaml_scalar(value=data))


@beartype
def _parse_json(*, source: str) -> _ParsedInput:
    """Parse a JSON string into a ``_ParsedInput``."""
    try:
        data = json.loads(s=source)
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        )
        raise JSONParseError(message) from exc
    return _ParsedInput(data=data, raw_data=data)


@beartype
def _parse_json5(*, source: str) -> _ParsedInput:
    """Parse a JSON5 string into a ``_ParsedInput``."""
    try:
        data = pyjson5.decode(data=source)  # pylint: disable=no-member
    except pyjson5.Json5DecoderException as exc:  # pylint: disable=no-member
        message = f"Invalid JSON5: {exc}"
        raise JSON5ParseError(message) from exc
    return _ParsedInput(data=data, raw_data=data)


@functools.cache
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


@beartype
def _parse_yaml(*, source: str) -> _ParsedInput:
    """Parse a YAML string into a ``_ParsedInput``.

    Uses the comment-preserving (round-trip) loader so the same parse
    can later feed comment extraction without a second pass through
    the YAML source.
    """
    ruamel_yaml = get_yaml()
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        raw_data = ruamel_yaml.load(stream=source)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    data = _coerce_yaml_keys(data=raw_data)
    return _ParsedInput(data=data, raw_data=raw_data)


@beartype
def _parse_toml(*, source: str) -> _ParsedInput:
    """Parse a TOML string into a ``_ParsedInput``."""
    try:
        toml_doc = tomlkit.parse(string=source)
    except TOMLKitError as exc:
        message = f"Invalid TOML: {exc}"
        raise TOMLParseError(message) from exc
    toml_data = _coerce_toml_values(data=toml_doc.unwrap())
    return _ParsedInput(data=toml_data, raw_data=toml_doc)


@beartype
def parse_input(*, source: str, input_format: InputFormat) -> _ParsedInput:
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


@beartype
def _coerce_toml_values(*, data: object) -> Value:
    """Recursively convert TOML-specific types to ``Value`` types.

    ``tomlkit`` produces ``datetime.time`` values which are not
    representable in the ``Value`` type, so they are converted to
    their ISO-format string form.
    """
    match data:
        case dict():
            return {
                k: _coerce_toml_values(data=v)
                for k, v in cast("dict[str, object]", data).items()
            }
        case list():
            return [
                _coerce_toml_values(data=item)
                for item in cast("list[object]", data)
            ]
        case datetime.time():
            return data.isoformat()
        case _:
            return cast("Value", data)
