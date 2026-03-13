"""Convert JSON data to native language literals."""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence
from typing import Any, cast

from beartype import beartype


@dataclasses.dataclass(frozen=True)
class _LanguageSpec:
    """Describes how a language formats scalar literals and collections.

    Predefined specs for common languages are available in
    :data:`_LANGUAGE_SPECS`.  Create custom instances to support
    additional languages or override defaults.
    """

    null_literal: str
    true_literal: str
    false_literal: str
    collection_open: str
    collection_close: str
    dict_separator: str


_LANGUAGE_SPECS: dict[str, _LanguageSpec] = {
    "py": _LanguageSpec(
        null_literal="None",
        true_literal="True",
        false_literal="False",
        collection_open="(",
        collection_close=")",
        dict_separator=": ",
    ),
    "cs": _LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="(",
        collection_close=")",
        dict_separator=": ",
    ),
    "js": _LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="[",
        collection_close="]",
        dict_separator=": ",
    ),
    "ts": _LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="[",
        collection_close="]",
        dict_separator=": ",
    ),
    "rb": _LanguageSpec(
        null_literal="nil",
        true_literal="true",
        false_literal="false",
        collection_open="[",
        collection_close="]",
        dict_separator=" => ",
    ),
    "go": _LanguageSpec(
        null_literal="nil",
        true_literal="true",
        false_literal="false",
        collection_open="{",
        collection_close="}",
        dict_separator=": ",
    ),
    "cpp": _LanguageSpec(
        null_literal="nullptr",
        true_literal="true",
        false_literal="false",
        collection_open="{",
        collection_close="}",
        dict_separator=": ",
    ),
    "java": _LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="{",
        collection_close="}",
        dict_separator=": ",
    ),
    "kt": _LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="listOf(",
        collection_close=")",
        dict_separator=": ",
    ),
}


@beartype
def _resolve_spec(*, language: str) -> _LanguageSpec:
    """Look up the spec for *language*.

    Raises :exc:`KeyError` if *language* is not in :data:`_LANGUAGE_SPECS`.
    """
    return _LANGUAGE_SPECS[language]


@beartype
def _format_scalar(*, value: Any, spec: _LanguageSpec) -> str:  # noqa: ANN401
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

    msg = f"Unsupported scalar type: {type(value)}"
    raise TypeError(msg)


@beartype
def _format_value(*, value: Any, spec: _LanguageSpec) -> str:  # noqa: ANN401
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
def convert_json_to_native_literal(
    *,
    data: Sequence[Any] | Mapping[str, Any],
    language: str,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert parsed JSON data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified prefix.

    Args:
        data: A JSON array or object.  Arrays may contain scalars,
            arrays, or dicts with nesting to arbitrary depth.  Objects
            are formatted as one key-value pair per line using the
            language's dict separator.
        language: File extension identifying the target language
            (e.g. ``"py"``, ``"ts"``, ``"go"``).  Must be a key in
            :data:`_LANGUAGE_SPECS`.
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
        wrap: If True, wrap the output in delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
    """
    spec = _resolve_spec(language=language)
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
