"""Checks that raise when data is incompatible with a language's
collection-shape constraints.
"""

import copy
import datetime
import math
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, overload

from beartype import beartype

from literalizer._formatters.type_inference import infer_element_type
from literalizer._language import Language
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    ExcessiveNestingError,
    HeterogeneousCollectionError,
    HeterogeneousScalarCollectionError,
    HeterogeneousSetError,
    HeterogeneousSiblingListsError,
    HeterogeneousSiblingMapsError,
    LiteralizerError,
    MixedDictKeysError,
    MixedDictShapesError,
    MixedDictValuesError,
    MixedListValuesError,
    TargetScalarCollisionError,
    UnrepresentableInputError,
    UnrepresentableNullError,
    UnrepresentableStringError,
)

if TYPE_CHECKING:
    from literalizer._formatters.type_inference import RecordShape

_C0_UPPER_BOUND = 0x20


def _format_scalar_identity(*, value: Scalar, spec: Language) -> str:
    """Return the target expression that determines scalar identity."""
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
        # No supported input syntax can put a time-only value in a mapping
        # key or set, the only positions whose scalar identities are checked.
        case datetime.time():  # pragma: no cover
            result = spec.format_time(value)
        case _:
            result = spec.format_date(value)
    return result


def _check_scalar_collection_identity(
    *, values: Iterable[Scalar], spec: Language
) -> None:
    """Reject a collision within one scalar-keyed collection."""
    rendered_values: dict[str, Scalar] = {}
    for value in values:
        rendered = _format_scalar_identity(value=value, spec=spec)
        if rendered in rendered_values:
            raise TargetScalarCollisionError(
                language_name=type(spec).__name__,
                first=rendered_values[rendered],
                second=value,
                rendered=rendered,
            )
        rendered_values[rendered] = value


def _check_scalar_identity_collisions(*, data: Value, spec: Language) -> None:
    """Reject distinct set members or mapping keys rendered
    identically.
    """
    match data:
        case dict():
            _check_scalar_collection_identity(values=data.keys(), spec=spec)
            for value in data.values():
                _check_scalar_identity_collisions(data=value, spec=spec)
        case set():
            _check_scalar_collection_identity(values=data, spec=spec)
        case list():
            for value in data:
                _check_scalar_identity_collisions(data=value, spec=spec)
        case _:
            return


def _check_raw_control_characters(*, data: Value, spec: Language) -> None:
    """Reject strings whose selected formatter emits a raw C0 byte."""
    match data:
        case str():
            candidates = tuple(
                character
                for character in data
                if ord(character) < _C0_UPPER_BOUND
                and character not in "\0\t\n\r"
            )
            if not candidates:
                return
            formatted = spec.format_string(data)
            unsafe_control = next(
                (
                    character
                    for character in candidates
                    if character in formatted
                ),
                None,
            )
            if unsafe_control is not None:
                raise UnrepresentableStringError(
                    language_name=type(spec).__name__,
                    character_name=(
                        f"U+{ord(unsafe_control):04X} control character"
                    ),
                )
        case dict():
            for key, value in data.items():
                # These back ends either reject control-bearing keys via
                # a dedicated contract or derive a safe identifier without
                # rendering the string key itself.
                if not spec.checks_raw_control_dict_keys_separately:
                    _check_raw_control_characters(data=key, spec=spec)
                _check_raw_control_characters(data=value, spec=spec)
        case list() | set():
            for value in data:
                _check_raw_control_characters(data=value, spec=spec)
        case _:
            return


@beartype
def guard_collection_nesting_depth(
    *, data: Value, language_name: str, maximum_depth: int
) -> None:
    """Raise before rendering a collection deeper than *maximum_depth*."""
    pending: list[tuple[Value, int]] = [(data, 0)]
    while pending:
        value, parent_depth = pending.pop()
        if not isinstance(value, dict | list | set):
            continue
        depth = parent_depth + 1
        if depth > maximum_depth:
            raise ExcessiveNestingError(
                language_name=language_name,
                maximum_depth=maximum_depth,
                actual_depth=depth,
            )
        children = value.values() if isinstance(value, dict) else value
        pending.extend((child, depth) for child in children)


@beartype
def _sequence_shape(value: Value, /) -> tuple[object, ...] | None:
    """Return the nested lengths a sequence's type is built from.

    A fixed-size type spells a length at every level it nests, so two
    sequences share a type only where their whole shapes agree, not
    only their outer lengths (issue #4728).  Anything that is not a
    sequence has no shape of its own to compare.
    """
    if not isinstance(value, list):
        return None
    return (len(value), tuple(_sequence_shape(item) for item in value))


@beartype
def _reject_ragged_siblings(
    *,
    siblings: list[Value],
    language_name: str,
) -> None:
    """Reject sequences beside each other that cannot share one type."""
    lengths = {len(item) for item in siblings if isinstance(item, list)}
    if len(lengths) > 1:
        sizes = ", ".join(str(object=length) for length in sorted(lengths))
        msg = (
            f"{language_name} renders a sequence as a fixed-size "
            "array, whose length is part of its type, so sibling "
            f"sequences of lengths {sizes} have no common type"
        )
        raise UnrepresentableInputError(msg)
    shapes = {
        _sequence_shape(item) for item in siblings if isinstance(item, list)
    }
    if len(shapes) > 1:
        msg = (
            f"{language_name} renders a sequence as a fixed-size array, "
            "whose length is part of its type at every level it nests, "
            "so sibling sequences of the same outer length whose nested "
            "sequences differ in length have no common type"
        )
        raise UnrepresentableInputError(msg)


