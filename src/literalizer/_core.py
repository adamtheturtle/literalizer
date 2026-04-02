"""Core conversion logic: formatting values and parsing JSON/YAML."""

import dataclasses
import datetime
import json
from collections.abc import Sequence
from io import StringIO
from typing import Any, assert_never, cast

from beartype import BeartypeConf, beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError

from literalizer._comments import (
    CollectionComments,
    ElementComments,
    apply_collection_comments,
    extract_yaml_comments,
    literalize_yaml_scalar,
    prepend_collection_comments,
)
from literalizer._formatters.type_inference import (
    DictType,
    infer_element_type,
)
from literalizer._language import Language
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    JSONParseError,
    YAMLParseError,
)


@dataclasses.dataclass(frozen=True)
class LiteralizeResult:
    """Result of converting data to a native language literal."""

    code: str
    """The formatted literal text.

    When a language defines ``scalar_body_preamble`` entries (e.g.
    Haskell typeclass instances), those lines are prepended to the code
    so they appear in the correct structural position.
    """

    preamble: tuple[str, ...]
    """Lines (imports, package declarations, etc.) that must precede
    the generated code.  Empty when none are needed.
    """


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
            if len(val) == 0:
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

    Like :func:`_scalar_type_bucket` but distinguishes
    ``datetime.datetime`` from ``datetime.date`` (they need different
    preamble lines).
    """
    if isinstance(value, datetime.datetime):
        return datetime.datetime
    if isinstance(value, datetime.date):
        return datetime.date
    return _scalar_type_bucket(value=value)


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


@dataclasses.dataclass(frozen=True)
class _PreambleResult:
    """Header and body preamble lines."""

    header: tuple[str, ...]
    body: tuple[str, ...]


@beartype
def _compute_preamble(
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
            lines=scalar + collection + type_hint,
        )
        + tuple(language.static_body_preamble),
        body=body,
    )


@beartype
def _scalar_type_bucket(*, value: Value) -> type | None:
    """Return the type bucket for a scalar, or ``None`` for
    collections.
    """
    if value is None:
        return type(None)
    # Check bool before int (bool is a subclass of int), and
    # datetime before date (datetime is a subclass of date).
    _buckets = (
        bool,
        int,
        float,
        str,
        bytes,
        datetime.date,
    )
    for bucket in _buckets:
        if isinstance(value, bucket):
            return bucket
    return None


@beartype
def _coerce_scalar_to_str(
    *,
    value: Value,
) -> str:
    """Convert a scalar to its string representation."""
    match value:
        case bool():
            return "True" if value else "False"
        case None:
            return "None"
        # datetime.datetime is a subclass of datetime.date, so this
        # single check covers both types.
        case datetime.date():
            return value.isoformat()
        case bytes():
            return value.hex()
        case str():
            return value
        case _:
            return repr(value)


@beartype
def _scalar_type_buckets(
    *,
    values: Sequence[Value],
) -> set[type] | None:
    """Return the set of scalar type buckets for *values*.

    Returns ``None`` if any value is not a scalar.
    """
    buckets: set[type] = set()
    for v in values:
        bucket = _scalar_type_bucket(value=v)
        if bucket is None:
            return None
        buckets.add(bucket)
    return buckets


@beartype
def _all_scalars_heterogeneous(
    *,
    values: Sequence[Value],
) -> bool:
    """Check whether values are all scalars with more than one type."""
    buckets = _scalar_type_buckets(values=values)
    return buckets is not None and len(buckets) > 1


@beartype
def _coerce_heterogeneous_sibling_lists(*, data: Value) -> Value:
    """Recursively coerce sibling lists with heterogeneous scalar
    element types so that every inner element becomes a string.

    For example, ``[[1, 2], ["a", "b"]]`` becomes
    ``[["1", "2"], ["a", "b"]]``.
    """
    match data:
        case dict() | ordereddict():
            return type(data)(
                {
                    k: _coerce_heterogeneous_sibling_lists(data=v)  # pyright: ignore[reportUnknownArgumentType]
                    for k, v in data.items()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
                }
            )
        case list():
            new_list = [
                _coerce_heterogeneous_sibling_lists(data=v) for v in data
            ]
            sublists: list[list[Value]] = [
                v for v in new_list if isinstance(v, list)
            ]
            if (
                len(sublists) == len(new_list)
                and len(sublists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in sublists for e in sub],
                )
            ):
                return [
                    [_coerce_scalar_to_str(value=e) for e in sub]
                    for sub in sublists
                ]
            return new_list
        case _:
            return data


@beartype
def _has_heterogeneous(*, data: Value) -> bool:
    """Recursively check whether data contains any heterogeneous
    all-scalar collections.
    """
    match data:
        case ordereddict() | dict():
            children: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        case list():
            children = data
        case set():
            return _all_scalars_heterogeneous(values=list(data))
        case _:
            return False

    return any(
        _has_heterogeneous(data=v) for v in children
    ) or _all_scalars_heterogeneous(values=children)


@beartype
def _has_heterogeneous_sibling_lists(*, data: Value) -> bool:
    """Recursively check whether data contains sibling lists whose
    combined scalar elements are heterogeneous.

    For example, ``[[1, 2], ["a", "b"]]`` returns ``True`` because the
    sibling sub-lists have differing element types when combined.
    """
    match data:
        case dict() | ordereddict():
            return any(
                _has_heterogeneous_sibling_lists(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            )
        case list():
            if any(_has_heterogeneous_sibling_lists(data=v) for v in data):
                return True
            sublists: list[list[Value]] = [
                v for v in data if isinstance(v, list)
            ]
            return (
                len(sublists) == len(data)
                and len(sublists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in sublists for e in sub],
                )
            )
        case _:
            return False


@beartype
def _check_heterogeneous(*, data: Value) -> None:
    """Recursively check for heterogeneous all-scalar collections and
    raise if found.
    """
    if _has_heterogeneous(data=data):
        msg = (
            "Collection contains heterogeneous scalar types "
            "that would be coerced to strings"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _coerce_heterogeneous_ordereddict(
    *,
    data: ordereddict,
) -> ordereddict:
    """Coerce an ordered dict with heterogeneous scalar values."""
    new_ordered_map: ordereddict = ordereddict()
    for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        new_ordered_map[k] = _coerce_heterogeneous_scalars(data=v)  # pyright: ignore[reportUnknownArgumentType]
    ordered_map_vals: list[Value] = list(new_ordered_map.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if _all_scalars_heterogeneous(values=ordered_map_vals):
        for k in new_ordered_map:  # pyright: ignore[reportUnknownVariableType]
            new_ordered_map[k] = _coerce_scalar_to_str(
                value=new_ordered_map[k],  # pyright: ignore[reportUnknownArgumentType]
            )
    return new_ordered_map


@beartype
def _coerce_heterogeneous_dict(
    *,
    data: dict[str, Value],
) -> dict[str, Value]:
    """Coerce a dict with heterogeneous scalar values."""
    new_dict: dict[str, Value] = {
        k: _coerce_heterogeneous_scalars(data=v) for k, v in data.items()
    }
    if _all_scalars_heterogeneous(
        values=list(new_dict.values()),
    ):
        new_dict = {
            k: _coerce_scalar_to_str(value=v) for k, v in new_dict.items()
        }
    return new_dict


@beartype
def _coerce_heterogeneous_set(
    *,
    data: set[Scalar],
) -> set[Scalar]:
    """Coerce a set with heterogeneous scalar values."""
    items: list[Value] = list(data)
    if _all_scalars_heterogeneous(values=items):
        return {_coerce_scalar_to_str(value=v) for v in items}
    return data


@beartype
def _coerce_heterogeneous_list(
    *,
    data: list[Value],
) -> list[Value]:
    """Coerce a list with heterogeneous scalar values."""
    new_list = [_coerce_heterogeneous_scalars(data=v) for v in data]
    if _all_scalars_heterogeneous(values=new_list):
        return [_coerce_scalar_to_str(value=v) for v in new_list]
    return new_list


@beartype
def _coerce_heterogeneous_scalars(
    *,
    data: Value,
) -> Value:
    """Recursively coerce heterogeneous all-scalar collections to
    strings.
    """
    match data:
        case ordereddict():
            return _coerce_heterogeneous_ordereddict(data=data)
        case dict():
            return _coerce_heterogeneous_dict(data=data)
        case set():
            return _coerce_heterogeneous_set(data=data)
        case list():
            return _coerce_heterogeneous_list(data=data)
        case _:
            return data


@beartype
def _value_type_family(*, value: Value) -> str:
    """Return a broad type family label for a value.

    Used to decide whether values in a dict are homogeneous enough for
    languages that require a single value type (e.g. Mojo).
    """
    if value is None:
        return "none"
    # Check bool before int (bool is a subclass of int), and
    # datetime before date (datetime is a subclass of date).
    for check_type, family in (
        (bool, "bool"),
        (int, "int"),
        (float, "float"),
        (str, "str"),
        (bytes, "bytes"),
        (datetime.datetime, "datetime"),
        (datetime.date, "date"),
        (list, "list"),
        (ordereddict, "dict"),
        (dict, "dict"),
    ):
        if isinstance(value, check_type):
            return family
    return "set"


@beartype
def _dict_values_mixed_types(*, values: Sequence[Value]) -> bool:
    """Check whether dict values span more than one type family."""
    if len(values) <= 1:
        return False
    families: set[str] = set()
    for v in values:
        families.add(_value_type_family(value=v))
    return len(families) > 1


@beartype
def _coerce_value_to_str(*, value: Value) -> str:
    """Convert any value (scalar or collection) to a string."""
    if isinstance(value, str):
        return value
    bucket = _scalar_type_bucket(value=value)
    if bucket is not None or value is None:
        return _coerce_scalar_to_str(value=value)
    if isinstance(value, set):
        sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
        return json.dumps(obj=sorted_items, default=str)
    return json.dumps(obj=value, default=str, sort_keys=False)


@beartype
def _coerce_mixed_dict_values(*, data: Value) -> Value:
    """Recursively coerce dicts whose values span multiple type families.

    When a dict has values of mixed types (e.g. strings and lists),
    all values are converted to strings so the dict becomes homogeneous.
    """
    match data:
        case ordereddict():
            new_ordered_map: ordereddict = ordereddict()
            for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                new_ordered_map[k] = _coerce_mixed_dict_values(data=v)  # pyright: ignore[reportUnknownArgumentType]
            ordered_map_vals: list[Value] = list(new_ordered_map.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            if _dict_values_mixed_types(values=ordered_map_vals):
                for k in new_ordered_map:  # pyright: ignore[reportUnknownVariableType]
                    new_ordered_map[k] = _coerce_value_to_str(
                        value=new_ordered_map[k],  # pyright: ignore[reportUnknownArgumentType]
                    )
            return new_ordered_map
        case dict():
            new_dict: dict[str, Value] = {
                k: _coerce_mixed_dict_values(data=v) for k, v in data.items()
            }
            if _dict_values_mixed_types(values=list(new_dict.values())):
                new_dict = {
                    k: _coerce_value_to_str(value=v)
                    for k, v in new_dict.items()
                }
            return new_dict
        case list():
            return [_coerce_mixed_dict_values(data=v) for v in data]
        case _:
            return data


@beartype
def _coerce_mixed_list_values(*, data: Value) -> Value:
    """Recursively coerce lists whose elements span multiple type families.

    When a list has elements of mixed types (e.g. scalars and nested
    collections), all elements are converted to strings so the list
    becomes homogeneous.
    """
    match data:
        case ordereddict():
            new_ordered_map: ordereddict = ordereddict()
            for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                new_ordered_map[k] = _coerce_mixed_list_values(data=v)  # pyright: ignore[reportUnknownArgumentType]
            return new_ordered_map
        case dict():
            return {
                k: _coerce_mixed_list_values(data=v) for k, v in data.items()
            }
        case list():
            new_list = [_coerce_mixed_list_values(data=v) for v in data]
            if _dict_values_mixed_types(values=new_list):
                return [_coerce_value_to_str(value=v) for v in new_list]
            return new_list
        case _:
            return data


@beartype
def _has_mixed_dict_values(*, data: Value) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families.
    """
    match data:
        case ordereddict() | dict():
            values: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            if _dict_values_mixed_types(values=values):
                return True
            return any(_has_mixed_dict_values(data=v) for v in values)
        case list():
            return any(_has_mixed_dict_values(data=v) for v in data)
        case _:
            return False


