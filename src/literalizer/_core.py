"""Core conversion logic: formatting values and parsing JSON/YAML."""

import dataclasses
import datetime
import json
from collections.abc import Sequence
from io import StringIO
from typing import Any, cast

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
from literalizer._language import Language
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    JSONParseError,
    YAMLParseError,
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
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    # datetime.datetime is a subclass of datetime.date, so this
    # single check covers both types.
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, str):
        return value
    return repr(value)


@beartype
def _all_scalars_heterogeneous(
    *,
    values: Sequence[Value],
) -> bool:
    """Check whether values are all scalars with more than one type."""
    buckets: set[type] = set()
    for v in values:
        bucket = _scalar_type_bucket(value=v)
        if bucket is None:
            return False
        buckets.add(bucket)
    return len(buckets) > 1


@beartype
def _coerce_heterogeneous_sibling_lists(*, data: Value) -> Value:
    """Recursively coerce sibling lists with heterogeneous scalar
    element types so that every inner element becomes a string.

    For example, ``[[1, 2], ["a", "b"]]`` becomes
    ``[["1", "2"], ["a", "b"]]``.
    """
    if isinstance(data, (dict, ordereddict)):
        return type(data)(
            {
                k: _coerce_heterogeneous_sibling_lists(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for k, v in data.items()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            }
        )

    if isinstance(data, list):
        new_list = [_coerce_heterogeneous_sibling_lists(data=v) for v in data]
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

    return data


@beartype
def _has_heterogeneous(*, data: Value) -> bool:
    """Recursively check whether data contains any heterogeneous
    all-scalar collections.
    """
    if isinstance(data, (ordereddict, dict)):
        children: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    elif isinstance(data, list):
        children = data
    elif isinstance(data, set):
        return _all_scalars_heterogeneous(values=list(data))
    else:
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
    if isinstance(data, (dict, ordereddict)):
        return any(
            _has_heterogeneous_sibling_lists(data=v)  # pyright: ignore[reportUnknownArgumentType]
            for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
        )

    if isinstance(data, list):
        if any(_has_heterogeneous_sibling_lists(data=v) for v in data):
            return True
        sublists: list[list[Value]] = [v for v in data if isinstance(v, list)]
        if (
            len(sublists) == len(data)
            and len(sublists) > 1
            and _all_scalars_heterogeneous(
                values=[e for sub in sublists for e in sub],
            )
        ):
            return True

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
    if isinstance(data, ordereddict):
        return _coerce_heterogeneous_ordereddict(data=data)
    if isinstance(data, dict):
        return _coerce_heterogeneous_dict(data=data)
    if isinstance(data, set):
        return _coerce_heterogeneous_set(data=data)
    if isinstance(data, list):
        return _coerce_heterogeneous_list(data=data)
    return data


_TYPE_FAMILY_CHECKS: tuple[tuple[type, str], ...] = (
    # Check bool before int (bool is a subclass of int), and
    # datetime before date (datetime is a subclass of date).
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
)


@beartype
def _value_type_family(*, value: Value) -> str:
    """Return a broad type family label for a value.

    Used to decide whether values in a dict are homogeneous enough for
    languages that require a single value type (e.g. Mojo).
    """
    if value is None:
        return "none"
    for check_type, family in _TYPE_FAMILY_CHECKS:
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
    if isinstance(data, ordereddict):
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

    if isinstance(data, dict):
        new_dict: dict[str, Value] = {
            k: _coerce_mixed_dict_values(data=v) for k, v in data.items()
        }
        if _dict_values_mixed_types(values=list(new_dict.values())):
            new_dict = {
                k: _coerce_value_to_str(value=v) for k, v in new_dict.items()
            }
        return new_dict

    if isinstance(data, list):
        return [_coerce_mixed_dict_values(data=v) for v in data]

    return data


@beartype
def _coerce_mixed_list_values(*, data: Value) -> Value:
    """Recursively coerce lists whose elements span multiple type families.

    When a list has elements of mixed types (e.g. scalars and nested
    collections), all elements are converted to strings so the list
    becomes homogeneous.
    """
    if isinstance(data, (ordereddict, dict)):
        if isinstance(data, ordereddict):
            new_ordered_map: ordereddict = ordereddict()
            for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                new_ordered_map[k] = _coerce_mixed_list_values(data=v)  # pyright: ignore[reportUnknownArgumentType]
            return new_ordered_map
        return {k: _coerce_mixed_list_values(data=v) for k, v in data.items()}

    if isinstance(data, list):
        new_list = [_coerce_mixed_list_values(data=v) for v in data]
        if _dict_values_mixed_types(values=new_list):
            return [_coerce_value_to_str(value=v) for v in new_list]
        return new_list

    return data


@beartype
def _format_scalar(*, value: Scalar, spec: Language) -> str:
    """Format a scalar JSON value as a native language literal."""
    if value is None:
        result = spec.null_literal
    elif isinstance(value, bool):
        result = spec.true_literal if value else spec.false_literal
    elif isinstance(value, int):
        result = str(object=value)
    elif isinstance(value, float):
        result = repr(value)
    elif isinstance(value, str):
        result = spec.format_string(value)
    elif isinstance(value, bytes):
        result = spec.format_bytes(value)
    elif isinstance(value, datetime.datetime):
        result = spec.format_datetime(value)
    else:
        result = spec.format_date(value)
    return result


@beartype
def _build_dict_entry(*, key_str: str, val_str: str, spec: Language) -> str:
    """Format a single dict key-value entry using the language spec."""
    return spec.dict_format_config.format_entry(key_str, val_str)


@beartype
def _format_set_value(*, value: set[Scalar], spec: Language) -> str:
    """Format a set value as a native language literal."""
    if not value and spec.set_format_config.empty_set is not None:
        return spec.set_format_config.empty_set
    sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
    formatted = [_format_scalar(value=v, spec=spec) for v in sorted_items]
    entries = [spec.format_set_entry(item) for item in formatted]
    joined = spec.element_separator.join(entries)
    set_cfg = spec.set_format_config
    return set_cfg.open_str + joined + set_cfg.close


@beartype
def _format_ordered_map_value(
    *,
    value: ordereddict,
    spec: Language,
) -> str:
    """Format an ordered map as a native language literal."""
    ordered_map_items: list[tuple[str, Value]] = [
        (k, v)
        for k, v in value.items()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        if not (spec.skip_null_dict_values and v is None)
    ]
    pairs = [
        spec.format_ordered_map_entry(
            _format_value(value=k, spec=spec),
            _format_value(value=v, spec=spec),
        )
        for k, v in ordered_map_items
    ]
    joined = spec.element_separator.join(pairs)
    ordered_map_cfg = spec.ordered_map_format_config
    return ordered_map_cfg.open_str + joined + ordered_map_cfg.close


@beartype
def _format_dict_value(
    *,
    value: dict[str, Value],
    spec: Language,
) -> str:
    """Format a dict as a native language literal."""
    dict_items: dict[str, Value] = {
        k: v
        for k, v in value.items()
        if not (spec.skip_null_dict_values and v is None)
    }
    dict_cfg = spec.dict_format_config
    if not dict_items and dict_cfg.empty_dict is not None:
        return dict_cfg.empty_dict
    pairs = [
        _build_dict_entry(
            key_str=_format_value(value=k, spec=spec),
            val_str=_format_value(value=v, spec=spec),
            spec=spec,
        )
        for k, v in dict_items.items()
    ]
    joined = spec.element_separator.join(pairs)
    return dict_cfg.open_fn(dict_items) + joined + dict_cfg.close


@beartype
def _format_list_value(
    *,
    value: list[Value],
    spec: Language,
) -> str:
    """Format a list as a native language literal."""
    seq_cfg = spec.sequence_format_config
    if not value and seq_cfg.empty_sequence is not None:
        return seq_cfg.empty_sequence
    items = [
        spec.format_sequence_entry(_format_value(value=v, spec=spec))
        for v in value
    ]
    joined = spec.element_separator.join(items)
    # Some languages (e.g. Python) require a trailing comma on
    # single-element sequences to avoid syntactic ambiguity.
    if len(items) == 1 and seq_cfg.single_element_trailing_comma:
        joined += spec.element_separator.strip()
    return f"{spec.sequence_open(value)}{joined}{seq_cfg.close}"


@beartype
def _format_value(
    *,
    value: Value,
    spec: Language,
) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), dicts, and sets.
    """
    if isinstance(value, ordereddict):
        return _format_ordered_map_value(value=value, spec=spec)

    if isinstance(value, dict):
        return _format_dict_value(value=value, spec=spec)

    if isinstance(value, set):
        return _format_set_value(value=value, spec=spec)

    if isinstance(value, list):
        return _format_list_value(value=value, spec=spec)

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
    ci = spec.multiline_close_indent
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
        opening = f"{line_prefix}{spec.set_format_config.open_str}"
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

    ``ordereddict`` (used for YAML ``!!omap`` nodes) is excluded from
    key coercion so that ordered-map detection in :func:`_literalize` is
    preserved.
    """
    if isinstance(data, ordereddict):
        return cast("Value", data)
    if isinstance(data, dict):
        return {
            f"{k}": _coerce_yaml_keys(data=v)
            for k, v in cast("dict[object, object]", data).items()
        }
    if isinstance(data, list):
        return [
            _coerce_yaml_keys(data=item) for item in cast("list[object]", data)
        ]
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
        else:
            data = _coerce_heterogeneous_scalars(data=data)
            data = _coerce_heterogeneous_sibling_lists(data=data)
        data = _coerce_mixed_dict_values(data=data)
        data = _coerce_mixed_list_values(data=data)
    return data


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: Value,
    language: Language,
    line_prefix: str,
    indent: str,
    wrap: bool,
    error_on_coercion: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified indent.

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
        indent: Indentation step for elements inside delimiters when
            *wrap* is ``True`` (e.g. ``"    "`` for 4-space indent).
            Ignored when *wrap* is ``False``.
        wrap: If True, wrap the output in delimiters
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

    body_prefix = line_prefix + indent if wrap else line_prefix
    lines: list[str] = []

    is_ordered_map = isinstance(data, ordereddict)
    if is_ordered_map or isinstance(data, dict):
        dict_data = cast("dict[str, Value]", data)
        entries = [
            (k, v)
            for k, v in dict_data.items()
            if not (spec.skip_null_dict_values and v is None)
        ]
        if not entries and wrap and dict_data:
            empty_value: ordereddict | dict[str, Value] = (
                ordereddict() if is_ordered_map else {}
            )
            return _format_value(value=empty_value, spec=spec)
        last_idx = len(entries) - 1
        for i, (k, v) in enumerate(iterable=entries):
            formatted_key = _format_value(value=k, spec=spec)
            formatted_val = _format_value(value=v, spec=spec)
            entry = (
                spec.format_ordered_map_entry(formatted_key, formatted_val)
                if is_ordered_map
                else _build_dict_entry(
                    key_str=formatted_key, val_str=formatted_val, spec=spec
                )
            )
            add_sep = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator.strip() if add_sep else ""
            lines.append(f"{body_prefix}{entry}{sep}")
    elif isinstance(data, set):
        sorted_items = sorted(data, key=lambda v: (type(v).__name__, repr(v)))
        last_idx = len(sorted_items) - 1
        for i, item in enumerate(iterable=sorted_items):
            formatted = _format_value(value=item, spec=spec)
            entry = spec.format_set_entry(formatted)
            add_sep = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator.strip() if add_sep else ""
            lines.append(f"{body_prefix}{entry}{sep}")
    else:
        # data must be a list (other types handled above)
        items: list[Value] = list(data)
        last_idx = len(items) - 1
        for i, element in enumerate(iterable=items):
            formatted = spec.format_sequence_entry(
                _format_value(value=element, spec=spec)
            )
            add_sep = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator.strip() if add_sep else ""
            lines.append(f"{body_prefix}{formatted}{sep}")

    body = "\n".join(lines)

    if not wrap or not body:
        return body

    return _wrap_body(
        body=body,
        is_ordered_map=is_ordered_map,
        data=data,
        spec=spec,
        line_prefix=line_prefix,
    )


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    line_prefix: str,
    indent: str,
    wrap: bool,
    variable_name: str | None,
    new_variable: bool,
    error_on_coercion: bool,
) -> str:
    r"""Convert a JSON string to native language literal text.

    Convert a JSON string to native language literal text.

    Args:
        json_string: A JSON string representing a scalar, array, or
            object.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        line_prefix: String to prepend to every output line
            (e.g. ``"        "`` for 8-space margin, or ``"\t\t"``
            for 2-tab margin).  Positions the generated block at
            the right column in surrounding source code.
        indent: Indentation step for elements inside delimiters when
            *wrap* is ``True`` (e.g. ``"    "`` for 4-space indent).
            Ignored when *wrap* is ``False``.
        wrap: If True, wrap the output in delimiters
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
        indent=indent,
        wrap=wrap,
        error_on_coercion=error_on_coercion,
    )
    if variable_name is not None:
        formatter = (
            language.format_variable_declaration
            if new_variable
            else language.format_variable_assignment
        )
        return formatter(variable_name, result)
    return result


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
    yaml_string: str,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    wrap: bool,
) -> _ResolvedComments:
    """Resolve comments for a YAML set."""
    ruamel_set: CommentedSet = YAML().load(  # pyright: ignore[reportUnknownMemberType]
        stream=StringIO(initial_value=yaml_string),
    )
    set_comments = extract_yaml_comments(ruamel_data=ruamel_set)
    if not language.supports_collection_comments:
        return _ResolvedComments(result=base, pending=set_comments)
    result = apply_collection_comments(
        collection_comments=set_comments,
        base=base,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        wrap=wrap,
    )
    return _ResolvedComments(result=result, pending=None)


@beartype
def _resolve_yaml_collection_comments(
    *,
    yaml_string: str,
    data: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    wrap: bool,
) -> _ResolvedComments:
    """Resolve comments for a YAML list or dict."""
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ruamel_data: CommentedSeq | CommentedMap = YAML().load(  # pyright: ignore[reportUnknownMemberType]
        stream=StringIO(initial_value=yaml_string),
    )
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
        wrap=wrap,
    )
    return _ResolvedComments(result=result, pending=None)


@beartype
def literalize_yaml(  # pylint: disable=too-many-branches,too-complex,too-many-statements
    *,
    yaml_string: str,
    language: Language,
    line_prefix: str,
    indent: str,
    wrap: bool,
    variable_name: str | None,
    new_variable: bool,
    error_on_coercion: bool,
) -> str:
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
        line_prefix: String to prepend to every output line
            (e.g. ``"        "`` for 8-space margin, or ``"\t\t"``
            for 2-tab margin).  Positions the generated block at
            the right column in surrounding source code.
        indent: Indentation step for elements inside delimiters when
            *wrap* is ``True`` (e.g. ``"    "`` for 4-space indent).
            Ignored when *wrap* is ``False``.
        wrap: If True, wrap the output in delimiters
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
    ruamel_yaml = YAML(typ="safe")
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        data = ruamel_yaml.load(stream=yaml_string)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    base = _literalize(
        data=_coerce_yaml_keys(data=cast("object", data)),
        language=language,
        line_prefix=line_prefix,
        indent=indent,
        wrap=wrap,
        error_on_coercion=error_on_coercion,
    )

    comment_cfg = language.comment_config
    cp = comment_cfg.prefix
    cs = comment_cfg.suffix
    comment_line_prefix = line_prefix + indent if wrap else line_prefix

    result: str
    pending_collection_comments: CollectionComments | None = None
    if isinstance(data, set):
        resolved = _resolve_yaml_set_comments(
            yaml_string=yaml_string,
            base=base,
            language=language,
            comment_prefix=cp,
            comment_suffix=cs,
            comment_line_prefix=comment_line_prefix,
            wrap=wrap,
        )
        result = resolved.result
        pending_collection_comments = resolved.pending
    elif not isinstance(data, (list, dict)):
        stream = StringIO(initial_value=yaml_string)
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        tokens = YAML().scan(stream=stream)  # pyright: ignore[reportUnknownMemberType]
        result = literalize_yaml_scalar(
            tokens=tokens,
            base=base,
            comment_prefix=cp,
            comment_suffix=cs,
            line_prefix=line_prefix,
        )
    elif not base:
        result = base
    else:
        resolved = _resolve_yaml_collection_comments(
            yaml_string=yaml_string,
            data=data,  # pyright: ignore[reportUnknownArgumentType]
            base=base,
            language=language,
            comment_prefix=cp,
            comment_suffix=cs,
            comment_line_prefix=comment_line_prefix,
            wrap=wrap,
        )
        result = resolved.result
        pending_collection_comments = resolved.pending

    if variable_name is not None:
        formatter = (
            language.format_variable_declaration
            if new_variable
            else language.format_variable_assignment
        )
        result = formatter(variable_name, result)

    if pending_collection_comments is not None:
        result = prepend_collection_comments(
            collection_comments=pending_collection_comments,
            base=result,
            comment_prefix=cp,
            comment_suffix=cs,
            line_prefix=line_prefix,
        )

    return result