@beartype
def reject_ragged_nested_sequences(
    *,
    data: Value,
    language_name: str,
    record_fields_are_independent: bool,
    list_elements_are_independent: bool,
) -> None:
    """Reject sibling lists of unequal length beside each other.

    A fixed-size array literal carries its length in its type, so two
    sibling arrays of different lengths have no common type and the
    generated file does not compile (issue #3924).

    *list_elements_are_independent* says the enclosing list is itself
    written as a tuple, whose element types stand apart, so siblings
    inside one need no common type; a mapping value slot still takes
    one type however its siblings are written (issue #4663).
    """
    match data:
        case dict():
            is_record = (
                bool(data)
                and not isinstance(data, OrderedMap)
                and all(isinstance(key, str) for key in data)
            )
            if not (record_fields_are_independent and is_record):
                _reject_ragged_siblings(
                    siblings=list(data.values()),
                    language_name=language_name,
                )
            for value in data.values():
                reject_ragged_nested_sequences(
                    data=value,
                    language_name=language_name,
                    record_fields_are_independent=(
                        record_fields_are_independent
                    ),
                    list_elements_are_independent=(
                        list_elements_are_independent
                    ),
                )
        case list():
            if not list_elements_are_independent:
                _reject_ragged_siblings(
                    siblings=data,
                    language_name=language_name,
                )
            for item in data:
                reject_ragged_nested_sequences(
                    data=item,
                    language_name=language_name,
                    record_fields_are_independent=(
                        record_fields_are_independent
                    ),
                    list_elements_are_independent=(
                        list_elements_are_independent
                    ),
                )
        case _:
            return


@beartype
def reject_aware_datetimes(
    *, data: Value, language_name: str, allow_utc_offset: bool
) -> None:
    """Reject timezone-aware datetimes that a native formatter would
    lose.
    """
    stack = [data]
    while stack:
        value = stack.pop()
        match value:
            case datetime.datetime() if value.utcoffset() is not None and not (
                allow_utc_offset and value.utcoffset() == datetime.timedelta()
            ):
                msg = (
                    f"{language_name} native datetime format cannot preserve "
                    f"UTC offset {value.utcoffset()}"
                )
                raise UnrepresentableInputError(msg)
            case dict():
                stack.extend(value.keys())
                stack.extend(value.values())
            case list() | set():
                stack.extend(value)
            case _:
                continue


_CJSON_EXACT_INTEGER_LIMIT = 2**53
"""The widest integer a cJSON number holds exactly.

A cJSON number is a C ``double``, so an integer past this is stored as
the nearest representable value.
"""

_CJSON_PRINT_PRECISION = 15
"""Significant digits the cJSON printer writes a number with."""


@beartype
def reject_cjson_unrepresentable(*, data: Value, language_name: str) -> None:
    """Reject values the cJSON representation silently changes.

    cJSON stores every number as a C ``double`` and prints it to 15
    significant digits, and its strings end at the first null byte, so
    each of those inputs comes back as something else (issues #4469,
    #4512 and #4539).

    Every value of the document passes through here, so the test and
    the descent share one walk rather than calling out per value.
    """
    stack = [data]
    while stack:
        value = stack.pop()
        match value:
            case bool():
                continue
            case int() if abs(value) > _CJSON_EXACT_INTEGER_LIMIT:
                reason = (
                    f"integer {value}, which a cJSON number stores as a "
                    "double and cannot hold exactly"
                )
            case float() if not math.isinf(value) and math.isinf(
                float(f"{value:.{_CJSON_PRINT_PRECISION}g}")
            ):
                reason = (
                    f"float {value!r}, which cJSON prints rounded to "
                    f"{_CJSON_PRINT_PRECISION} significant digits and so "
                    "out of range, reading back as infinity"
                )
            case str() if "\x00" in value:
                reason = (
                    "a string with an embedded null, which cJSON truncates at"
                )
            case dict():
                stack.extend(value.keys())
                stack.extend(value.values())
                continue
            case list() | set():
                stack.extend(value)
                continue
            case _:
                continue
        msg = f"{language_name} json_type=CJSON cannot represent {reason}"
        raise UnrepresentableInputError(msg)


@beartype
def reject_negative_zero(*, data: Value, language_name: str) -> None:
    """Reject negative zero a target cannot keep the sign of.

    Some JSON value types have no signed zero at all: Haskell's
    ``Data.Aeson`` stores ``-0.0`` as ``Number 0.0`` before anything
    is encoded, and ``JSON.stringify`` writes ``0`` for ``-0``.  The
    sign is lost wherever the value goes next, so it is refused
    rather than silently dropped (issue #4543).
    """
    stack = [data]
    while stack:
        value = stack.pop()
        match value:
            case float() if value == 0.0 and math.copysign(1.0, value) < 0:
                msg = (
                    f"{language_name} cannot represent negative zero: its "
                    "JSON value type has no signed zero"
                )
                raise UnrepresentableInputError(msg)
            case dict():
                stack.extend(value.keys())
                stack.extend(value.values())
            case list() | set():
                stack.extend(value)
            case _:
                continue