@beartype
def _has_mixed_list_values(*, data: Value) -> bool:
    """Recursively check whether data contains any list whose elements span
    multiple type families.
    """
    match data:
        case ordereddict() | dict():
            return any(
                _has_mixed_list_values(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            )
        case list():
            if _dict_values_mixed_types(values=data):
                return True
            return any(_has_mixed_list_values(data=v) for v in data)
        case _:
            return False


@beartype
def _format_scalar(*, value: Scalar, spec: Language) -> str:
    """Format a scalar JSON value as a native language literal."""
    match value:
        case None:
            result = spec.null_literal
        case bool():
            result = spec.true_literal if value else spec.false_literal
        case int():
            result = spec.format_integer(value)
        case float():
            result = spec.format_float(value)
        case str():
            result = spec.format_string(value)
        case bytes():
            result = spec.format_bytes(value)
        case datetime.datetime():
            result = spec.format_datetime(value)
        case _:
            result = spec.format_date(value)
    return result


@beartype
def _build_dict_entry(
    *, key_str: str, val: Value, val_str: str, spec: Language
) -> str:
    """Format a single dict key-value entry using the language spec."""
    return spec.dict_format_config.format_entry(key_str, val, val_str)


@beartype
def _format_set_value(*, value: set[Scalar], spec: Language) -> str:
    """Format a set value as a native language literal."""
    set_cfg = spec.set_format_config

    if not value and set_cfg.empty_set is not None:
        return set_cfg.empty_set
    sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
    items_as_values: list[Value] = list(sorted_items)
    formatted = [_format_scalar(value=v, spec=spec) for v in sorted_items]
    entries = [
        spec.format_set_entry(v, item)
        for v, item in zip(sorted_items, formatted, strict=True)
    ]
    joined = spec.element_separator.join(entries)
    return set_cfg.set_open(items_as_values) + joined + set_cfg.close


@beartype
def _format_ordered_map_value(
    *,
    value: ordereddict,
    spec: Language,
) -> str:
    """Format an ordered map as a native language literal."""
    ordered_map_cfg = spec.ordered_map_format_config

    ordered_map_items: list[tuple[str, Value]] = [
        (k, v)
        for k, v in value.items()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        if not (spec.skip_null_dict_values and v is None)
    ]
    pairs = [
        spec.format_ordered_map_entry(
            _format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
            ),
            v,
            _format_value(
                value=v,
                spec=spec,
                dict_open_override=None,
            ),
        )
        for k, v in ordered_map_items
    ]
    joined = spec.element_separator.join(pairs)
    return ordered_map_cfg.open_str + joined + ordered_map_cfg.close


