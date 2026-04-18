"""Heterogeneous-type coercion and detection helpers."""

import dataclasses
import datetime
import json
from collections.abc import Callable, Sequence
from typing import Protocol

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._language import CoercionOptions, Language
from literalizer._types import Scalar, Value
from literalizer.exceptions import HeterogeneousCoercionError


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
def coerce_scalar_to_str(
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
        bucket = scalar_type_bucket(value=v)
        if bucket is None:
            return None
        buckets.add(bucket)
    return buckets


@beartype
def all_scalars_heterogeneous(
    *,
    values: Sequence[Value],
) -> bool:
    """Check whether values are all scalars with more than one type."""
    buckets = _scalar_type_buckets(values=values)
    return buckets is not None and len(buckets) > 1


@beartype
def _map_mapping_values(
    *,
    data: ordereddict | dict[str, Value],
    fn: Callable[[Value], Value],
) -> ordereddict | dict[str, Value]:
    """Apply a function to every value of a dict or ordereddict,
    preserving the container type.
    """
    if isinstance(data, ordereddict):
        result: ordereddict = ordereddict()
        for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
            result[k] = fn(v)  # pyright: ignore[reportUnknownArgumentType]
        return result
    return {k: fn(v) for k, v in data.items()}


@beartype
def _coerce_heterogeneous_sibling_lists(*, data: Value) -> Value:
    """Recursively coerce sibling lists with heterogeneous scalar
    element types so that every inner element becomes a string.

    For example, ``[[1, 2], ["a", "b"]]`` becomes
    ``[["1", "2"], ["a", "b"]]``.
    """
    match data:
        case dict() | ordereddict():
            return _map_mapping_values(
                data=data,
                fn=lambda v: _coerce_heterogeneous_sibling_lists(data=v),
            )
        case list():
            new_list = [
                _coerce_heterogeneous_sibling_lists(data=v) for v in data
            ]
            sublists: list[list[Value]] = []
            all_elements: list[Value] = []
            for v in new_list:
                if isinstance(v, list):
                    sublists.append(v)
                    all_elements.extend(v)
            if (
                len(sublists) == len(new_list)
                and len(sublists) > 1
                and all_scalars_heterogeneous(values=all_elements)
            ):
                return [
                    [coerce_scalar_to_str(value=e) for e in sub]
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
            return all_scalars_heterogeneous(values=list(data))
        case _:
            return False

    return any(
        _has_heterogeneous(data=v) for v in children
    ) or all_scalars_heterogeneous(values=children)


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
                and all_scalars_heterogeneous(
                    values=[e for sub in sublists for e in sub],
                )
            )
        case _:
            return False


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


def _describe_heterogeneous_types(*, data: Value) -> str:
    """Return a sorted, comma-separated string of scalar type names in
    *data*.
    """
    return ", ".join(sorted(_collect_scalar_type_names(data=data)))


def _find_first_mixed_values(
    *,
    data: Value,
    container_type: type,
) -> Sequence[Value]:
    """Return the first collection of children in *data* that spans
    multiple type families.

    Only considers collections whose immediate container matches
    *container_type* (``dict`` or ``list``).
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
def _check_heterogeneous(*, data: Value) -> None:
    """Recursively check for heterogeneous all-scalar collections and
    raise if found.
    """
    if _has_heterogeneous(data=data):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Collection contains heterogeneous scalar types "
            "that would be coerced to strings"
            f" (found types: {types})"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _check_mixed_dict_shapes(*, data: Value) -> None:
    """Raise if data contains dicts with different key sets."""
    if _has_mixed_dict_shapes(data=data):
        msg = (
            "List contains dicts with different key sets "
            "that would be padded with null values"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _check_heterogeneous_sibling_lists(*, data: Value) -> None:
    """Raise if sibling lists have heterogeneous scalar types."""
    if _has_heterogeneous_sibling_lists(data=data):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Collection contains heterogeneous scalar types "
            "that would be coerced to strings"
            f" (found types: {types})"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _check_mixed_dict_values(*, data: Value) -> None:
    """Raise if any dict has values spanning multiple type families."""
    if _has_mixed_dict_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=dict,
        )
        msg = (
            "Dict contains values of mixed types "
            "that would be coerced to strings"
            f" (found types: {types})"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _check_mixed_list_values(*, data: Value) -> None:
    """Raise if any list has elements spanning multiple type families."""
    if _has_mixed_list_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=list,
        )
        msg = (
            "List contains elements of mixed types "
            "that would be coerced to strings"
            f" (found types: {types})"
        )
        raise HeterogeneousCoercionError(msg)


@beartype
def _coerce_heterogeneous_mapping(
    *,
    data: ordereddict | dict[str, Value],
) -> ordereddict | dict[str, Value]:
    """Coerce a dict or ordereddict with heterogeneous scalar values."""
    new_mapping = _map_mapping_values(
        data=data,
        fn=lambda v: _coerce_heterogeneous_scalars(data=v),
    )
    values: list[Value] = list(new_mapping.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if all_scalars_heterogeneous(values=values):
        new_mapping = _map_mapping_values(
            data=new_mapping,
            fn=lambda v: coerce_scalar_to_str(value=v),
        )
    return new_mapping


@beartype
def _coerce_heterogeneous_set(
    *,
    data: set[Scalar],
) -> set[Scalar]:
    """Coerce a set with heterogeneous scalar values."""
    items: list[Value] = list(data)
    if all_scalars_heterogeneous(values=items):
        return {coerce_scalar_to_str(value=v) for v in items}
    return data


@beartype
def _coerce_heterogeneous_list(
    *,
    data: list[Value],
) -> list[Value]:
    """Coerce a list with heterogeneous scalar values."""
    new_list = [_coerce_heterogeneous_scalars(data=v) for v in data]
    if all_scalars_heterogeneous(values=new_list):
        return [coerce_scalar_to_str(value=v) for v in new_list]
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
        case ordereddict() | dict():
            return _coerce_heterogeneous_mapping(data=data)
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
def _values_mixed_types(*, values: Sequence[Value]) -> bool:
    """Check whether values span more than one type family."""
    if len(values) <= 1:
        return False
    families: set[str] = set()
    for v in values:
        families.add(_value_type_family(value=v))
    return len(families) > 1


@beartype
def _coerce_value_to_str(*, value: Value) -> str:
    """Convert any value (scalar or collection) to a string."""
    match value:
        case str():
            return value
        case None | bool() | int() | float() | bytes() | datetime.date():
            return coerce_scalar_to_str(value=value)
        case set():
            sorted_items = sorted(
                value,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            return json.dumps(obj=sorted_items, default=str)
        case _:
            return json.dumps(obj=value, default=str, sort_keys=False)


@beartype
def _coerce_mixed_dict_values(*, data: Value) -> Value:
    """Recursively coerce dicts whose values span multiple type families.

    When a dict has values of mixed types (e.g. strings and lists),
    all values are converted to strings so the dict becomes homogeneous.
    """
    match data:
        case ordereddict() | dict():
            values: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            if _values_mixed_types(values=values):
                return _map_mapping_values(
                    data=data,
                    fn=lambda v: _coerce_value_to_str(value=v),
                )
            return _map_mapping_values(
                data=data,
                fn=lambda v: _coerce_mixed_dict_values(data=v),
            )
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
        case ordereddict() | dict():
            return _map_mapping_values(
                data=data,
                fn=lambda v: _coerce_mixed_list_values(data=v),
            )
        case list():
            if _values_mixed_types(values=data):
                return [_coerce_value_to_str(value=v) for v in data]
            return [_coerce_mixed_list_values(data=v) for v in data]
        case _:
            return data


@beartype
def _coerce_mixed_dict_shapes(*, data: Value) -> Value:
    """Recursively pad dicts in lists so every dict has the same keys.

    When a list contains dicts with different key sets, each dict is
    padded with ``None`` for any missing keys so the records become
    structurally uniform.
    """
    match data:
        case ordereddict() | dict():
            return _map_mapping_values(
                data=data,
                fn=lambda v: _coerce_mixed_dict_shapes(data=v),
            )
        case list():
            new_list = [_coerce_mixed_dict_shapes(data=v) for v in data]
            dicts_in_list = [v for v in new_list if isinstance(v, dict)]
            key_sets = {frozenset(d.keys()) for d in dicts_in_list}
            needs_padding = (
                not all(ks == next(iter(key_sets)) for ks in key_sets)
                if key_sets
                else False
            )
            if needs_padding:
                all_keys: list[str] = []
                seen: set[str] = set()
                for d in dicts_in_list:
                    for k in d:
                        if k not in seen:
                            all_keys.append(k)
                            seen.add(k)
                new_list = [
                    (
                        {k: v.get(k) for k in all_keys}
                        if isinstance(v, dict)
                        else v
                    )
                    for v in new_list
                ]
            return new_list
        case _:
            return data


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


class _CheckFn(Protocol):
    """Protocol for coercion check functions."""

    def __call__(self, *, data: Value) -> None:
        """Raise if the data violates the coercion constraint."""


class _CoerceFn(Protocol):
    """Protocol for coercion transform functions."""

    def __call__(self, *, data: Value) -> Value:
        """Return the data with the coercion applied."""


@dataclasses.dataclass(frozen=True)
class _CoercionStep:
    """A single coercion: a check that raises on error, a transform
    that applies the coercion, and the option-flag name that gates it.
    """

    check: _CheckFn
    coerce: _CoerceFn
    option_name: str


def _build_coercion_steps(
    *,
    spec: Language,
) -> list[_CoercionStep]:
    """Build the ordered list of coercion steps for the given spec."""
    steps: list[_CoercionStep] = []

    if spec.sequence_format_config.requires_uniform_record_shapes:
        steps.append(
            _CoercionStep(
                check=_check_mixed_dict_shapes,
                coerce=_coerce_mixed_dict_shapes,
                option_name="coerce_nonuniform_record_shapes",
            )
        )

    steps.extend(
        [
            _CoercionStep(
                check=_check_heterogeneous,
                coerce=_coerce_heterogeneous_scalars,
                option_name="coerce_heterogeneous_scalars",
            ),
            _CoercionStep(
                check=_check_heterogeneous_sibling_lists,
                coerce=_coerce_heterogeneous_sibling_lists,
                option_name="coerce_heterogeneous_sibling_lists",
            ),
            _CoercionStep(
                check=_check_mixed_dict_values,
                coerce=_coerce_mixed_dict_values,
                option_name="coerce_mixed_dict_values",
            ),
            _CoercionStep(
                check=_check_mixed_list_values,
                coerce=_coerce_mixed_list_values,
                option_name="coerce_mixed_list_values",
            ),
        ]
    )

    return steps


def apply_coercions(
    *,
    data: Value,
    spec: Language,
) -> Value:
    """Apply heterogeneous-type coercions controlled by the sequence
    format and the language's per-coercion opt-in flags.
    """
    if not spec.sequence_format_config.supports_heterogeneity:
        # Heterogeneous-only languages don't need to set coercion_options
        # — they never enter this branch.  Languages that *can* select a
        # non-heterogeneous format must set it on the instance.
        options = getattr(spec, "coercion_options", CoercionOptions())
        for step in _build_coercion_steps(spec=spec):
            if getattr(options, step.option_name):
                data = step.coerce(data=data)
            else:
                step.check(data=data)
    return data
