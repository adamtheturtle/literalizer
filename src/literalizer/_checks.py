"""Checks that raise when data is incompatible with a language's
collection-shape constraints.
"""

import datetime
from collections.abc import Sequence

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._language import Language
from literalizer._types import Value
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSetError,
    HeterogeneousSiblingListsError,
    MixedDictShapesError,
    MixedDictValuesError,
    MixedListValuesError,
)


@beartype
def scalar_type_bucket(*, value: Value) -> type | None:
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
def _scalar_type_buckets(
    *,
    values: Sequence[Value],
) -> set[type] | None:
    """Return the set of scalar type buckets for *values*.

    Returns ``None`` if any value is not a scalar.
    """
    buckets: set[type] = set()
    for v in values:
        bucket = scalar_type_bucket(value=v)
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
def _value_type_family(*, value: Value) -> str:
    """Return a broad type family label for a value."""
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
def _values_mixed_types(*, values: Sequence[Value]) -> bool:
    """Check whether values span more than one type family."""
    if len(values) <= 1:
        return False
    families: set[str] = set()
    for v in values:
        families.add(_value_type_family(value=v))
    return len(families) > 1


@beartype
def _collect_scalar_type_names(*, data: Value) -> set[str]:
    """Collect the names of scalar type buckets found in *data*."""
    names: set[str] = set()
    match data:
        case ordereddict() | dict():
            for v in data.values():  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
                names |= _collect_scalar_type_names(data=v)  # pyright: ignore[reportUnknownArgumentType]
        case list():
            for v in data:
                names |= _collect_scalar_type_names(data=v)
        case set():
            for v in data:
                names |= _collect_scalar_type_names(data=v)
        case _:
            names.add(_value_type_family(value=data))
    return names


@beartype
def _describe_heterogeneous_types(*, data: Value) -> str:
    """Return a sorted, comma-separated string of scalar type names in
    *data*.
    """
    return ", ".join(sorted(_collect_scalar_type_names(data=data)))


@beartype
def _find_first_mixed_values(
    *,
    data: Value,
    container_type: type,
) -> Sequence[Value]:
    """Return the first collection of children in *data* that spans
    multiple type families.
    """
    children: Sequence[Value]
    match data:
        case ordereddict() | dict():
            children = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            if container_type is dict and _values_mixed_types(
                values=children,
            ):
                return children
        case list():
            children = data
            if container_type is list and _values_mixed_types(
                values=children,
            ):
                return children
        case _:
            return []
    for child in children:
        result = _find_first_mixed_values(
            data=child,
            container_type=container_type,
        )
        if result:
            return result
    return []


@beartype
def _describe_mixed_type_families(
    *,
    data: Value,
    container_type: type,
) -> str:
    """Return a sorted, comma-separated string of type families for the
    first collection in *data* whose children span multiple families.
    """
    values = _find_first_mixed_values(
        data=data,
        container_type=container_type,
    )
    return ", ".join(sorted({_value_type_family(value=v) for v in values}))


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

    Sibling lists are detected both as the direct children of a list
    and as the values of a dict.
    """
    match data:
        case dict() | ordereddict():
            values = list(data.values())  # pyright: ignore[reportUnknownArgumentType,reportUnknownMemberType]
            if any(_has_heterogeneous_sibling_lists(data=v) for v in values):
                return True
            sublists: list[list[Value]] = [
                v for v in values if isinstance(v, list)
            ]
            return (
                len(sublists) == len(values)
                and len(sublists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in sublists for e in sub],
                )
            )
        case list():
            if any(_has_heterogeneous_sibling_lists(data=v) for v in data):
                return True
            list_sublists: list[list[Value]] = [
                v for v in data if isinstance(v, list)
            ]
            return (
                len(list_sublists) == len(data)
                and len(list_sublists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in list_sublists for e in sub],
                )
            )
        case _:
            return False


@beartype
def _has_mixed_dict_shapes(*, data: Value) -> bool:
    """Recursively check whether data contains any list of dicts
    with different key sets.
    """
    match data:
        case ordereddict() | dict():
            return any(
                _has_mixed_dict_shapes(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            )
        case list():
            dicts_in_list = [v for v in data if isinstance(v, dict)]
            key_sets = {frozenset(d.keys()) for d in dicts_in_list}
            has_mixed = (
                not all(ks == next(iter(key_sets)) for ks in key_sets)
                if key_sets
                else False
            )
            if has_mixed:
                return True
            return any(_has_mixed_dict_shapes(data=v) for v in data)
        case _:
            return False


@beartype
def _has_mixed_dict_values(*, data: Value) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families.
    """
    match data:
        case ordereddict() | dict():
            values: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            if _values_mixed_types(values=values):
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
            if _values_mixed_types(values=data):
                return True
            return any(_has_mixed_list_values(data=v) for v in data)
        case _:
            return False


