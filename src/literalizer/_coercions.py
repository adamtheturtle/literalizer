"""Constraints on data for languages whose sequence format is not
heterogeneous.
"""

import dataclasses
import datetime
from collections.abc import Sequence
from typing import Protocol

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._language import Language
from literalizer._types import Value
from literalizer.exceptions import (
    HeterogeneousScalarTypesError,
    HeterogeneousSiblingListScalarsError,
    InconsistentRecordKeysError,
    MixedMappingValueTypesError,
    MixedSequenceElementTypesError,
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
def all_scalars_heterogeneous(
    *,
    values: Sequence[Value],
) -> bool:
    """Check whether values are all scalars with more than one type."""
    buckets = _scalar_type_buckets(values=values)
    return buckets is not None and len(buckets) > 1


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
            f"(found types: {types})"
        )
        raise HeterogeneousScalarTypesError(msg)


@beartype
def _check_mixed_dict_shapes(*, data: Value) -> None:
    """Raise if data contains dicts with different key sets."""
    if _has_mixed_dict_shapes(data=data):
        msg = (
            "List contains dicts with different key sets; all records "
            "must share the same keys for this format."
        )
        raise InconsistentRecordKeysError(msg)


@beartype
def _check_heterogeneous_sibling_lists(*, data: Value) -> None:
    """Raise if sibling lists have heterogeneous scalar types."""
    if _has_heterogeneous_sibling_lists(data=data):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Sibling lists contain heterogeneous scalar types when "
            f"combined (found types: {types})"
        )
        raise HeterogeneousSiblingListScalarsError(msg)


@beartype
def _check_mixed_dict_values(*, data: Value) -> None:
    """Raise if any dict has values spanning multiple type families."""
    if _has_mixed_dict_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=dict,
        )
        msg = (
            "Dict values use incompatible broad types "
            f"(found types: {types})"
        )
        raise MixedMappingValueTypesError(msg)


@beartype
def _check_mixed_list_values(*, data: Value) -> None:
    """Raise if any list has elements spanning multiple type families."""
    if _has_mixed_list_values(data=data):
        types = _describe_mixed_type_families(
            data=data,
            container_type=list,
        )
        msg = (
            "List elements use incompatible broad types "
            f"(found types: {types})"
        )
        raise MixedSequenceElementTypesError(msg)


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
    """Protocol for validation check functions."""

    def __call__(self, *, data: Value) -> None:
        """Raise if the data violates the constraint."""


@dataclasses.dataclass(frozen=True)
class _ValidationStep:
    """One ordered validation step for homogeneous sequence formats."""

    check: _CheckFn


def _build_validation_steps(
    *,
    spec: Language,
) -> list[_ValidationStep]:
    """Build validation steps for the given spec."""
    steps: list[_ValidationStep] = []

    if spec.sequence_format_config.requires_uniform_record_shapes:
        steps.append(_ValidationStep(check=_check_mixed_dict_shapes))

    steps.extend(
        [
            _ValidationStep(check=_check_heterogeneous),
            _ValidationStep(check=_check_heterogeneous_sibling_lists),
            _ValidationStep(check=_check_mixed_dict_values),
            _ValidationStep(check=_check_mixed_list_values),
        ]
    )

    return steps


@beartype
def validate_homogeneous_sequence_data(*, data: Value, spec: Language) -> None:
    """Raise if *data* violates constraints for non-heterogeneous
    sequence formats.
    """
    if spec.sequence_format_config.supports_heterogeneity:
        return
    for step in _build_validation_steps(spec=spec):
        step.check(data=data)