@beartype
def reject_non_nfc_strings(*, data: Value, language_name: str) -> None:
    """Reject strings a target normalizes on the way back out.

    HCL normalizes source to NFC by specification, and a Raku string
    is normalized by definition, so a value written with a combining
    mark comes back as the single character it composes to, however
    the literal is spelled.  No escape avoids that, so the value is
    refused rather than silently altered (issue #4522).
    """
    stack = [data]
    while stack:
        value = stack.pop()
        match value:
            case str() if not unicodedata.is_normalized("NFC", value):
                raise UnrepresentableStringError(
                    language_name=language_name,
                    character_name=(
                        f"the combining marks in {value!r}, which it "
                        "normalizes to NFC form"
                    ),
                )
            case dict():
                stack.extend(value.keys())
                stack.extend(value.values())
            case list() | set():
                stack.extend(value)
            case _:
                continue


@beartype
def _reject_unpreserved_aware_times(*, data: Value, spec: Language) -> None:
    """Reject aware times when the selected formatter drops the offset."""
    stack = [data]
    while stack:
        value = stack.pop()
        match value:
            case datetime.time() if value.utcoffset() is not None:
                naive = value.replace(tzinfo=None)
                if spec.format_time(value) == spec.format_time(naive):
                    msg = (
                        f"{type(spec).__name__} native time format cannot "
                        f"preserve UTC offset {value.utcoffset()}"
                    )
                    raise UnrepresentableInputError(msg)
            case dict():
                stack.extend(value.keys())
                stack.extend(value.values())
            case list() | set():
                stack.extend(value)
            case _:
                continue


@beartype
def reject_stringified_dict_key_collisions(
    *, data: Value, language_name: str
) -> None:
    """Reject distinct mapping keys that convert to the same string."""
    match data:
        case dict():
            normalized: dict[str, Scalar] = {}
            for key, value in data.items():
                rendered_key = str(object=key)
                previous = normalized.get(rendered_key)
                if rendered_key in normalized and type(previous) is not type(
                    key
                ):
                    msg = (
                        f"{language_name} stringifies distinct dict keys "
                        f"{previous!r} and {key!r} as {rendered_key!r}"
                    )
                    raise MixedDictKeysError(msg)
                normalized[rendered_key] = key
                reject_stringified_dict_key_collisions(
                    data=value,
                    language_name=language_name,
                )
        case list() | set():
            for value in data:
                reject_stringified_dict_key_collisions(
                    data=value,
                    language_name=language_name,
                )
        case _:
            return


def reject_null_dict_keys(*, data: Value, language_name: str) -> None:
    """Reject a null mapping key in a language whose keys are strings.

    Such a language has no null key: the key is converted to text, so
    ``None`` silently becomes an ordinary string key that no longer
    means null (issue #4544).
    """
    match data:
        case dict():
            for key, value in data.items():
                if key is None:
                    raise UnrepresentableNullError(
                        language_name=language_name,
                        conflated_value="the string form of that key",
                    )
                reject_null_dict_keys(data=value, language_name=language_name)
        case list() | set():
            for value in data:
                reject_null_dict_keys(data=value, language_name=language_name)
        case _:
            return


def _contains_set(data: Value, /) -> bool:
    """Return whether *data* contains a set at any depth."""
    match data:
        case set():
            return True
        case dict():
            return any(
                _contains_set(key) or _contains_set(value)
                for key, value in data.items()
            )
        case list():
            return any(_contains_set(value) for value in data)
        case _:
            return False


@overload
def scalar_type_bucket(*, value: Scalar) -> type: ...


@overload
def scalar_type_bucket(*, value: Value) -> type | None: ...


@beartype
def scalar_type_bucket(*, value: Value) -> type | None:
    """Return the type bucket for a scalar, or ``None`` for
    collections.

    Every :data:`Scalar` has a bucket, so callers that have already
    excluded collections get a plain ``type`` back.
    """
    # Check bool before int (bool is a subclass of int), and
    # datetime before date (datetime is a subclass of date).
    bucket_types = (
        type(None),
        bool,
        int,
        float,
        str,
        bytes,
        datetime.datetime,
        datetime.date,
        datetime.time,
    )
    return next(
        (bucket for bucket in bucket_types if isinstance(value, bucket)),
        None,
    )


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
def _value_type_family(  # noqa: C901, PLR0911, PLR0912
    *,
    value: Value,
) -> str:
    # pylint: disable=too-complex,too-many-branches
    """Return a broad type family label for a value."""
    # Check bool before int (bool is a subclass of int), datetime
    # before date (datetime is a subclass of date), and OrderedMap
    # before dict (OrderedMap is a subclass of dict).
    match value:
        case None:
            return "none"
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
        case datetime.date():
            return "date"
        case datetime.time():
            return "time"
        case list():
            return "list"
        case OrderedMap():
            return "dict"
        case dict():
            return "dict"
        case _:
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
def _list_nesting_depths(*, value: list[Value]) -> frozenset[int]:
    """Return the nesting depths a list value is known to have.

    An empty list carries no information about what it holds, so it
    contributes no depth and stays compatible with any sibling
    (issue #3933).

    Each element is measured on its own.  A non-list element puts the
    list at depth 1, and a list element puts it one deeper than that
    element reports -- or at depth 2 when the element is empty, since an
    empty list is still a list.  Folding the elements together first
    would lose that: a list holding only empty lists reports nothing to
    add to, and would read as a list of scalars.
    """
    depths: set[int] = set()
    for item in value:
        if isinstance(item, list):
            inner = _list_nesting_depths(value=item)
            depths |= {depth + 1 for depth in inner} or {2}
        else:
            depths.add(1)
    return frozenset(depths)