@beartype
def _format_dict_value(
    *,
    value: dict[str, Value],
    spec: Language,
    open_override: str | None,
) -> str:
    """Format a dict as a native language literal."""
    dict_cfg = spec.dict_format_config

    dict_items: dict[str, Value] = {
        k: v
        for k, v in value.items()
        if not (spec.skip_null_dict_values and v is None)
    }
    if not dict_items and dict_cfg.empty_dict is not None:
        return dict_cfg.empty_dict
    pairs = [
        _build_dict_entry(
            key_str=_format_value(
                value=k,
                spec=spec,
                dict_open_override=None,
            ),
            val=v,
            val_str=_format_value(
                value=v,
                spec=spec,
                dict_open_override=None,
            ),
            spec=spec,
        )
        for k, v in dict_items.items()
    ]
    joined = spec.element_separator.join(pairs)
    opener = (
        open_override
        if open_override is not None
        else dict_cfg.open_fn(dict_items)
    )
    return opener + joined + dict_cfg.close


@beartype
def _compute_dict_open_override(
    *,
    items: list[Value],
    spec: Language,
) -> str | None:
    """Return a widened dict opener when dicts in a list infer
    different value types, or ``None`` when no widening is needed.
    """
    open_fn = spec.dict_format_config.open_fn
    dicts: list[dict[str, Value]] = [
        item
        for item in items
        if isinstance(item, dict) and not isinstance(item, ordereddict)
    ]
    min_dicts_for_widening = 2
    if len(dicts) < min_dicts_for_widening:
        return None

    filtered_dicts = [
        {
            k: v
            for k, v in d.items()
            if not (spec.skip_null_dict_values and v is None)
        }
        for d in dicts
    ]

    openers = {open_fn(d) for d in filtered_dicts}
    if len(openers) <= 1:
        return None

    # Types differ: combine all values to infer the widened type.
    combined: dict[str, Value] = {}
    idx = 0
    for d in filtered_dicts:
        for v in d.values():
            combined[f"_k{idx}"] = v
            idx += 1
    return open_fn(combined)


