"""Compute preamble lines for the types present in literalized data."""

import dataclasses
import datetime
import math

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._checks import scalar_type_bucket
from literalizer._language import Language
from literalizer._types import Value


@beartype
def _collect_value_types(*, data: Value) -> frozenset[type]:
    """Return the set of Python types present in *data*."""
    match data:
        case ordereddict():
            child_types: frozenset[type] = frozenset()
            for v in data.values():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                child_types = child_types | _collect_value_types(data=v)  # pyright: ignore[reportUnknownArgumentType]
            return frozenset({ordereddict, str}) | child_types
        case dict():
            child_types = frozenset()
            for v in data.values():
                child_types = child_types | _collect_value_types(data=v)
            return frozenset({dict, str}) | child_types
        case set():
            scalar_types: frozenset[type] = frozenset(
                t
                for v in data
                if (t := _preamble_scalar_type(value=v)) is not None
            )
            return frozenset({set}) | scalar_types
        case list():
            child_types = frozenset()
            for v in data:
                child_types = child_types | _collect_value_types(data=v)
            return frozenset({list}) | child_types
        case _:
            result = _preamble_scalar_type(value=data)
            return frozenset({result}) if result is not None else frozenset()


@beartype
def _walk_empty_collections(*, val: Value, result: set[type]) -> None:
    """Walk *val* and add empty collection types to *result*."""
    match val:
        case ordereddict() | dict():
            if not val:
                result.add(dict)
            else:
                for v in val.values():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                    _walk_empty_collections(val=v, result=result)  # pyright: ignore[reportUnknownArgumentType]
        case set():
            if not val:
                result.add(set)
        case list():
            if not val:
                result.add(list)
            else:
                for v in val:
                    _walk_empty_collections(val=v, result=result)
        case _:
            pass


@beartype
def _collect_empty_collection_types(*, data: Value) -> frozenset[type]:
    """Return the set of collection types that have empty instances."""
    result: set[type] = set()
    _walk_empty_collections(val=data, result=result)
    return frozenset(result)


@beartype
def _preamble_scalar_type(*, value: Value) -> type | None:
    """Return the preamble-relevant type for a scalar.

    Like :func:`scalar_type_bucket` but distinguishes
    ``datetime.datetime`` from ``datetime.date`` (they need different
    preamble lines).
    """
    match value:
        case datetime.datetime():
            return datetime.datetime
        case datetime.date():
            return datetime.date
        case _:
            return scalar_type_bucket(value=value)


@beartype
def _collection_preamble(
    *,
    types: frozenset[type],
    language: Language,
) -> tuple[str, ...]:
    """Return collection-config preamble lines for present types."""
    lines: list[str] = []
    if dict in types:
        lines.extend(language.dict_format_config.preamble_lines)
    if set in types:
        lines.extend(language.set_format_config.preamble_lines)
    if list in types:
        lines.extend(language.sequence_format_config.preamble_lines)
    if ordereddict in types:
        lines.extend(language.ordered_map_format_config.preamble_lines)
    return tuple(lines)


@beartype
def _deduplicate(*, lines: tuple[str, ...]) -> tuple[str, ...]:
    """Remove duplicates from *lines* preserving insertion order."""
    seen: set[str] = set()
    result: list[str] = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return tuple(result)


@beartype
def _has_special_float(*, data: Value) -> bool:
    """Return ``True`` if *data* contains any special float value
    (inf, -inf, or nan).
    """
    match data:
        case float():
            return math.isinf(data) or math.isnan(data)
        case dict():
            return any(_has_special_float(data=v) for v in data.values())
        case list() | set():
            return any(_has_special_float(data=v) for v in data)
        case _:
            return False


@dataclasses.dataclass(frozen=True)
class _PreambleResult:
    """Header and body preamble lines."""

    header: tuple[str, ...]
    body: tuple[str, ...]
    types_present: frozenset[type]


@beartype
def compute_preamble(
    *,
    data: Value,
    language: Language,
    has_variable_declaration: bool,
) -> _PreambleResult:
    """Compute preamble lines from the data types present and the
    language configuration.
    """
    types = _collect_value_types(data=data)

    scalar = tuple(
        line
        for scalar_type, preamble in language.scalar_preamble.items()
        if scalar_type in types
        for line in preamble
    )
    special_float = (
        language.special_float_preamble
        if float in types and _has_special_float(data=data)
        else ()
    )
    collection = _collection_preamble(types=types, language=language)
    empty_collection_types: frozenset[type] = (
        _collect_empty_collection_types(data=data)
        if has_variable_declaration and types & {dict, list, set, ordereddict}
        else frozenset()
    )
    type_hint = (
        language.type_hint_collection_preamble_lines(empty_collection_types)
        if empty_collection_types
        else ()
    )
    body = language.compute_body_preamble(types, data)
    return _PreambleResult(
        header=_deduplicate(
            lines=scalar + special_float + collection + type_hint,
        )
        + tuple(language.static_body_preamble),
        body=body,
        types_present=types,
    )
