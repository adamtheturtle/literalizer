"""Compute preamble lines for the types present in literalized data."""

import dataclasses
import datetime
import math
from collections import OrderedDict
from typing import assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._checks import scalar_type_bucket
from literalizer._language import Language
from literalizer._types import Scalar, Value


class HeterogeneousElements:
    """Sentinel added to ``annotated_collection_types`` when the data
    contains annotated collections whose element types produce a union
    (i.e. ``Union[A, B]`` or ``A | B`` in the generated type hint).

    Languages that need to import a union-type helper only when it is
    actually used (e.g. Python 3.8's ``from typing import Union``) can
    check for this sentinel in their
    ``type_hint_collection_preamble_lines`` callable.
    """


@beartype
def _collect_value_types(*, data: Value) -> frozenset[type]:
    """Return the set of Python types present in *data*."""
    match data:
        case dict():
            child_types: frozenset[type] = frozenset()
            for k, v in data.items():
                child_types = child_types | _collect_value_types(data=k)
                child_types = child_types | _collect_value_types(data=v)
            container_type = (
                ordereddict if isinstance(data, ordereddict) else dict
            )
            # ``str`` is included unconditionally because typed-map
            # languages whose dict opener hard-codes the default key
            # type (e.g. ``std::map<std::string, ...>`` in C++) still
            # need the string preamble even when the data has no string
            # keys or values.  The actual rendered code references
            # ``std::string`` regardless of payload.
            return frozenset({container_type, str}) | child_types
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
def _needs_annotation(val: Value) -> bool:
    """Return True if *val* requires a type annotation.

    A collection needs annotation when it is empty (so type-checkers can
    infer element types) or contains an element/value that itself needs
    annotation.
    """
    match val:
        case dict():
            return not val or any(
                _needs_annotation(val=v) for v in val.values()
            )
        case set():
            return not val
        case list():
            return not val or any(_needs_annotation(val=v) for v in val)
        case _:
            return False


@beartype
def _walk_annotated_collections(  # noqa: C901, PLR0912  # pylint: disable=too-complex,too-many-branches
    *,
    val: Value,
    result: set[type],
) -> None:
    """Walk *val* and add collection types that appear in type annotations."""
    match val:
        case ordereddict():
            if _needs_annotation(val=val):
                result.add(ordereddict)
                for v in val.values():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                    _walk_annotated_collections(val=v, result=result)  # pyright: ignore[reportUnknownArgumentType]
        case dict():
            if _needs_annotation(val=val):
                result.add(dict)
                for v in val.values():
                    _walk_annotated_collections(val=v, result=result)
        case set():
            if not val:
                result.add(set)
        case list():
            if _needs_annotation(val=val):
                result.add(list)
                for v in val:
                    _walk_annotated_collections(val=v, result=result)
                    match v:
                        case ordereddict():
                            result.add(ordereddict)
                        case dict():
                            result.add(dict)
                        case set():
                            result.add(set)
                        case list():
                            result.add(list)
                        case _:
                            pass
        case _:
            pass


@beartype
def _collect_annotated_collection_types(*, data: Value) -> frozenset[type]:
    """Return the set of collection types that appear in type annotations.

    This is a superset of empty collection types: it also includes
    non-empty containers that wrap annotated children.
    """
    result: set[type] = set()
    _walk_annotated_collections(val=data, result=result)
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
def deduplicate_preamble_entries(
    *,
    entries: tuple[str, ...],
) -> tuple[str, ...]:
    """Remove duplicate preamble entries preserving first-seen order.

    An entry is usually one source line, but callers may also represent
    a multi-line preamble block as one string.
    """
    seen: set[str] = set()
    result: list[str] = []
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            result.append(entry)
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


