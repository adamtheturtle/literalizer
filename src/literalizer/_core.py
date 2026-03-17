"""Core conversion logic: formatting values and parsing JSON/YAML."""

from __future__ import annotations

import dataclasses
import datetime
import json
from io import StringIO
from typing import TYPE_CHECKING, Any, cast

from beartype import BeartypeConf, beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.compat import ordereddict
from ruamel.yaml.error import YAMLError

from literalizer._comments import (
    YamlCollectionContext,
    extract_yaml_comments,
    literalize_yaml_collection,
    literalize_yaml_scalar,
)
from literalizer._language import Language  # noqa: TC001
from literalizer._types import Scalar, Value  # noqa: TC001
from literalizer.exceptions import JSONParseError, YAMLParseError

if TYPE_CHECKING:
    from ruamel.yaml.comments import CommentedSeq


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
        escaped = (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )
        result = f'"{escaped}"'
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
    sep = f"{spec.element_separator} "
    return spec.set_open + sep.join(entries) + spec.set_close


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
        sep = f"{spec.element_separator} "
        return spec.omap_open + sep.join(pairs) + spec.omap_close

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
        sep = f"{spec.element_separator} "
        return spec.dict_open + sep.join(pairs) + spec.dict_close

    if isinstance(value, set):
        return _format_set_value(value=value, spec=spec)

    if isinstance(value, list):
        if not value and spec.empty_collection is not None:
            return spec.empty_collection
        items = [
            spec.format_list_entry(_format_value(value=v, spec=spec))
            for v in value
        ]
        sep = f"{spec.element_separator} "
        joined = sep.join(items)
        # Some languages (e.g. Python) require a trailing comma on
        # single-element collections to avoid syntactic ambiguity.
        if len(items) == 1 and spec.single_element_trailing_comma:
            joined += spec.element_separator
        return f"{spec.collection_open}{joined}{spec.collection_close}"

    return _format_scalar(value=value, spec=spec)


@beartype
def _wrap_body(
    *,
    body: str,
    is_omap: bool,
    data: list[Any] | dict[str, Any] | set[Any],
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
    return f"{spec.collection_open}\n{body}\n{ci}{spec.collection_close}"


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def _literalize(
    *,
    data: list[Any]
    | dict[str, Any]
    | set[Any]
    | str
    | bytes
    | datetime.date
    | float
    | bool
    | None,
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
        dict_data = cast("dict[str, Any]", data)
        entries = [
            (k, v)
            for k, v in dict_data.items()
            if not (spec.skip_null_dict_values and v is None)
        ]
        if not entries and wrap and dict_data:
            empty_value: ordereddict | dict[str, Any] = (
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
            add_comma = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator if add_comma else ""
            lines.append(f"{effective_prefix}{entry}{sep}")
    elif isinstance(data, set):
        sorted_items = sorted(data, key=lambda v: (type(v).__name__, repr(v)))
        last_idx = len(sorted_items) - 1
        for i, item in enumerate(iterable=sorted_items):
            formatted = _format_value(value=item, spec=spec)
            entry = spec.format_set_entry(formatted)
            add_comma = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator if add_comma else ""
            lines.append(f"{effective_prefix}{entry}{sep}")
    else:
        items = list(data)
        last_idx = len(items) - 1
        for i, item in enumerate(iterable=items):
            formatted = spec.format_list_entry(
                _format_value(value=item, spec=spec)
            )
            add_comma = i < last_idx or spec.multiline_trailing_comma
            sep = spec.element_separator if add_comma else ""
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

    if isinstance(data, set):
        result = base
    elif not isinstance(data, (list, dict)):
        stream = StringIO(initial_value=yaml_string)
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        tokens = YAML().scan(stream=stream)  # pyright: ignore[reportUnknownMemberType]
        result = literalize_yaml_scalar(
            tokens=tokens,
            base=base,
            comment_prefix=cp,
            prefix=prefix,
        )
    elif not base:
        result = base
    else:
        is_sequence = isinstance(data, list)
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        ruamel_data: CommentedSeq | CommentedMap = YAML().load(  # pyright: ignore[reportUnknownMemberType]
            stream=StringIO(initial_value=yaml_string),
        )
        collection_comments = extract_yaml_comments(
            ruamel_data=ruamel_data,
            is_sequence=is_sequence,
        )

        if (
            not is_sequence
            and language.skip_null_dict_values
            and isinstance(ruamel_data, CommentedMap)
        ):
            filtered_elements = tuple(
                ec
                for key, ec in zip(  # pyright: ignore[reportUnknownVariableType]
                    ruamel_data.keys(),  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                    collection_comments.elements,
                    strict=True,
                )
                if data[key] is not None
            )
            collection_comments = dataclasses.replace(
                collection_comments,
                elements=filtered_elements,
            )

        has_comments = (
            any(
                element_comment.before or element_comment.inline
                for element_comment in collection_comments.elements
            )
            or collection_comments.trailing
        )
        if not has_comments:
            result = base
        else:
            ctx = YamlCollectionContext(
                base=base,
                element_comments=collection_comments.elements,
                trailing=collection_comments.trailing,
                comment_prefix=cp,
                prefix=prefix,
                wrap=wrap,
            )
            result = literalize_yaml_collection(ctx=ctx)

    if variable_name is not None:
        formatter = (
            language.format_variable_declaration
            if new_variable
            else language.format_variable_assignment
        )
        return formatter(variable_name, result)
    return result
