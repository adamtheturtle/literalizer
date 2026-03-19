"""Core conversion logic: formatting values and parsing JSON/YAML."""

import dataclasses
import datetime
import json
from collections.abc import Sequence
from io import StringIO
from typing import cast

from beartype import BeartypeConf, beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq, CommentedSet
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError

from literalizer._comments import (
    apply_collection_comments,
    extract_yaml_comments,
    literalize_yaml_scalar,
    prepend_collection_comments,
)
from literalizer._language import Language
from literalizer._types import Scalar, Value
from literalizer.exceptions import JSONParseError, YAMLParseError


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
        datetime.datetime,
        datetime.date,
    )
    for bucket in _buckets:
        if isinstance(value, bucket):
            return bucket
    return None


def _coerce_scalar_to_str(*, value: Value) -> str:
    """Convert a scalar to its string representation."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, str):
        return value
    return repr(value)


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


def _coerce_heterogeneous(*, data: Value) -> Value:
    """Recursively coerce heterogeneous all-scalar collections to
    strings.
    """
    if isinstance(data, ordereddict):
        new_omap: ordereddict = ordereddict()
        for k, v in data.items():  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
            new_omap[k] = _coerce_heterogeneous(data=v)  # pyright: ignore[reportUnknownArgumentType]
        omap_vals: list[Value] = list(new_omap.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        if _all_scalars_heterogeneous(values=omap_vals):
            for k in new_omap:  # pyright: ignore[reportUnknownVariableType]
                new_omap[k] = _coerce_scalar_to_str(
                    value=new_omap[k],  # pyright: ignore[reportUnknownArgumentType]
                )
        return new_omap

    if isinstance(data, dict):
        new_dict: dict[str, Value] = {
            k: _coerce_heterogeneous(data=v) for k, v in data.items()
        }
        if _all_scalars_heterogeneous(
            values=list(new_dict.values()),
        ):
            new_dict = {
                k: _coerce_scalar_to_str(value=v) for k, v in new_dict.items()
            }
        return new_dict

    if isinstance(data, set):
        items: list[Value] = list(data)
        if _all_scalars_heterogeneous(values=items):
            return {_coerce_scalar_to_str(value=v) for v in items}
        return data

    if isinstance(data, list):
        new_list = [_coerce_heterogeneous(data=v) for v in data]
        if _all_scalars_heterogeneous(values=new_list):
            return [_coerce_scalar_to_str(value=v) for v in new_list]
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
    return spec.format_dict_entry(key_str, val_str)


@beartype
def _format_set_value(*, value: set[Scalar], spec: Language) -> str:
    """Format a set value as a native language literal."""
    if not value and spec.empty_set is not None:
        return spec.empty_set
    sorted_items = sorted(value, key=lambda v: (type(v).__name__, repr(v)))
    formatted = [_format_scalar(value=v, spec=spec) for v in sorted_items]
    entries = [spec.format_set_entry(item) for item in formatted]
    joined = spec.element_separator.join(entries)
    return spec.set_open + joined + spec.set_close


@beartype
def _format_value(*, value: Value, spec: Language) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), dicts, and sets.
    """
    if isinstance(value, ordereddict):
        omap_items: list[tuple[str, Value]] = [
            (k, v)
            for k, v in value.items()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
            if not (spec.skip_null_dict_values and v is None)
        ]
        pairs = [
            spec.format_omap_entry(
                _format_value(value=k, spec=spec),
                _format_value(value=v, spec=spec),
            )
            for k, v in omap_items
        ]
        joined = spec.element_separator.join(pairs)
        return spec.omap_open + joined + spec.omap_close

    if isinstance(value, dict):
        dict_items: dict[str, Value] = {
            k: v
            for k, v in value.items()
            if not (spec.skip_null_dict_values and v is None)
        }
        if not dict_items and spec.empty_dict is not None:
            return spec.empty_dict
        pairs = [
            _build_dict_entry(
                key_str=_format_value(value=k, spec=spec),
                val_str=_format_value(value=v, spec=spec),
                spec=spec,
            )
            for k, v in dict_items.items()
        ]
        joined = spec.element_separator.join(pairs)
        return spec.dict_open(dict_items) + joined + spec.dict_close

    if isinstance(value, set):
        return _format_set_value(value=value, spec=spec)

    if isinstance(value, list):
        if not value and spec.empty_sequence is not None:
            return spec.empty_sequence
        items = [
            spec.format_sequence_entry(_format_value(value=v, spec=spec))
            for v in value
        ]
        joined = spec.element_separator.join(items)
        # Some languages (e.g. Python) require a trailing comma on
        # single-element sequences to avoid syntactic ambiguity.
        if len(items) == 1 and spec.single_element_trailing_comma:
            joined += spec.element_separator.strip()
        return f"{spec.sequence_open(value)}{joined}{spec.sequence_close}"

    return _format_scalar(value=value, spec=spec)


@beartype
def _wrap_body(
    *,
    body: str,
    is_omap: bool,
    data: list[Value] | dict[str, Value] | set[Scalar],
    spec: Language,
    line_prefix: str,
) -> str:
    """Wrap ``body`` in the language's open/close delimiters."""
    ci = spec.multiline_close_indent
    close_prefix = f"{line_prefix}{ci}"
    if is_omap:
        opening = f"{line_prefix}{spec.omap_open}"
        closing = f"{close_prefix}{spec.omap_close}"
    elif isinstance(data, dict):
        opening = f"{line_prefix}{spec.dict_open(data)}"
        closing = f"{close_prefix}{spec.dict_close}"
    elif isinstance(data, set):
        opening = f"{line_prefix}{spec.set_open}"
        closing = f"{close_prefix}{spec.set_close}"
    else:
        opening = f"{line_prefix}{spec.sequence_open(data)}"
        closing = f"{close_prefix}{spec.sequence_close}"
    return f"{opening.rstrip()}\n{body}\n{closing}"


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: Value,
    language: Language,
    line_prefix: str,
    indent: str,
    wrap: bool,
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
    """
    spec = language
    if spec.coerce_heterogeneous_to_strings:
        data = _coerce_heterogeneous(data=data)

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

    is_omap = isinstance(data, ordereddict)
    if is_omap or isinstance(data, dict):
        dict_data = cast("dict[str, Value]", data)
        entries = [
            (k, v)
            for k, v in dict_data.items()
            if not (spec.skip_null_dict_values and v is None)
        ]
        if not entries and wrap and dict_data:
            empty_value: ordereddict | dict[str, Value] = (
                ordereddict() if is_omap else {}
            )
            return _format_value(value=empty_value, spec=spec)
        last_idx = len(entries) - 1
        for i, (k, v) in enumerate(iterable=entries):
            formatted_key = _format_value(value=k, spec=spec)
            formatted_val = _format_value(value=v, spec=spec)
            entry = (
                spec.format_omap_entry(formatted_key, formatted_val)
                if is_omap
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
        # At this point data must be a list (scalars/dict/set/omap handled)
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
        is_omap=is_omap,
        data=data,
        spec=spec,
        line_prefix=line_prefix,
    )


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    line_prefix: str = "",
    indent: str = "    ",
    wrap: bool,
    variable_name: str | None = None,
    new_variable: bool = True,
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

    Raises:
        JSONParseError: If *json_string* is not valid JSON.
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
def literalize_yaml(  # noqa: PLR0912,C901,PLR0915  # pylint: disable=too-many-branches,too-complex,too-many-statements
    *,
    yaml_string: str,
    language: Language,
    line_prefix: str = "",
    indent: str = "    ",
    wrap: bool,
    variable_name: str | None = None,
    new_variable: bool = True,
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

    Raises:
        YAMLParseError: If *yaml_string* is not valid YAML.
    """
    ruamel_yaml = YAML(typ="safe")
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        data = ruamel_yaml.load(stream=yaml_string)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    base = _literalize(
        data=data,
        language=language,
        line_prefix=line_prefix,
        indent=indent,
        wrap=wrap,
    )

    cp = language.comment_prefix
    cs = language.comment_suffix

    comment_line_prefix = line_prefix + indent if wrap else line_prefix

    result: str
    pending_collection_comments = None
    if isinstance(data, set):
        ruamel_set: CommentedSet = YAML().load(  # pyright: ignore[reportUnknownMemberType]
            stream=StringIO(initial_value=yaml_string),
        )
        set_comments = extract_yaml_comments(ruamel_data=ruamel_set)
        if not language.supports_collection_comments:
            result = base
            pending_collection_comments = set_comments
        else:
            result = apply_collection_comments(
                collection_comments=set_comments,
                base=base,
                comment_prefix=cp,
                comment_suffix=cs,
                comment_line_prefix=comment_line_prefix,
                wrap=wrap,
            )
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
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        ruamel_data: CommentedSeq | CommentedMap = YAML().load(  # pyright: ignore[reportUnknownMemberType]
            stream=StringIO(initial_value=yaml_string),
        )
        collection_comments = extract_yaml_comments(
            ruamel_data=ruamel_data,
        )

        if language.skip_null_dict_values and isinstance(
            ruamel_data, CommentedMap
        ):
            pending: list[str] = []
            filtered_elements_list = []
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
                    filtered_elements_list.append(  # pyright: ignore[reportUnknownMemberType]
                        dataclasses.replace(ec, before=new_before),
                    )
            collection_comments = dataclasses.replace(
                collection_comments,
                elements=tuple(filtered_elements_list),  # pyright: ignore[reportUnknownArgumentType]
                trailing=(*pending, *collection_comments.trailing),
            )

        if not language.supports_collection_comments:
            result = base
            pending_collection_comments = collection_comments
        else:
            result = apply_collection_comments(
                collection_comments=collection_comments,
                base=base,
                comment_prefix=cp,
                comment_suffix=cs,
                comment_line_prefix=comment_line_prefix,
                wrap=wrap,
            )

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
