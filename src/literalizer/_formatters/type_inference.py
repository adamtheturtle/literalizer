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
    element_types: set[type | ListType] = set()
    all_dict_values: list[Value] = []
    for item in items:
        if isinstance(item, list):
            inner = infer_element_type(items=item)
            if inner is None:
                return None
            element_types.add(ListType(inner=inner))
        elif isinstance(item, dict) and not isinstance(item, _ordereddict):
            all_dict_values.extend(item.values())
            element_types.add(dict)
        else:
            element_types.add(type(item))
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