@beartype
def _compute_sequence_dict_override(
    *,
    items: list[Value],
    spec: Language,
) -> str | None:
    """Determine the dict opener override for dicts in a sequence.

    When all items are uniform dicts and the language defines a
    ``narrowed_open``, returns that anonymous opener so the
    sequence type carries the map type instead of each dict.
    Otherwise falls back to the widening logic of
    :func:`_compute_dict_open_override`.
    """
    narrowed_open = spec.dict_format_config.narrowed_open
    if narrowed_open is not None:
        element_type = infer_element_type(items=items)
        if isinstance(element_type, DictType):
            return narrowed_open
    return _compute_dict_open_override(items=items, spec=spec)


@beartype
def _format_list_value(
    *,
    value: list[Value],
    spec: Language,
) -> str:
    """Format a list as a native language literal."""
    sequence_cfg = spec.sequence_format_config

    if not value and sequence_cfg.empty_sequence is not None:
        return sequence_cfg.empty_sequence
    dict_open_override = _compute_sequence_dict_override(
        items=value,
        spec=spec,
    )
    items = [
        spec.format_sequence_entry(
            v,
            _format_value(
                value=v,
                spec=spec,
                dict_open_override=dict_open_override,
            ),
        )
        for v in value
    ]
    joined = spec.element_separator.join(items)
    # Some languages (e.g. Python) require a trailing comma on
    # single-element sequences to avoid syntactic ambiguity.
    if len(items) == 1 and sequence_cfg.single_element_trailing_comma:
        joined += spec.element_separator.strip()
    return f"{spec.sequence_open(value)}{joined}{sequence_cfg.close}"


