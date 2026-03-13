"""Convert JSON data to native language literals."""

from __future__ import annotations

import dataclasses
import datetime
import json
from collections.abc import Mapping, Sequence  # noqa: TC003
from typing import Any, Protocol, cast, runtime_checkable

import yaml
from beartype import beartype


@runtime_checkable
class Language(Protocol):
    """Protocol describing how a language formats scalar literals and
    collections.

    Implement this protocol to add support for additional languages
    beyond the built-in defaults.
    """

    @property
    def null_literal(self) -> str: ...
    @property
    def true_literal(self) -> str: ...
    @property
    def false_literal(self) -> str: ...
    @property
    def collection_open(self) -> str: ...
    @property
    def collection_close(self) -> str: ...
    @property
    def dict_separator(self) -> str: ...


@dataclasses.dataclass(frozen=True)
class LanguageSpec:
    """A concrete implementation of :class:`Language`.

    Predefined specs for common languages are available as module-level
    constants (e.g. :data:`PYTHON`, :data:`JAVASCRIPT`).  Create custom
    instances to support additional languages or override defaults.
    """

    null_literal: str
    true_literal: str
    false_literal: str
    collection_open: str
    collection_close: str
    dict_separator: str


PYTHON = LanguageSpec(
    null_literal="None",
    true_literal="True",
    false_literal="False",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
)

CSHARP = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
)

JAVASCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=": ",
)

TYPESCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=": ",
)

RUBY = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=" => ",
)

GO = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

CPP = LanguageSpec(
    null_literal="nullptr",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

JAVA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

KOTLIN = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="listOf(",
    collection_close=")",
    dict_separator=": ",
)


@beartype
def _format_scalar(*, value: Any, spec: Language) -> str:  # noqa: ANN401
    """Format a scalar JSON value as a native language literal."""
    if value is None:
        return spec.null_literal

    if isinstance(value, bool):
        return spec.true_literal if value else spec.false_literal

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        return repr(value)

    if isinstance(value, str):
        escaped = (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )
        return f'"{escaped}"'

    if isinstance(value, (datetime.datetime, datetime.date)):
        return f'"{value.isoformat()}"'

    msg = f"Unsupported scalar type: {type(value)}"
    raise TypeError(msg)


@beartype
def _format_value(*, value: Any, spec: Language) -> str:  # noqa: ANN401
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), and dicts.
    """
    if isinstance(value, dict):
        pairs = [
            f"{_format_value(value=k, spec=spec)}{spec.dict_separator}"
            f"{_format_value(value=v, spec=spec)}"
            for k, v in cast("dict[str, object]", value).items()
        ]
        return "{" + ", ".join(pairs) + "}"

    if isinstance(value, list):
        items = [
            _format_value(value=v, spec=spec)
            for v in cast("list[object]", value)
        ]
        joined = ", ".join(items)
        # Single-element tuples need a trailing comma in Python/C#.
        if len(items) == 1 and spec.collection_open == "(":
            joined += ","
        return f"{spec.collection_open}{joined}{spec.collection_close}"

    return _format_scalar(value=value, spec=spec)


@beartype
def literalize(
    *,
    data: Sequence[Any] | Mapping[str, Any] | float | bool | None,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified prefix.

    Args:
        data: A scalar, sequence, or mapping.  Scalars (strings,
            numbers, booleans, ``None``) are formatted as a single
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

    # Handle scalars (check str before Sequence since str is a Sequence).
    if isinstance(data, (str, int, float, bool)) or data is None:
        return f"{prefix}{_format_scalar(value=data, spec=spec)}"

    effective_prefix = prefix if not wrap else (prefix or "    ")
    lines: list[str] = []

    if isinstance(data, dict):
        for k, v in cast("dict[str, object]", data).items():
            formatted_key = _format_value(value=k, spec=spec)
            formatted_val = _format_value(value=v, spec=spec)
            lines.append(
                f"{effective_prefix}{formatted_key}{spec.dict_separator}{formatted_val},"
            )
    else:
        for item in data:
            formatted = _format_value(value=item, spec=spec)
            lines.append(f"{effective_prefix}{formatted},")

    body = "\n".join(lines)

    if not wrap or not body:
        return body

    if isinstance(data, dict):
        return f"{{\n{body}\n}}"

    return f"[\n{body}\n]"


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert a JSON string to native language literal text.

    This is a convenience wrapper around :func:`literalize` that
    accepts JSON as a string rather than a pre-parsed data structure.

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

    Raises:
        json.JSONDecodeError: If *json_string* is not valid JSON.
    """
    data = json.loads(json_string)
    return literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )


@beartype
def literalize_yaml(
    *,
    yaml_string: str,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert a YAML string to native language literal text.

    This is a convenience wrapper around :func:`literalize` that
    accepts YAML as a string rather than a pre-parsed data structure.

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

    Raises:
        yaml.YAMLError: If *yaml_string* is not valid YAML.
    """
    data = yaml.safe_load(yaml_string)
    return literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )
