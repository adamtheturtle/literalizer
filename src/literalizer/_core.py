"""Core conversion logic: formatting values and parsing input formats."""

import dataclasses
import datetime
import enum
import json
import math
from collections.abc import Sequence
from io import StringIO
from typing import Any, assert_never, cast

import pyjson5
import tomlkit
from beartype import BeartypeConf, beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError
from tomlkit.exceptions import TOMLKitError

from literalizer._coercions import (
    _all_scalars_heterogeneous,
    _apply_coercions,
    _coerce_scalar_to_str,
    _scalar_type_bucket,
)
from literalizer._comments import (
    CollectionComments,
    ElementComments,
    apply_collection_comments,
    extract_toml_comments,
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
    JSON5ParseError,
    JSONParseError,
    TOMLParseError,
    YAMLParseError,
)


class InputFormat(enum.Enum):
    """Supported input serialization formats."""

    JSON = enum.auto()
    JSON5 = enum.auto()
    YAML = enum.auto()
    TOML = enum.auto()


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

    body_preamble: tuple[str, ...]
    """Type-definition lines (e.g. F#'s ``type Val = …``, Haskell's
    ``data Val = …`` and typeclass instances) that are prepended to
    :attr:`code`.  Empty when none are needed.

    Use :attr:`bare_code` to obtain the literal text *without* these
    lines.
    """

    pre_declaration_comments: tuple[str, ...] = ()
    """Already-formatted comment lines that appear between
    :attr:`body_preamble` and the variable declaration/assignment in
    :attr:`code`.  These come from scalar before-comments when the
    language does not support them inline.

    Included in :attr:`bare_code` but excluded from
    :attr:`declaration_code`.
    """

    @property
    def bare_code(self) -> str:
        """The literal text without :attr:`body_preamble` prepended.

        Identical to :attr:`code` when :attr:`body_preamble` is empty.
        :attr:`pre_declaration_comments` are preserved.
        """
        if not self.body_preamble:
            return self.code
        prefix = "\n".join(self.body_preamble) + "\n"
        return self.code[len(prefix) :]

    @property
    def declaration_code(self) -> str:
        """The literal text without :attr:`body_preamble` or
        :attr:`pre_declaration_comments` prepended.

        Use this when you need just the variable declaration or
        assignment, without any preceding comment lines.
        """
        all_prefix_lines = (
            *self.body_preamble,
            *self.pre_declaration_comments,
        )
        if not all_prefix_lines:
            return self.code
        prefix = "\n".join(all_prefix_lines) + "\n"
        return self.code[len(prefix) :]


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
    )


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
    if set_cfg.coerce_mixed_to_str and _all_scalars_heterogeneous(
        values=list(value),
    ):
        value = {_coerce_scalar_to_str(value=v) for v in value}
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
        else dict_cfg.dict_open(dict_items)
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
    dict_open = spec.dict_format_config.dict_open
    dicts: list[dict[str, Value]] = [
        item
        for item in items
        if isinstance(item, dict) and not isinstance(item, ordereddict)
    ]
    # Widening compares openers across dicts, so we need at least two
    # to have anything to compare.
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

    openers = {dict_open(d) for d in filtered_dicts}
    if len(openers) <= 1:
        return None

    # Types differ: combine all values to infer the widened type.
    combined: dict[str, Value] = {}
    idx = 0
    for d in filtered_dicts:
        for v in d.values():
            combined[f"_k{idx}"] = v
            idx += 1
    return dict_open(combined)


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

        opening = f"{line_prefix}{dict_cfg.dict_open(data)}"
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


def _append_entries(
    *,
    formatted_entries: Sequence[str],
    lines: list[str],
    body_prefix: str,
    trailing_comma: bool,
    spec: Language,
) -> None:
    """Append formatted entries with separators to *lines*."""
    last_idx = len(formatted_entries) - 1
    for i, entry in enumerate(iterable=formatted_entries):
        add_sep = i < last_idx or trailing_comma
        sep = spec.element_separator.strip() if add_sep else ""
        lines.append(f"{body_prefix}{entry}{sep}")


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
            formatted_entries: list[str] = []
            for k, v in entries:
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
                formatted_entries.append(entry)
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=trailing_comma,
                spec=spec,
            )
        case set() as set_data:
            sorted_items = sorted(
                set_data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            formatted_entries = [
                spec.format_set_entry(
                    item,
                    _format_value(
                        value=item,
                        spec=spec,
                        dict_open_override=None,
                    ),
                )
                for item in sorted_items
            ]
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=trailing_comma,
                spec=spec,
            )
        case list() as list_data:
            seq_trailing = (
                trailing_comma
                and spec.sequence_format_config.supports_trailing_comma
            )
            dict_open_override = _compute_sequence_dict_override(
                items=list_data,
                spec=spec,
            )
            formatted_entries = [
                spec.format_sequence_entry(
                    element,
                    _format_value(
                        value=element,
                        spec=spec,
                        dict_open_override=dict_open_override,
                    ),
                )
                for element in list_data
            ]
            _append_entries(
                formatted_entries=formatted_entries,
                lines=lines,
                body_prefix=body_prefix,
                trailing_comma=seq_trailing,
                spec=spec,
            )
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

    if (
        isinstance(data, set)
        and spec.set_format_config.coerce_mixed_to_str
        and _all_scalars_heterogeneous(values=list(data))
    ):
        data = {_coerce_scalar_to_str(value=v) for v in data}

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


@dataclasses.dataclass(frozen=True)
class _ParsedInput:
    """Result of parsing an input string."""

    data: Value
    raw_data: object


def _parse_json(*, source: str) -> _ParsedInput:
    """Parse a JSON string into a ``_ParsedInput``."""
    try:
        data = json.loads(s=source)
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        )
        raise JSONParseError(message) from exc
    return _ParsedInput(data=data, raw_data=data)


def _parse_json5(*, source: str) -> _ParsedInput:
    """Parse a JSON5 string into a ``_ParsedInput``."""
    try:
        data = pyjson5.decode(data=source)  # pylint: disable=no-member
    except pyjson5.Json5DecoderException as exc:  # pylint: disable=no-member
        message = f"Invalid JSON5: {exc}"
        raise JSON5ParseError(message) from exc
    return _ParsedInput(data=data, raw_data=data)


def _parse_yaml(*, source: str) -> _ParsedInput:
    """Parse a YAML string into a ``_ParsedInput``."""
    ruamel_yaml = YAML(typ="safe")
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        raw_data = ruamel_yaml.load(stream=source)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    data = _coerce_yaml_keys(data=raw_data)
    return _ParsedInput(data=data, raw_data=raw_data)


def _parse_toml(*, source: str) -> _ParsedInput:
    """Parse a TOML string into a ``_ParsedInput``."""
    try:
        toml_doc = tomlkit.parse(string=source)
    except TOMLKitError as exc:
        message = f"Invalid TOML: {exc}"
        raise TOMLParseError(message) from exc
    toml_data = _coerce_toml_values(data=toml_doc.unwrap())
    return _ParsedInput(data=toml_data, raw_data=toml_doc)


def _parse_input(*, source: str, input_format: InputFormat) -> _ParsedInput:
    """Parse and coerce an input string according to its format."""
    match input_format:
        case InputFormat.JSON:
            return _parse_json(source=source)
        case InputFormat.JSON5:
            return _parse_json5(source=source)
        case InputFormat.YAML:
            return _parse_yaml(source=source)
        case InputFormat.TOML:
            return _parse_toml(source=source)
    assert_never(input_format)  # pragma: no cover


@beartype
def literalize(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    pre_indent_level: int = 0,
    include_delimiters: bool = True,
    variable_name: str | None = None,
    new_variable: bool = True,
    error_on_coercion: bool = False,
) -> LiteralizeResult:
    r"""Convert a JSON, JSON5, YAML, or TOML string to a native
    language literal.

    YAML and TOML comments are preserved in the output using the
    target language's comment syntax.

    Args:
        source: The input string to convert.
        input_format: The serialization format of *source*.
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
        JSONParseError: If *input_format* is ``JSON`` and *source* is
            not valid JSON.
        JSON5ParseError: If *input_format* is ``JSON5`` and *source*
            is not valid JSON5.
        YAMLParseError: If *input_format* is ``YAML`` and *source* is
            not valid YAML.
        TOMLParseError: If *input_format* is ``TOML`` and *source* is
            not valid TOML.
        HeterogeneousCoercionError: If *error_on_coercion* is ``True``
            and the data contains heterogeneous scalar collections
            that would be coerced.
    """
    line_prefix = language.indent * pre_indent_level
    parsed = _parse_input(source=source, input_format=input_format)
    data = parsed.data

    # --- Format ---
    result = _literalize(
        data=data,
        language=language,
        line_prefix=line_prefix,
        include_delimiters=include_delimiters,
        error_on_coercion=error_on_coercion,
    )

    # --- Comment resolution ---
    resolved: _ResolvedComments | None = None
    if input_format is InputFormat.YAML:
        comment_cfg = language.comment_config
        cp = comment_cfg.prefix
        cs = comment_cfg.suffix
        comment_line_prefix = (
            line_prefix + language.indent
            if include_delimiters
            else line_prefix
        )
        resolved = _resolve_yaml_comments(
            yaml_string=source,
            data=parsed.raw_data,
            base=result,
            language=language,
            comment_prefix=cp,
            comment_suffix=cs,
            comment_line_prefix=comment_line_prefix,
            line_prefix=line_prefix,
            include_delimiters=include_delimiters,
        )
        result = resolved.result
    elif input_format is InputFormat.TOML:
        comment_cfg = language.comment_config
        comment_line_prefix = (
            line_prefix + language.indent
            if include_delimiters
            else line_prefix
        )
        resolved = _resolve_toml_comments(
            toml_doc=parsed.raw_data,
            base=result,
            language=language,
            comment_prefix=comment_cfg.prefix,
            comment_suffix=comment_cfg.suffix,
            comment_line_prefix=comment_line_prefix,
            include_delimiters=include_delimiters,
        )
        result = resolved.result

    # --- Variable wrapping ---
    result = _apply_variable_wrapper(
        result=result,
        language=language,
        data=data,
        variable_name=variable_name,
        new_variable=new_variable,
    )

    # --- Pending comments ---
    if resolved is not None and resolved.pending is not None:
        comment_cfg = language.comment_config
        result = prepend_collection_comments(
            collection_comments=resolved.pending,
            base=result,
            comment_prefix=comment_cfg.prefix,
            comment_suffix=comment_cfg.suffix,
            line_prefix=line_prefix,
        )

    if resolved is not None and resolved.pending_scalar_before:
        result = "\n".join(resolved.pending_scalar_before) + "\n" + result

    # --- Preamble ---
    computed = _compute_preamble(
        data=data,
        language=language,
        has_variable_declaration=variable_name is not None and new_variable,
    )
    preamble = tuple(language.static_preamble) + computed.header
    if computed.body:
        result = "\n".join(computed.body) + "\n" + result

    pre_decl = resolved.pending_scalar_before if resolved is not None else ()
    return LiteralizeResult(
        code=result,
        preamble=preamble,
        body_preamble=computed.body,
        pre_declaration_comments=pre_decl,
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
    """Result of resolving YAML comments for a collection or scalar."""

    result: str
    pending: CollectionComments | None
    pending_scalar_before: tuple[str, ...]
    """Already-formatted comment lines to prepend before the variable
    declaration.  Used for scalar before-comments when the language
    does not support them inline (see
    :attr:`~literalizer.Language.supports_scalar_before_comments`).
    """


@beartype
def _resolve_collection_comments(
    *,
    collection_comments: CollectionComments,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> _ResolvedComments:
    """Resolve pre-extracted collection comments."""
    if not language.supports_collection_comments:
        return _ResolvedComments(
            result=base,
            pending=collection_comments,
            pending_scalar_before=(),
        )
    result = apply_collection_comments(
        collection_comments=collection_comments,
        base=base,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )
    return _ResolvedComments(
        result=result,
        pending=None,
        pending_scalar_before=(),
    )


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

    return _resolve_collection_comments(
        collection_comments=collection_comments,
        base=base,
        language=language,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )


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
        return _resolve_collection_comments(
            collection_comments=extract_yaml_comments(
                ruamel_data=ruamel_set,
            ),
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
        scalar_result = literalize_yaml_scalar(
            tokens=tokens,
            base=base,
            comment_prefix=comment_prefix,
            comment_suffix=comment_suffix,
            line_prefix=line_prefix,
            supports_scalar_before_comments=language.supports_scalar_before_comments,
            supports_scalar_inline_comments=language.supports_scalar_inline_comments,
        )
        return _ResolvedComments(
            result=scalar_result.result,
            pending=None,
            pending_scalar_before=scalar_result.pending_before,
        )

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
def _resolve_toml_comments(
    *,
    toml_doc: object,
    base: str,
    language: Language,
    comment_prefix: str,
    comment_suffix: str,
    comment_line_prefix: str,
    include_delimiters: bool,
) -> _ResolvedComments:
    """Extract and resolve comments from a tomlkit document."""
    return _resolve_collection_comments(
        collection_comments=extract_toml_comments(toml_doc=toml_doc),
        base=base,
        language=language,
        comment_prefix=comment_prefix,
        comment_suffix=comment_suffix,
        comment_line_prefix=comment_line_prefix,
        include_delimiters=include_delimiters,
    )


def _coerce_toml_values(*, data: object) -> Value:
    """Recursively convert TOML-specific types to ``Value`` types.

    ``tomlkit`` produces ``datetime.time`` values which are not
    representable in the ``Value`` type, so they are converted to
    their ISO-format string form.
    """
    match data:
        case dict():
            return {
                k: _coerce_toml_values(data=v)
                for k, v in cast("dict[str, object]", data).items()
            }
        case list():
            return [
                _coerce_toml_values(data=item)
                for item in cast("list[object]", data)
            ]
        case datetime.time():
            return data.isoformat()
        case _:
            return cast("Value", data)