@beartype
def _values_mixed_list_depths(*, values: Sequence[Value]) -> bool:
    """Check whether sibling list values nest to different depths.

    A map with one value type cannot hold a list of scalars beside a
    list of lists, and the two share no element type either, so the
    shape is refused rather than rendered (issue #3933).
    """
    lists = [value for value in values if isinstance(value, list)]
    if len(lists) <= 1:
        return False
    depth_shapes = {
        depths
        for value in lists
        if (depths := _list_nesting_depths(value=value))
    }
    return len(depth_shapes) > 1


@beartype
def _collect_scalar_type_names(*, data: Value) -> set[str]:
    """Collect the names of scalar type buckets found in *data*."""
    names: set[str] = set()
    match data:
        case dict():
            for v in data.values():
                names |= _collect_scalar_type_names(data=v)
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
        case dict():
            children = list(data.values())
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
def _has_heterogeneous(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any heterogeneous
    all-scalar collections.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.  Lists
    whose ``id`` is in *tuple_list_ids* are skipped — they are carved
    out by the active TUPLE heterogeneous strategy, which renders them
    as a fixed-size tuple rather than a homogeneous sequence.
    """
    match data:
        case dict():
            children: list[Value] = list(data.values())
            own_mixed = id(
                data
            ) not in record_dict_ids and _all_scalars_heterogeneous(
                values=children
            )
        case list():
            children = data
            own_mixed = id(
                data
            ) not in tuple_list_ids and _all_scalars_heterogeneous(
                values=children
            )
        case set():
            return _all_scalars_heterogeneous(values=list(data))
        case _:
            return False

    return own_mixed or any(
        _has_heterogeneous(
            data=v,
            record_dict_ids=record_dict_ids,
            tuple_list_ids=tuple_list_ids,
        )
        for v in children
    )


@beartype
def _has_heterogeneous_sibling_lists(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains sibling lists whose
    combined scalar elements are heterogeneous.

    Sibling lists are detected both as the direct children of a list
    and as the values of a dict.

    Lists whose ``id`` is in *tuple_list_ids* are carved out by the
    active TUPLE heterogeneous strategy: each is rendered as its own
    fixed-size tuple type rather than the sequence type shared by the
    remaining sibling lists, so its elements do not join the shared
    element pool and it does not count as a sibling sequence.  Such a
    list still counts as a list value for the "all values are lists"
    gate, so a genuine heterogeneous pair of sibling sequences beside a
    tuple-eligible list is still rejected.
    """
    match data:
        case dict():
            values = list(data.values())
            if any(
                _has_heterogeneous_sibling_lists(
                    data=v,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in values
            ):
                return True
            all_lists: list[list[Value]] = [
                v for v in values if isinstance(v, list)
            ]
            seq_lists = [v for v in all_lists if id(v) not in tuple_list_ids]
            return (
                len(all_lists) == len(values)
                and len(seq_lists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in seq_lists for e in sub],
                )
            )
        case list():
            if any(
                _has_heterogeneous_sibling_lists(
                    data=v,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in data
            ):
                return True
            all_list_children: list[list[Value]] = [
                v for v in data if isinstance(v, list)
            ]
            seq_list_children = [
                v for v in all_list_children if id(v) not in tuple_list_ids
            ]
            return (
                len(all_list_children) == len(data)
                and len(seq_list_children) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in seq_list_children for e in sub],
                )
            )
        case _:
            return False


@beartype
def _has_empty_sibling_sequence(*, data: Value) -> bool:
    """Return whether sibling sequences mix empty and non-empty values."""
    match data:
        case dict():
            children: list[Value] = list(data.values())
        case list():
            children = data
        case _:
            return False

    sibling_sequences = [
        value for value in children if isinstance(value, list)
    ]
    if (
        len(sibling_sequences) == len(children)
        and any(sibling_sequences)
        and any(not value for value in sibling_sequences)
    ):
        return True
    return any(_has_empty_sibling_sequence(data=value) for value in children)


@beartype
def _has_mixed_dict_shapes(*, data: Value) -> bool:
    """Recursively check whether data contains any list of dicts
    with different key sets.
    """
    match data:
        case dict():
            return any(_has_mixed_dict_shapes(data=v) for v in data.values())
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