def _list_merge_dicts(*, elements: list[Value]) -> list[Value]:
    """Return *elements* with plain dicts pooled and ordered dicts pooled.

    Mirrors the ``merge_dicts=True`` behavior used by Python's
    ``_collection_element_union`` for sequence elements: all plain-dict
    siblings are merged into a single representative dict (likewise for
    ordered-dict siblings) so that the element-type union is computed on
    the merged result rather than on each individual dict.
    """
    plain_vals: list[Value] = []
    ordered_vals: list[Value] = []
    non_dict: list[Value] = []
    has_plain = False
    has_ordered = False
    for elem in elements:
        match elem:
            case ordereddict() | OrderedDict():
                has_ordered = True
                ordered_vals.extend(
                    elem.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                )
            case dict():
                has_plain = True
                plain_vals.extend(elem.values())
            case _:
                non_dict.append(elem)
    merged: list[Value] = list(non_dict)
    if has_plain:
        merged_plain: dict[Scalar, Value] = {
            str(object=i): v for i, v in enumerate(iterable=plain_vals)
        }
        merged.append(merged_plain)
    if has_ordered:
        merged_ordered: dict[Scalar, Value] = ordereddict(
            {str(object=i): v for i, v in enumerate(iterable=ordered_vals)}
        )
        merged.append(merged_ordered)
    return merged


def _structural_type_id(  # noqa: C901, PLR0911, PLR0912  # pylint: disable=too-complex,too-many-branches,too-many-return-statements
    *,
    value: Value,
) -> str:
    """Return a structural type identifier for *value*.

    Two values produce the same ID if and only if Python's
    ``_python_type_hint`` would return the same string for them
    (regardless of the concrete type-hint names configured for the
    language, e.g. ``Tuple`` vs ``tuple``).

    This is used by :func:`_has_union_in_type_hints` to detect whether
    element types are heterogeneous without actually running the full
    type-hint formatter.
    """
    match value:
        case bool():
            return "bool"
        case int():
            return "int"
        case float():
            return "float"
        case str():
            return "str"
        case bytes():
            return "bytes"
        case datetime.datetime():
            return "datetime"
        case datetime.time():
            return "time"
        case datetime.date():
            return "date"
        case None:
            return "None"
        case list() if not value:
            return "empty_list"
        case list():
            merged = _list_merge_dicts(elements=value)
            elem_ids = list(
                dict.fromkeys(_structural_type_id(value=e) for e in merged)
            )
            return f"list({','.join(elem_ids)})"
        case set() if not value:
            return "empty_set"
        case set():
            elem_ids = sorted({_structural_type_id(value=e) for e in value})
            return f"set({','.join(elem_ids)})"
        case ordereddict() | OrderedDict() if not value:
            return "empty_odict"
        case ordereddict() | OrderedDict():
            val_set: set[str] = set()
            for ov in value.values():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                val_set.add(
                    _structural_type_id(value=ov)  # pyright: ignore[reportUnknownArgumentType]
                )
            val_ids = sorted(val_set)
            return f"odict({','.join(val_ids)})"
        case dict() if not value:
            return "empty_dict"
        case dict():
            val_ids = sorted(
                {_structural_type_id(value=v) for v in value.values()}
            )
            return f"dict({','.join(val_ids)})"
        case _ as unreachable:
            assert_never(unreachable)


def _has_union_in_type_hints(*, data: Value) -> bool:
    """Return ``True`` if the Python type hints for *data* would contain
    a union (``Union[A, B]`` or ``A | B``).

    Walks *data* recursively and applies the same ``merge_dicts=True``
    logic that Python's sequence type-hint formatter uses, so the result
    is accurate without running the full formatter.
    """
    match data:
        case list():
            merged = _list_merge_dicts(elements=data)
            type_ids = list(
                dict.fromkeys(_structural_type_id(value=e) for e in merged)
            )
            if len(type_ids) > 1:
                return True
            return any(_has_union_in_type_hints(data=e) for e in merged)
        case dict():
            if data:
                val_ids = list(
                    dict.fromkeys(
                        _structural_type_id(value=v) for v in data.values()
                    )
                )
                if len(val_ids) > 1:
                    return True
            return any(_has_union_in_type_hints(data=v) for v in data.values())
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
    annotated_collection_types: frozenset[type] = (
        _collect_annotated_collection_types(data=data)
        if has_variable_declaration and types & {dict, list, set, ordereddict}
        else frozenset()
    )
    if annotated_collection_types and _has_union_in_type_hints(data=data):
        annotated_collection_types = annotated_collection_types | frozenset(
            {HeterogeneousElements}
        )
    type_hint = (
        language.type_hint_collection_preamble_lines(
            annotated_collection_types
        )
        if annotated_collection_types
        else ()
    )
    body = language.compute_body_preamble(types, data)
    return _PreambleResult(
        header=deduplicate_preamble_entries(
            entries=scalar + special_float + collection + type_hint,
        )
        + tuple(language.static_body_preamble),
        body=body,
        types_present=types,
    )
