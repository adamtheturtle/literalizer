"""Core conversion logic: formatting values and parsing JSON/YAML."""

import dataclasses
import datetime
import json
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
)
from literalizer._language import Language
from literalizer._types import Scalar, Value
from literalizer.exceptions import JSONParseError, YAMLParseError


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
        dict_items = {
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
        return spec.dict_open + joined + spec.dict_close

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
) -> str:
    """Wrap ``body`` in the language's open/close delimiters."""
    ci = spec.multiline_close_indent
    if is_omap:
        return f"{spec.omap_open}\n{body}\n{ci}{spec.omap_close}"
    if isinstance(data, dict):
        return f"{spec.dict_open}\n{body}\n{ci}{spec.dict_close}"
    if isinstance(data, set):
        return f"{spec.set_open}\n{body}\n{ci}{spec.set_close}"
    return f"{spec.sequence_open(data)}\n{body}\n{ci}{spec.sequence_close}"


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: Value,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified prefix.

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
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
        wrap: If True, wrap the output in delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
            Ignored for scalar values.
    """
    spec = language

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
        return f"{prefix}{_format_scalar(value=data, spec=spec)}"

    effective_prefix = prefix if not wrap else (prefix or "    ")
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
            lines.append(f"{effective_prefix}{entry}{sep}")
    elif isinstance(data, set):
        sorted_items = sorted(data, key=lambda v: (type(v).__name__, repr(v)))
        last_idx = len(sorted_items) - 1
        for i, item in enumerate(iterable=sorted_items):
            formatted = _format_value(value=item, spec=spec)
            entry = spec.format_set_entry(formatted)
            add_sep = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator.strip() if add_sep else ""
            lines.append(f"{effective_prefix}{entry}{sep}")
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
            lines.append(f"{effective_prefix}{formatted}{sep}")

    body = "\n".join(lines)

    if not wrap or not body:
        return body

    return _wrap_body(body=body, is_omap=is_omap, data=data, spec=spec)


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    prefix: str,
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
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
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
        prefix=prefix,
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
def literalize_yaml(
    *,
    yaml_string: str,
    language: Language,
    prefix: str,
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
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
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
        prefix=prefix,
        wrap=wrap,
    )

    cp = language.comment_prefix
    cs = language.comment_suffix

    result: str
    if isinstance(data, set):
        ruamel_set: CommentedSet = YAML().load(  # pyright: ignore[reportUnknownMemberType]
            stream=StringIO(initial_value=yaml_string),
        )
        set_comments = extract_yaml_comments(ruamel_data=ruamel_set)
        result = apply_collection_comments(
            collection_comments=set_comments,
            base=base,
            comment_prefix=cp,
            comment_suffix=cs,
            prefix=prefix,
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
            prefix=prefix,
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

        result = apply_collection_comments(
            collection_comments=collection_comments,
            base=base,
            comment_prefix=cp,
            comment_suffix=cs,
            prefix=prefix,
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