def _has_mixed_record_shapes(
    *,
    data: Value,
    shapes_by_id: "Mapping[int, RecordShape]",
) -> bool:
    """Recursively check whether sibling dicts in *data* resolve to
    different :class:`RecordShape` values.

    Record-eligible dicts compare equal when their entry in
    *shapes_by_id* matches, so shapes that have been unified by the
    strategy are treated as compatible siblings.  Non-record-eligible
    dicts (e.g. ordered maps, empty dicts, dicts with non-string keys)
    are compared by raw key set as a conservative fallback.
    """
    match data:
        case dict():
            return any(
                _has_mixed_record_shapes(data=v, shapes_by_id=shapes_by_id)
                for v in data.values()
            )
        case list():
            dicts_in_list = [v for v in data if isinstance(v, dict)]
            signatures: set[object] = {
                shapes_by_id.get(id(d), frozenset(d.keys()))
                for d in dicts_in_list
            }
            if len(signatures) > 1:
                return True
            return any(
                _has_mixed_record_shapes(data=v, shapes_by_id=shapes_by_id)
                for v in data
            )
        case _:
            return False


@beartype
def _has_mixed_dict_keys(*, data: Value) -> bool:
    """Recursively check whether data contains any dict whose keys span
    multiple type families.
    """
    match data:
        case dict():
            keys: list[Value] = list(data.keys())
            if _values_mixed_types(values=keys):
                return True
            return any(_has_mixed_dict_keys(data=v) for v in data.values())
        case list():
            return any(_has_mixed_dict_keys(data=v) for v in data)
        case _:
            return False


@beartype
def _find_first_mixed_keys(*, data: Value) -> Sequence[Value]:
    """Return the keys of the first dict in *data* whose keys span
    multiple type families.
    """
    children: Sequence[Value]
    match data:
        case dict():
            keys: list[Value] = list(data.keys())
            if _values_mixed_types(values=keys):
                return keys
            children = list(data.values())
        case list():
            children = data
        case _:
            return []
    for child in children:
        result = _find_first_mixed_keys(data=child)
        if result:
            return result
    return []