@beartype
def _format_value(
    *,
    value: Value,
    spec: Language,
    dict_open_override: str | None,
) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), dicts, and sets.

    When *dict_open_override* is set, dict values use it as the opening
    delimiter instead of inferring the type from their own values.
    This is used to widen map value types when dicts with differing
    inferred types appear in the same sequence.
    """
    match value:
        case ordereddict():
            return _format_ordered_map_value(value=value, spec=spec)
        case dict():
            return _format_dict_value(
                value=value,
                spec=spec,
                open_override=dict_open_override,
            )
        case set():
            return _format_set_value(value=value, spec=spec)
        case list():
            return _format_list_value(value=value, spec=spec)
        case _:
            return _format_scalar(value=value, spec=spec)


@beartype
def _wrap_body(
    *,
    body: str,
    is_ordered_map: bool,
    data: list[Value] | dict[str, Value] | set[Scalar],
    spec: Language,
    line_prefix: str,
) -> str:
    """Wrap ``body`` in the language's open/close delimiters."""
    ci = spec.indent if spec.indent_closing_delimiter else ""
    close_prefix = f"{line_prefix}{ci}"
    if is_ordered_map:
        ordered_map_cfg = spec.ordered_map_format_config

        opening = f"{line_prefix}{ordered_map_cfg.open_str}"
        closing = f"{close_prefix}{ordered_map_cfg.close}"
    elif isinstance(data, dict):
        dict_cfg = spec.dict_format_config

        opening = f"{line_prefix}{dict_cfg.open_fn(data)}"
        closing = f"{close_prefix}{dict_cfg.close}"
    elif isinstance(data, set):
        sorted_set: list[Value] = sorted(
            data,
            key=lambda v: (type(v).__name__, repr(v)),
        )
        opening = f"{line_prefix}{spec.set_format_config.set_open(sorted_set)}"
        closing = f"{close_prefix}{spec.set_format_config.close}"
    else:
        opening = f"{line_prefix}{spec.sequence_open(data)}"
        closing = f"{close_prefix}{spec.sequence_format_config.close}"
    return f"{opening.rstrip()}\n{body}\n{closing}"


@beartype
def _coerce_yaml_keys(*, data: object) -> Value:
    """Recursively convert non-string dict keys to their string form.

    YAML allows non-string mapping keys (e.g. integers); ``Value``
    requires ``dict[str, Value]``, so we normalise before passing
    loaded YAML data to :func:`_literalize`.

    ``ordereddict`` (used for YAML ``!!omap`` nodes) preserves its keys
    (so ordered-map detection in :func:`_literalize` still works) but
    still walks into its values.
    """
    match data:
        case ordereddict():
            omap = cast("dict[object, object]", data)
            coerced = ordereddict(
                [(f"{k}", _coerce_yaml_keys(data=v)) for k, v in omap.items()]
            )
            return cast("Value", coerced)
        case dict():
            return {
                f"{k}": _coerce_yaml_keys(data=v)
                for k, v in cast("dict[object, object]", data).items()
            }
        case list():
            return [
                _coerce_yaml_keys(data=item)
                for item in cast("list[object]", data)
            ]
        case _:
            return cast("Value", data)


@beartype
def _apply_coercions(
    *,
    data: Value,
    spec: Language,
    error_on_coercion: bool,
) -> Value:
    """Apply heterogeneous-type coercions controlled by the sequence
    format.
    """
    if not spec.sequence_format.supports_heterogeneity:
        if error_on_coercion:
            _check_heterogeneous(data=data)
            if _has_heterogeneous_sibling_lists(data=data):
                msg = (
                    "Collection contains heterogeneous scalar types "
                    "that would be coerced to strings"
                )
                raise HeterogeneousCoercionError(msg)
            if _has_mixed_dict_values(data=data):
                msg = (
                    "Dict contains values of mixed types "
                    "that would be coerced to strings"
                )
                raise HeterogeneousCoercionError(msg)
            if _has_mixed_list_values(data=data):
                msg = (
                    "List contains elements of mixed types "
                    "that would be coerced to strings"
                )
                raise HeterogeneousCoercionError(msg)
        else:
            data = _coerce_heterogeneous_scalars(data=data)
            data = _coerce_heterogeneous_sibling_lists(data=data)
            data = _coerce_mixed_dict_values(data=data)
            data = _coerce_mixed_list_values(data=data)
    return data