@beartype
def _has_heterogeneous_set(*, data: Value) -> bool:
    """Recursively check whether data contains any set with
    heterogeneous scalar elements.
    """
    match data:
        case set():
            return _all_scalars_heterogeneous(values=list(data))
        case ordereddict() | dict():
            return any(
                _has_heterogeneous_set(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            )
        case list():
            return any(_has_heterogeneous_set(data=v) for v in data)
        case _:
            return False


@beartype
def _check_heterogeneous(*, data: Value) -> None:
    """Raise if data contains heterogeneous all-scalar collections."""
    if _has_heterogeneous(data=data):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Collection contains heterogeneous scalar types that cannot "
            "be represented in the target language "
            f"(found types: {types})"
        )
        raise HeterogeneousScalarCollectionError(msg)


@beartype
def _check_heterogeneous_sibling_lists(*, data: Value) -> None:
    """Raise if sibling lists have heterogeneous scalar types."""
    if _has_heterogeneous_sibling_lists(data=data):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Sibling lists contain heterogeneous scalar types that "
            "cannot be represented in the target language "
            f"(found types: {types})"
        )
        raise HeterogeneousSiblingListsError(msg)


@beartype
def _check_mixed_dict_shapes(*, data: Value) -> None:
    """Raise if data contains dicts with different key sets."""
    if _has_mixed_dict_shapes(data=data):
        msg = (
            "List contains dicts with different key sets that cannot "
            "be represented in the target language"
        )
        raise MixedDictShapesError(msg)


@beartype
def _check_mixed_dict_values(*, data: Value) -> None:
    """Raise if any dict has values spanning multiple type families."""
    if _has_mixed_dict_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=dict,
        )
        msg = (
            "Dict contains values of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedDictValuesError(msg)


@beartype
def _check_mixed_list_values(*, data: Value) -> None:
    """Raise if any list has elements spanning multiple type families."""
    if _has_mixed_list_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=list,
        )
        msg = (
            "List contains elements of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedListValuesError(msg)


@beartype
def _check_heterogeneous_set(*, data: Value) -> None:
    """Raise if data contains a set with heterogeneous scalar elements."""
    if _has_heterogeneous_set(data=data):
        msg = (
            "Set contains heterogeneous scalar elements that cannot be "
            "represented in the target language"
        )
        raise HeterogeneousSetError(msg)


@beartype
def check_data(*, data: Value, spec: Language) -> None:
    """Check that *data* fits the language's collection-shape
    constraints.

    Raises a subclass of
    :exc:`~literalizer.exceptions.HeterogeneousCollectionError` when the
    data cannot be represented in the target language's collection
    formats.
    """
    if spec.sequence_format_config.requires_uniform_record_shapes:
        _check_mixed_dict_shapes(data=data)

    seq_supports_het = spec.sequence_format_config.supports_heterogeneity
    dict_supports_het = spec.dict_supports_heterogeneous_values
    if not spec.heterogeneous_behavior.skip_scalar_checks:
        if not seq_supports_het:
            _check_heterogeneous(data=data)
            _check_heterogeneous_sibling_lists(data=data)
        if not dict_supports_het:
            _check_mixed_dict_values(data=data)
        if not seq_supports_het:
            _check_mixed_list_values(data=data)

    if not spec.set_format_config.supports_heterogeneity:
        _check_heterogeneous_set(data=data)