@beartype
def _has_mixed_dict_values(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.  A value
    whose ``id`` is in *tuple_list_ids* is excluded from the
    type-family span of its parent dict: the TUPLE strategy renders
    that heterogeneous array as a single fixed-size tuple field, so it
    does not force the surrounding map to a heterogeneous value type.
    """
    match data:
        case dict():
            values: list[Value] = list(data.values())
            considered = [v for v in values if id(v) not in tuple_list_ids]
            if id(data) not in record_dict_ids and _values_mixed_types(
                values=considered
            ):
                return True
            return any(
                _has_mixed_dict_values(
                    data=v,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in values
            )
        case list():
            return any(
                _has_mixed_dict_values(
                    data=v,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in data
            )
        case _:
            return False


@beartype
def _has_dict_with_unwrappable_value_mix(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families and at least one value is a container.

    Wrapping strategies that only wrap scalars (tagged-enum / variant
    payload with no list/dict member) cannot uniformly type such a
    dict — scalar values would render wrapped while container values
    stay raw, and any two distinct non-scalar families (e.g. ``dict``
    and ``list``) cannot share a single map value type even after the
    wrapping.  The static-typed target rejects the resulting
    heterogeneous map.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.
    """
    match data:
        case dict():
            values: list[Value] = list(data.values())
            has_container = any(
                isinstance(v, (list, dict, set)) for v in values
            )
            if (
                id(data) not in record_dict_ids
                and has_container
                and _values_mixed_types(values=values)
            ):
                return True
            return any(
                _has_dict_with_unwrappable_value_mix(
                    data=v,
                    record_dict_ids=record_dict_ids,
                )
                for v in values
            )
        case list():
            return any(
                _has_dict_with_unwrappable_value_mix(
                    data=v,
                    record_dict_ids=record_dict_ids,
                )
                for v in data
            )
        case _:
            return False


@beartype
def _has_mixed_list_values(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any list whose elements span
    multiple type families.

    Lists whose ``id`` is in *tuple_list_ids* are skipped — they are
    carved out by the active TUPLE heterogeneous strategy, which
    renders them as a fixed-size tuple whose positions may differ in
    type.
    """
    match data:
        case dict():
            return any(
                _has_mixed_list_values(data=v, tuple_list_ids=tuple_list_ids)
                for v in data.values()
            )
        case list():
            if id(data) not in tuple_list_ids and _values_mixed_types(
                values=data
            ):
                return True
            return any(
                _has_mixed_list_values(data=v, tuple_list_ids=tuple_list_ids)
                for v in data
            )
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
        case dict():
            return any(_has_heterogeneous_set(data=v) for v in data.values())
        case list():
            return any(_has_heterogeneous_set(data=v) for v in data)
        case _:
            return False


@beartype
def _check_heterogeneous(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if data contains heterogeneous all-scalar collections."""
    if _has_heterogeneous(
        data=data,
        record_dict_ids=record_dict_ids,
        tuple_list_ids=tuple_list_ids,
    ):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Collection contains heterogeneous scalar types that cannot "
            "be represented in the target language "
            f"(found types: {types})"
        )
        raise HeterogeneousScalarCollectionError(msg)


@beartype
def _check_heterogeneous_sibling_lists(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if sibling lists have heterogeneous scalar types."""
    if _has_heterogeneous_sibling_lists(
        data=data,
        tuple_list_ids=tuple_list_ids,
    ):
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
def _check_mixed_dict_keys(*, data: Value) -> None:
    """Raise if any dict has keys spanning multiple type families."""
    if _has_mixed_dict_keys(data=data):
        keys = _find_first_mixed_keys(data=data)
        types = ", ".join(
            sorted({_value_type_family(value=k) for k in keys}),
        )
        msg = (
            "Dict contains keys of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedDictKeysError(msg)


@beartype
def _check_mixed_dict_values(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if any dict has values spanning multiple type families."""
    if _has_mixed_dict_values(
        data=data,
        record_dict_ids=record_dict_ids,
        tuple_list_ids=tuple_list_ids,
    ):
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
def _has_mixed_dict_list_depths(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
) -> bool:
    """Return whether one dict has list values of differing depth."""
    match data:
        case dict():
            values: list[Value] = list(data.values())
            if id(data) not in record_dict_ids and _values_mixed_list_depths(
                values=values
            ):
                return True
            return any(
                _has_mixed_dict_list_depths(
                    data=value,
                    record_dict_ids=record_dict_ids,
                )
                for value in values
            )
        case list():
            return any(
                _has_mixed_dict_list_depths(
                    data=item,
                    record_dict_ids=record_dict_ids,
                )
                for item in data
            )
        case _:
            return False


@beartype
def _check_mixed_dict_list_depths(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
) -> None:
    """Raise if one dict has list values of differing depth."""
    if _has_mixed_dict_list_depths(
        data=data,
        record_dict_ids=record_dict_ids,
    ):
        msg = (
            "Dict contains list values nesting to different depths, "
            "which cannot share one map value type in the target "
            "language"
        )
        raise MixedDictValuesError(msg)


@beartype
def _check_mixed_list_values(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if any list has elements spanning multiple type families."""
    if _has_mixed_list_values(data=data, tuple_list_ids=tuple_list_ids):
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


# Two dicts whose values mix disjoint scalar types, used to probe whether
# a language's dict opener collapses mixed values to a stable
# "accepts anything" fallback or builds a content-specific type.  When
# the two openers differ the language uses variant/union typing (e.g.
# C++'s ``std::variant``) with no single value type that every sibling
# map converts to, so divergent sibling maps cannot be widened and must
# be rejected.  Both probes are non-empty and string-keyed so no
# language's opener depends on an empty-dict opener (which some
# strategies, e.g. D's ``RECORD``, reject).  Mirrors
# :data:`literalizer._literalize._DICT_FALLBACK_PROBE_A` / ``_B``.
_MIXED_VALUE_PROBE_A: dict[Scalar, Value] = {"_probe_a": 1, "_probe_b": "s"}
_MIXED_VALUE_PROBE_B: dict[Scalar, Value] = {
    "_probe_a": 1.5,
    "_probe_b": False,
}


@beartype
def _dict_slot_uses_variant_typing(*, spec: Language) -> bool:
    """Return whether *spec*'s dict opener builds a content-specific
    value type with no single type accepting every sibling map.

    True only for languages whose opener derives the value type from the
    values (variant/union typing, e.g. C++), so two dicts with different
    value content yield different openers; those have no "accepts
    anything" value type to widen a narrower sibling map into.  False for
    languages with a stable fallback (Go's ``map[string]any``, Kotlin's
    ``Any?``) and for dynamic languages whose opener ignores the values.

    A language whose opener rejects a heterogeneous-valued dict outright
    (e.g. D's narrow-typed mode) already raises on the real data through
    its own path, so the probe failure maps to ``False`` here.
    """
    dict_open = spec.dict_format_config.dict_open
    try:
        return dict_open(_MIXED_VALUE_PROBE_A) != dict_open(
            _MIXED_VALUE_PROBE_B
        )
    except (UnrepresentableInputError, HeterogeneousCollectionError):
        return False


@beartype
def _plain_maps(*, values: Iterable[Value]) -> list[dict[Scalar, Value]]:
    """Return unordered plain maps from *values*."""
    return [
        value
        for value in values
        if isinstance(value, dict) and not isinstance(value, OrderedMap)
    ]


@beartype
def _fill_nested_empty_map_siblings(
    *, maps: list[dict[Scalar, Value]]
) -> None:
    """Give nested empty maps a non-empty cousin's inferred shape."""
    keys = {key for sibling in maps for key in sibling}
    for key in keys:
        owners = [sibling for sibling in maps if key in sibling]
        cousins = [owner[key] for owner in owners]
        cousin_maps = _plain_maps(values=cousins)
        if cousins and len(cousin_maps) == len(cousins):
            replacement = next((cousin for cousin in cousins if cousin), None)
            if replacement is not None:
                for owner in owners:
                    if owner[key] == {}:
                        owner[key] = copy.deepcopy(x=replacement)
            nested_maps = _plain_maps(values=(owner[key] for owner in owners))
            _fill_nested_empty_map_siblings(
                maps=nested_maps,
            )
            continue
        for cousin in cousins:
            if isinstance(cousin, list):
                nested_maps = _plain_maps(values=cousin)
                if nested_maps:
                    _fill_nested_empty_map_siblings(maps=nested_maps)


@beartype
def _sibling_maps_diverge(
    *,
    pool: list[Value],
    spec: Language,
    record_dict_ids: frozenset[int],
) -> bool:
    """Return whether two or more maps sharing one declared value slot
    infer different dict openers.

    *pool* are the sibling values occupying a single declared value slot.
    Dicts rendered as records (``record_dict_ids``) are excluded because
    they render as their own struct type rather than a shared map slot.
    When the remaining maps' openers disagree, the enclosing container
    declares a widened map slot that the narrower inner maps do not fit.
    """
    dict_open = spec.dict_format_config.dict_open
    maps: list[dict[Scalar, Value]] = [
        item
        for item in pool
        if isinstance(item, dict)
        and not isinstance(item, OrderedMap)
        and id(item) not in record_dict_ids
    ]
    min_maps_for_divergence = 2
    if len(maps) < min_maps_for_divergence:
        return False
    filtered = copy.deepcopy(
        x=[
            {
                k: v
                for k, v in d.items()
                if not (spec.skip_null_dict_values and v is None)
            }
            for d in maps
        ]
    )
    if not spec.dict_supports_heterogeneous_values:
        if spec.dict_format_config.narrowed_empty_form is not None:
            _fill_nested_empty_map_siblings(maps=filtered)
        inferred_value_types = {
            infer_element_type(items=list(d.values())) for d in filtered if d
        }
        if len(inferred_value_types) > 1:
            return True
    return len({dict_open(d) for d in filtered}) > 1


@beartype
def _has_unrepresentable_sibling_maps(
    *,
    data: Value,
    spec: Language,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Return whether *data* holds sibling maps whose value types force a
    widened dict slot *spec* cannot represent.

    Walks *data* pooling sibling map values exactly as
    :func:`~literalizer._formatters.type_inference.infer_element_type`
    derives a container's declared type: a plain dict pools its own
    values, and a list of two or more plain dicts pools every element's
    values into one shared slot.  A pool whose maps disagree on their
    opener (see :func:`_sibling_maps_diverge`) declares a widened slot
    the language cannot represent.
    """
    match data:
        case OrderedMap():
            return any(
                _has_unrepresentable_sibling_maps(
                    data=value,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for value in data.values()
            )
        case dict():
            if _dict_slot_uses_variant_typing(
                spec=spec
            ) and _sibling_maps_diverge(
                pool=list(data.values()),
                spec=spec,
                record_dict_ids=record_dict_ids,
            ):
                return True
            return any(
                _has_unrepresentable_sibling_maps(
                    data=value,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for value in data.values()
            )
        case list():
            min_dicts_for_pooling = 2
            plain_dicts = [
                item
                for item in data
                if isinstance(item, dict) and not isinstance(item, OrderedMap)
            ]
            if (
                id(data) not in tuple_list_ids
                and len(plain_dicts) == len(data) >= min_dicts_for_pooling
                and _sibling_maps_diverge(
                    pool=(
                        [
                            value
                            for element in plain_dicts
                            for value in element.values()
                        ]
                        if spec.dict_supports_heterogeneous_values
                        else list(data)
                    ),
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                )
            ):
                return True
            return any(
                _has_unrepresentable_sibling_maps(
                    data=item,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for item in data
            )
        case _:
            return False


@beartype
def _check_unrepresentable_sibling_maps(
    *,
    data: Value,
    spec: Language,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if *data* holds sibling maps whose widened dict slot *spec*
    cannot represent.

    *record_dict_ids* also includes maps whose selected strategy wraps
    every scalar child into one shared value carrier; those maps no
    longer rely on their content-specific normal opener and are equally
    safe to exclude from the divergence probe.
    """
    typed_sibling_maps = (
        not spec.dict_supports_heterogeneous_values
        and not spec.heterogeneous_behavior.skip_scalar_checks
    ) or _dict_slot_uses_variant_typing(spec=spec)
    if typed_sibling_maps and (
        _has_unrepresentable_sibling_maps(
            data=data,
            spec=spec,
            record_dict_ids=record_dict_ids,
            tuple_list_ids=tuple_list_ids,
        )
    ):
        msg = (
            "Container holds sibling maps whose value types force a "
            "widened dict slot that the target language cannot "
            "represent"
        )
        raise HeterogeneousSiblingMapsError(msg)


@beartype
def check_empty_sibling_sequence_type_hint_data(
    *,
    data: Value,
    language_name: str,
    supports_empty_sibling_sequence_type_hints: bool,
) -> None:
    """Raise when an explicit hint cannot represent sibling sequences."""
    if (
        not supports_empty_sibling_sequence_type_hints
        and _has_empty_sibling_sequence(data=data)
    ):
        msg = (
            f"{language_name} cannot represent explicit type hints "
            "for sibling sequences that mix empty and non-empty values"
        )
        raise UnrepresentableInputError(msg)


@beartype
def _check_data(  # noqa: C901  # pylint: disable=too-complex
    *,
    data: Value,
    spec: Language,
) -> None:
    """Check that *data* fits the language's collection-shape
    constraints.

    Raises a subclass of
    :exc:`~literalizer.exceptions.HeterogeneousCollectionError` when the
    data cannot be represented in the target language's collection
    formats.
    """
    _check_raw_control_characters(data=data, spec=spec)
    _reject_unpreserved_aware_times(data=data, spec=spec)
    _check_scalar_identity_collisions(data=data, spec=spec)
    if not spec.set_format_config.preserves_set_semantics and _contains_set(
        data
    ):
        msg = (
            f"{type(spec).__name__} cannot preserve native set semantics "
            "with the selected set format"
        )
        raise UnrepresentableInputError(msg)
    if spec.sequence_format_config.requires_uniform_record_shapes:
        _check_mixed_dict_shapes(data=data)

    seq_supports_het = spec.sequence_format_config.supports_heterogeneity
    dict_supports_het = spec.dict_supports_heterogeneous_values
    set_supports_het = spec.set_format_config.supports_heterogeneity
    behavior = spec.heterogeneous_behavior
    # Validate tuple arity before record-shape refinement asks the
    # tuple-aware field-type hook to derive a native tuple type.  In
    # particular, Kotlin only has Pair and Triple, and its hook cannot
    # type an otherwise eligible four-element tuple.
    compute_tuple_list_ids = behavior.compute_tuple_list_ids
    tuple_list_ids: frozenset[int] = (
        compute_tuple_list_ids(data)
        if compute_tuple_list_ids is not None
        else frozenset()
    )
    compute_record_shapes = behavior.compute_record_shapes
    record_shapes_by_id: Mapping[int, RecordShape] = (
        compute_record_shapes(data)
        if compute_record_shapes is not None
        else {}
    )
    record_dict_ids: frozenset[int] = frozenset(record_shapes_by_id)
    _check_unrepresentable_sibling_maps(
        data=data,
        spec=spec,
        record_dict_ids=(record_dict_ids | behavior.compute_wrap_ids(data)),
        tuple_list_ids=tuple_list_ids,
    )
    if behavior.render_record_literal is not None and _has_mixed_record_shapes(
        data=data,
        shapes_by_id=record_shapes_by_id,
    ):
        msg = (
            "Sibling list contains dicts with different record shapes; "
            "the RECORD heterogeneous strategy cannot represent a "
            "heterogeneous sequence of record shapes"
        )
        raise HeterogeneousSiblingListsError(msg)
    if not dict_supports_het:
        _check_mixed_dict_keys(data=data)
    if not behavior.skip_scalar_checks:
        # A scalar-wrapping or top-type-widening strategy (RECORD
        # widening a nested sibling map to a plain map, issue #2910)
        # makes the scalar children of each marked container
        # representable by one declared value type, so those containers
        # are exempt from the scalar-family checks -- the same carve-out
        # ``record_dict_ids`` grants.
        wrapped_dict_ids = record_dict_ids | behavior.compute_wrap_ids(data)
        if not seq_supports_het:
            _check_heterogeneous(
                data=data,
                record_dict_ids=wrapped_dict_ids,
                tuple_list_ids=tuple_list_ids,
            )
            _check_heterogeneous_sibling_lists(
                data=data,
                tuple_list_ids=tuple_list_ids,
            )
        if not dict_supports_het:
            _check_mixed_dict_values(
                data=data,
                record_dict_ids=wrapped_dict_ids,
                tuple_list_ids=tuple_list_ids,
            )
            _check_mixed_dict_list_depths(
                data=data,
                record_dict_ids=wrapped_dict_ids,
            )
        if not seq_supports_het:
            _check_mixed_list_values(
                data=data,
                tuple_list_ids=tuple_list_ids,
            )
        if not set_supports_het:
            _check_heterogeneous_set(data=data)
    elif behavior.wrap_non_scalar is None:
        # A wrapping strategy that only wraps scalars cannot uniformly
        # represent a dict whose values span multiple type families and
        # include at least one container — the tagged-enum / variant
        # payload has no member that fits the container, and two
        # distinct non-scalar families share no map value type either.
        if not dict_supports_het and _has_dict_with_unwrappable_value_mix(
            data=data,
            record_dict_ids=record_dict_ids,
        ):
            msg = (
                "Dict has values of mixed type families including a "
                "container, which this heterogeneous strategy cannot "
                "represent"
            )
            raise MixedDictValuesError(msg)


def _path_key(key: Scalar) -> str | int:
    """Return a stable public path component for a mapping key."""
    if isinstance(key, str | int) and not isinstance(key, bool):
        return key
    return repr(key)


def _locate_error(
    *,
    data: Value,
    spec: Language,
    error_type: type[LiteralizerError],
) -> tuple[str | int, ...]:
    """Return the deepest child that independently raises *error_type*."""
    children: list[tuple[str | int, Value]]
    match data:
        case dict():
            children = [
                (_path_key(key=key), value) for key, value in data.items()
            ]
        case list():
            children = list(enumerate(iterable=data))
        case _:
            return ()
    for component, child in children:
        try:
            _check_data(data=child, spec=spec)
        except error_type:
            return (
                component,
                *_locate_error(
                    data=child,
                    spec=spec,
                    error_type=error_type,
                ),
            )
        except LiteralizerError:
            continue
    return ()


@beartype
def check_data(*, data: Value, spec: Language) -> None:
    """Validate data and attach the offending collection's input path."""
    try:
        _check_data(data=data, spec=spec)
    except LiteralizerError as exc:
        if exc.path is None:  # pragma: no branch - entry lacks a location
            exc.path = _locate_error(
                data=data,
                spec=spec,
                error_type=type(exc),
            )
        raise