def _format_collection_lines(
    *,
    data: dict[str, Value] | set[Scalar] | list[Value],
    spec: Language,
    body_prefix: str,
    trailing_comma: bool,
    is_ordered_map: bool,
    include_delimiters: bool,
) -> list[str] | str:
    """Format collection elements as indented lines.

    Returns a list of formatted lines, or a ``str`` when the caller
    should return that string immediately (e.g. an all-null dict that
    collapses to the empty-collection literal).
    """
    lines: list[str] = []
    match data:
        case dict() as dict_data:
            entries = [
                (k, v)
                for k, v in dict_data.items()
                if not (spec.skip_null_dict_values and v is None)
            ]
            if not entries and include_delimiters and dict_data:
                empty_value: ordereddict | dict[str, Value] = (
                    ordereddict() if is_ordered_map else {}
                )
                return _format_value(
                    value=empty_value,
                    spec=spec,
                    dict_open_override=None,
                )
            last_idx = len(entries) - 1
            for i, (k, v) in enumerate(iterable=entries):
                formatted_key = _format_value(
                    value=k,
                    spec=spec,
                    dict_open_override=None,
                )
                formatted_val = _format_value(
                    value=v,
                    spec=spec,
                    dict_open_override=None,
                )
                entry = (
                    spec.format_ordered_map_entry(
                        formatted_key, v, formatted_val
                    )
                    if is_ordered_map
                    else _build_dict_entry(
                        key_str=formatted_key,
                        val=v,
                        val_str=formatted_val,
                        spec=spec,
                    )
                )
                add_sep = i < last_idx or trailing_comma
                sep = spec.element_separator.strip() if add_sep else ""
                lines.append(f"{body_prefix}{entry}{sep}")
        case set() as set_data:
            sorted_items = sorted(
                set_data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            last_idx = len(sorted_items) - 1
            for i, item in enumerate(iterable=sorted_items):
                formatted = _format_value(
                    value=item,
                    spec=spec,
                    dict_open_override=None,
                )
                entry = spec.format_set_entry(item, formatted)
                add_sep = i < last_idx or trailing_comma
                sep = spec.element_separator.strip() if add_sep else ""
                lines.append(f"{body_prefix}{entry}{sep}")
        case list() as list_data:
            seq_trailing = (
                trailing_comma
                and spec.sequence_format_config.supports_trailing_comma
            )
            dict_open_override = _compute_sequence_dict_override(
                items=list_data,
                spec=spec,
            )
            last_idx = len(list_data) - 1
            for i, element in enumerate(iterable=list_data):
                formatted = spec.format_sequence_entry(
                    element,
                    _format_value(
                        value=element,
                        spec=spec,
                        dict_open_override=dict_open_override,
                    ),
                )
                add_sep = i < last_idx or seq_trailing
                sep = spec.element_separator.strip() if add_sep else ""
                lines.append(f"{body_prefix}{formatted}{sep}")
        case _ as unreachable:
            assert_never(unreachable)
    return lines


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: Value,
    language: Language,
    line_prefix: str,
    include_delimiters: bool,
    error_on_coercion: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the language's
    indent.

    Args:
        data: A scalar, sequence, or mapping.  Scalars (strings,
            numbers, booleans, ``None``, :class:`datetime.date`,
            :class:`datetime.datetime`) are formatted as a single
            literal value.  Sequences may contain scalars, sequences,
            or mappings with nesting to arbitrary depth.  Mappings are
            formatted as one key-value pair per line using the
            language's dict separator.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        line_prefix: String to prepend to every output line
            (e.g. ``"        "`` for 8-space margin, or ``"\t\t"``
            for 2-tab margin).  Positions the generated block at
            the right column in surrounding source code.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
            Ignored for scalar values.
        error_on_coercion: If ``True``, raise
            :exc:`~literalizer.exceptions.HeterogeneousCoercionError`
            instead of silently coercing heterogeneous scalar
            collections to strings.
    """
    spec = language
    data = _apply_coercions(
        data=data,
        spec=spec,
        error_on_coercion=error_on_coercion,
    )

    # Handle scalars (check ``str`` before Sequence since ``str`` is a
    # Sequence, and datetime before date since datetime subclasses
    # date).
    scalar_types = (
        str,
        bytes,
        int,
        float,
        bool,
        datetime.datetime,
        datetime.date,
    )
    if isinstance(data, scalar_types) or data is None:
        return f"{line_prefix}{_format_scalar(value=data, spec=spec)}"

    # Empty collections have no elements to lay out line-by-line, so
    # delegate to _format_value which already returns the correct
    # compact representation (e.g. ``{}``, ``[]``).
    if not data and include_delimiters:
        formatted = _format_value(
            value=data,
            spec=spec,
            dict_open_override=None,
        )
        return f"{line_prefix}{formatted}"

    body_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    is_ordered_map = isinstance(data, ordereddict)
    trailing_comma = spec.trailing_comma_config.multiline_trailing_comma
    lines_or_early = _format_collection_lines(
        data=data,
        spec=spec,
        body_prefix=body_prefix,
        trailing_comma=trailing_comma,
        is_ordered_map=is_ordered_map,
        include_delimiters=include_delimiters,
    )

    if isinstance(lines_or_early, str):
        return f"{line_prefix}{lines_or_early}"

    body = "\n".join(lines_or_early)

    if not include_delimiters or not body:
        return body

    return _wrap_body(
        body=body,
        is_ordered_map=is_ordered_map,
        data=data,
        spec=spec,
        line_prefix=line_prefix,
    )


@beartype
def _apply_variable_wrapper(
    *,
    result: str,
    language: Language,
    data: Value,
    variable_name: str | None,
    new_variable: bool,
) -> str:
    """Optionally wrap *result* in a variable declaration or
    assignment.
    """
    if variable_name is None:
        return result
    formatter = (
        language.format_variable_declaration
        if new_variable
        else language.format_variable_assignment
    )
    return formatter(variable_name, result, data)


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    pre_indent_level: int,
    include_delimiters: bool,
    variable_name: str | None,
    new_variable: bool,
    error_on_coercion: bool,
) -> LiteralizeResult:
    r"""Convert a JSON string to native language literal text.

    Convert a JSON string to native language literal text.

    Args:
        json_string: A JSON string representing a scalar, array, or
            object.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        pre_indent_level: Number of ``indent`` steps to prepend to
            every output line.  For example, ``2`` with a 4-space
            indent produces an 8-space margin.  Defaults to ``0``.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
        variable_name: If given, wrap the output in a variable
            declaration using the language's
            ``format_variable_declaration`` or
            ``format_variable_assignment`` callable.
        new_variable: If ``True`` (the default), use
            ``format_variable_declaration`` (e.g. ``const x =`` in
            JavaScript).  If ``False``, use
            ``format_variable_assignment`` (e.g. ``x =``).  Only
            relevant when *variable_name* is given.
        error_on_coercion: If ``True``, raise
            :exc:`~literalizer.exceptions.HeterogeneousCoercionError`
            instead of silently coercing heterogeneous scalar
            collections to strings.  Only has an effect when the
            the language's sequence format does not support
            heterogeneity.

    Raises:
        JSONParseError: If *json_string* is not valid JSON.
        HeterogeneousCoercionError: If *error_on_coercion* is ``True``
            and the data contains heterogeneous scalar collections
            that would be coerced.
    """
    line_prefix = language.indent * pre_indent_level
    try:
        data = json.loads(s=json_string)
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        )
        raise JSONParseError(message) from exc
    result = _literalize(
        data=data,
        language=language,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
        error_on_coercion=error_on_coercion,
    )
    if variable_name is not None:
        formatter = (
            language.format_variable_declaration
            if new_variable
            else language.format_variable_assignment
        )
        result = formatter(variable_name, result, data)
    computed = _compute_preamble(
        data=data,
        language=language,
        has_variable_declaration=variable_name is not None and new_variable,
    )
    preamble = tuple(language.static_preamble) + computed.header
    if computed.body:
        result = "\n".join(computed.body) + "\n" + result
    return LiteralizeResult(
        code=result,
        preamble=preamble,
    )


@beartype
def _filter_null_dict_comments(
    *,
    data: dict[Any, Any],
    ruamel_data: CommentedMap,
    collection_comments: CollectionComments,
) -> CollectionComments:
    """Remove comments for null-valued dict entries.

    When a language skips null dict values, the associated comments
    are redistributed to the next non-null entry.
    """
    pending: list[str] = []
    filtered_elements_list: list[ElementComments] = []
    for key, ec in zip(  # pyright: ignore[reportUnknownVariableType]
        ruamel_data.keys(),  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        collection_comments.elements,
        strict=True,
    ):
        if data[key] is None:
            pending.extend(ec.before)
            if ec.inline:
                pending.append(ec.inline)
        else:
            new_before = (*pending, *ec.before)
            pending = []
            filtered_elements_list.append(
                dataclasses.replace(ec, before=new_before),
            )
    return dataclasses.replace(
        collection_comments,
        elements=tuple(filtered_elements_list),
        trailing=(*pending, *collection_comments.trailing),
    )


@dataclasses.dataclass(frozen=True)
class _ResolvedComments:
    """Result of resolving YAML comments for a collection."""

    result: str
    pending: CollectionComments | None


@beartype
def _resolve_yaml_set_comments(
    *,
    ruamel_set: CommentedSet,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> _ResolvedComments:
    """Resolve comments for a YAML set."""
    set_comments = extract_yaml_comments(ruamel_data=ruamel_set)
    if not language.supports_collection_comments:
        return _ResolvedComments(result=base, pending=set_comments)
    result = apply_collection_comments(
        collection_comments=set_comments,
        base=base,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
    return _ResolvedComments(result=result, pending=None)


@beartype
def _resolve_yaml_collection_comments(
    *,
    ruamel_data: CommentedSeq | CommentedMap,
    data: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> _ResolvedComments:
    """Resolve comments for a YAML list or dict."""
    collection_comments = extract_yaml_comments(
        ruamel_data=ruamel_data,
    )

    if (
        language.skip_null_dict_values
        and isinstance(ruamel_data, CommentedMap)
        and isinstance(data, dict)
    ):
        collection_comments = _filter_null_dict_comments(
            data=data,  # pyright: ignore[reportUnknownArgumentType]
            ruamel_data=ruamel_data,
            collection_comments=collection_comments,
        )

    if not language.supports_collection_comments:
        return _ResolvedComments(
            result=base,
            pending=collection_comments,
        )
    result = apply_collection_comments(
        collection_comments=collection_comments,
        base=base,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
    return _ResolvedComments(result=result, pending=None)


@beartype
def _resolve_yaml_comments(
    *,
    yaml_string: str,
    data: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    line_prefix: str,
    include_delimiters: bool,
) -> _ResolvedComments:
    """Parse YAML for comment metadata and resolve comments."""
    if isinstance(data, set):
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        ruamel_set: CommentedSet = YAML().load(  # pyright: ignore[reportUnknownMemberType]
            stream=StringIO(initial_value=yaml_string),
        )
        return _resolve_yaml_set_comments(
            ruamel_set=ruamel_set,
            base=base,
            language=language,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            comment_line_prefix=comment_line_prefix,
            include_delimiters=include_delimiters,
        )

    if not isinstance(data, (list, dict)):
        stream = StringIO(initial_value=yaml_string)
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        tokens = YAML().scan(stream=stream)  # pyright: ignore[reportUnknownMemberType]
        result = literalize_yaml_scalar(
            tokens=tokens,
            base=base,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
        )
        return _ResolvedComments(result=result, pending=None)

    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ruamel_data: CommentedSeq | CommentedMap = YAML().load(  # pyright: ignore[reportUnknownMemberType]
        stream=StringIO(initial_value=yaml_string),
    )
    return _resolve_yaml_collection_comments(
        ruamel_data=ruamel_data,
        data=data,  # pyright: ignore[reportUnknownArgumentType]
        base=base,
        language=language,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )


@beartype
def literalize_yaml(
    *,
    yaml_string: str,
    language: Language,
    pre_indent_level: int,
    include_delimiters: bool,
    variable_name: str | None,
    new_variable: bool,
    error_on_coercion: bool,
) -> LiteralizeResult:
    r"""Convert a YAML string to native language literal text.

    YAML comments are preserved in the output using the target
    language's comment syntax.  The comment prefix is read from the
    ``comment_prefix`` attribute of *language* (defaulting to
    ``"#"`` when the attribute is absent).

    Args:
        yaml_string: A YAML string representing a scalar, sequence, or
            mapping.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        pre_indent_level: Number of ``indent`` steps to prepend to
            every output line.  For example, ``2`` with a 4-space
            indent produces an 8-space margin.  Defaults to ``0``.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
        variable_name: If given, wrap the output in a variable
            declaration using the language's
            ``format_variable_declaration`` or
            ``format_variable_assignment`` callable.
        new_variable: If ``True`` (the default), use
            ``format_variable_declaration`` (e.g. ``const x =`` in
            JavaScript).  If ``False``, use
            ``format_variable_assignment`` (e.g. ``x =``).  Only
            relevant when *variable_name* is given.
        error_on_coercion: If ``True``, raise
            :exc:`~literalizer.exceptions.HeterogeneousCoercionError`
            instead of silently coercing heterogeneous scalar
            collections to strings.  Only has an effect when the
            the language's sequence format does not support
            heterogeneity.

    Raises:
        YAMLParseError: If *yaml_string* is not valid YAML.
        HeterogeneousCoercionError: If *error_on_coercion* is ``True``
            and the data contains heterogeneous scalar collections
            that would be coerced.
    """
    line_prefix = language.indent * pre_indent_level
    ruamel_yaml = YAML(typ="safe")
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        data = ruamel_yaml.load(stream=yaml_string)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    coerced_data = _coerce_yaml_keys(data=data)
    base = _literalize(
        data=coerced_data,
        language=language,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
        error_on_coercion=error_on_coercion,
    )

    comment_cfg = language.comment_config
    cp = comment_cfg.prefix
    cs = comment_cfg.suffix
    comment_line_prefix = (
        line_prefix + language.indent if include_delimiters else line_prefix
    )

    resolved = _resolve_yaml_comments(
        yaml_string=yaml_string,
        data=data,
        base=base,
        language=language,
        comment_prefix=cp,
        comment_suffix=cs,
        comment_line_prefix=comment_line_prefix,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
    )
    result = resolved.result

    result = _apply_variable_wrapper(
        result=result,
        language=language,
        data=coerced_data,
        variable_name=variable_name,
        new_variable=new_variable,
    )

    if resolved.pending is not None:
        result = prepend_collection_comments(
            collection_comments=resolved.pending,
            base=result,
            comment_prefix=cp,
            comment_suffix=cs,
            line_prefix=line_prefix,
        )

    computed = _compute_preamble(
        data=coerced_data,
        language=language,
        has_variable_declaration=variable_name is not None and new_variable,
    )
    preamble = tuple(language.static_preamble) + computed.header
    if computed.body:
        result = "\n".join(computed.body) + "\n" + result
    return LiteralizeResult(
        code=result,
        preamble=preamble,
    )
