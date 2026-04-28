"""Type inference for homogeneous collections."""

from dataclasses import dataclass, field

from beartype import beartype
from ruamel.yaml.compat import ordereddict as _ordereddict

from literalizer._types import Value


@dataclass(frozen=True)
class ListType:
    """Represents a homogeneous list element type for type inference.

    For nested lists, ``inner`` is another ``ListType``.
    For leaf lists, ``inner`` is a Python ``type``.
    """

    inner: "type | ListType | DictType"


@dataclass(frozen=True)
class DictType:
    """Represents a homogeneous dict element type for type inference.

    ``value_type`` is the inferred common value type across all dicts
    in a sequence, or ``None`` when values are empty or mixed.
    ``values`` is the flattened sequence of dict values used to infer
    ``value_type``; callers can reuse it to derive a language-specific
    type (e.g. ``std::variant``) without re-walking the source items.
    """

    value_type: "type | ListType | DictType | None"
    values: "tuple[Value, ...]" = field(compare=False)


class MixedNumeric:
    """Sentinel class representing mixed int/float element types.

    Used as a key in scalar type mapping dicts so each language can
    decide how to handle collections containing both int and float
    values.
    """


@dataclass(frozen=True)
class _Collected:
    """Per-item type buckets gathered for ``infer_element_type``."""

    element_types: set[type | ListType]
    dict_values: list[Value]


_INFER_FAILED = object()


def _collect_element_types(
    items: list[Value],
) -> _Collected | object:
    """Collect element types for ``items`` or signal hard inference
    failure.

    Empty inner lists are skipped so they do not poison inference of
    homogeneous siblings.  When every list item is empty (and there
    are no other items contributing a ``ListType``), ``_INFER_FAILED``
    is returned because no concrete inner type could be derived.
    """
    element_types: set[type | ListType] = set()
    dict_values: list[Value] = []
    saw_empty_list = False
    for item in items:
        match item:
            case []:
                saw_empty_list = True
            case list():
                inner = infer_element_type(items=item)
                if inner is None:
                    return _INFER_FAILED
                element_types.add(ListType(inner=inner))
            case dict() if not isinstance(item, _ordereddict):
                dict_values.extend(item.values())
                element_types.add(dict)
            case _:
                element_types.add(type(item))
    if saw_empty_list and not any(
        isinstance(t, ListType) for t in element_types
    ):
        return _INFER_FAILED
    return _Collected(element_types=element_types, dict_values=dict_values)


@beartype
def infer_element_type(
    items: list[Value],
) -> type | ListType | DictType | None:
    """Infer the common element type from a list of values.

    Returns ``None`` when the list is empty or contains mixed types
    that cannot be unified.  Returns ``MixedNumeric`` when the list
    contains a mix of ``int`` and ``float`` values.  Returns a
    ``DictType`` when all items are plain dicts (not ordered maps).
    """
    if not items:
        return None
    collected = _collect_element_types(items=items)
    if not isinstance(collected, _Collected):
        return None
    element_types = collected.element_types
    all_dict_values = collected.dict_values
    if len(element_types) == 1:
        the_type = next(iter(element_types))
        if the_type is dict:
            value_type = infer_element_type(items=all_dict_values)
            return DictType(
                value_type=value_type,
                values=tuple(all_dict_values),
            )
        return the_type
    if element_types == {int, float}:
        return MixedNumeric
    return None
