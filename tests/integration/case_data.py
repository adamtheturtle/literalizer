"""Parse fixture inputs and inspect their values during case discovery."""

import datetime as dt
import json
import math
import tomllib
from typing import assert_never

import json5_document
import jsonc_document
from beartype import beartype
from pydantic import TypeAdapter
from ruamel.yaml import YAML
from ruamel.yaml.comments import TaggedScalar
from typing_extensions import TypeIs

import literalizer
from literalizer._language import NewVariableNameSyntax
from tests.yaml_support import as_yaml_parser

from .case_inputs import CaseInput
from .yaml_warnings import expected_yaml_warnings

# Every scalar a parser can yield: JSON/JSON5 -> str/int/float/bool/
# None; TOML adds date/datetime/time; YAML via ruamel adds those plus
# bytes (``!!binary``).  Mirrors ``literalizer._types.Scalar`` but is
# spelled out so strict pyright keeps it fully known (the ruamel
# library ships no type stubs).
type _CaseScalar = (
    str | int | float | bool | dt.date | dt.datetime | dt.time | bytes | None
)
# Parsed case data.  ``load_case_data`` parses YAML with the ``safe``
# loader (and JSON/JSON5/TOML natively), so containers are plain
# ``dict``/``list``/``set`` rather than the ruamel comment-tracking
# subclasses; a precise model keeps ``@beartype`` accurate and strict
# pyright/ty fully resolved.
type CaseData = (
    _CaseScalar
    # A YAML ``!!pairs`` node resolves to a list of two-tuples.
    | tuple[object, CaseData]
    | list[CaseData]
    | dict[object, CaseData]
    | set[_CaseScalar]
    | frozenset[_CaseScalar]
)


def _is_object_dict(value: object, /) -> TypeIs[dict[object, object]]:
    """Narrow a dynamically typed mapping for strict type checkers."""
    return isinstance(value, dict)


def _is_object_list(value: object, /) -> TypeIs[list[object]]:
    """Narrow a dynamically typed sequence for strict type checkers."""
    return isinstance(value, list)


def _demote_yaml_tags(*, value: object) -> object:
    """Demote round-trip-only tagged scalar wrappers for discovery."""
    if isinstance(value, TaggedScalar):
        value = str(object=value)
    if _is_object_dict(value):
        return {
            _demote_yaml_tags(value=key): _demote_yaml_tags(value=item)
            for key, item in value.items()
        }
    if _is_object_list(value):
        return [_demote_yaml_tags(value=item) for item in value]
    return value


@beartype
def _load_case_source(
    *, source: str, input_format: literalizer.InputFormat
) -> object:
    """Load raw fixture data through the third-party format parsers."""
    match input_format:
        case literalizer.InputFormat.JSON:
            return json.loads(s=source)
        case literalizer.InputFormat.JSONC:
            return jsonc_document.loads(source=source)
        case literalizer.InputFormat.JSON5:
            return json5_document.loads(source=source)
        case literalizer.InputFormat.YAML:
            # ``safe`` (not round-trip): yields plain ``dict``/``list``/
            # ``set`` instead of the ruamel comment-tracking subclasses,
            # so the result matches ``CaseData`` exactly.  Comments are
            # irrelevant to the key/float predicates.
            # Plain ``=`` is a legacy value tag in the safe loader, while
            # Literalizer deliberately routes it through the round-trip
            # loader. Mirror that choice so discovery can inspect the same
            # valid fixtures as the public API.
            yaml_type = "safe"
            if "=" in source:
                yaml_type = "rt"
            # The pure loader accepts rebound anchors, like the public
            # parser; the C loader rejects these otherwise valid cases.
            # https://sourceforge.net/p/ruamel-yaml/tickets/43/
            yaml = as_yaml_parser(parser=YAML(typ=yaml_type, pure=True))
            return _demote_yaml_tags(value=yaml.load(stream=source))
        case literalizer.InputFormat.TOML:
            return tomllib.loads(source)
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def load_case_data(*, input_info: CaseInput) -> CaseData:
    """Parse a case input file according to its declared format.

    Dispatches on :attr:`CaseInput.input_format` so discovery code can
    inspect any case's data without knowing which serialization backs
    it.  ``tomllib``/``json``/``json5`` yield plain containers and
    ``ruamel`` yields its comment-tracking mappings; both are walked
    structurally by the ``has_*`` predicates.
    """
    with expected_yaml_warnings(
        expectation=input_info.expected_reused_anchor_warning,
    ):
        parsed = _load_case_source(
            source=input_info.path.read_text(encoding="utf-8"),
            input_format=input_info.input_format,
        )
    return TypeAdapter[CaseData](type=CaseData).validate_python(
        parsed,
        strict=True,
    )


def has_non_printable_ascii_dict_keys(data: CaseData) -> bool:
    """Return whether a nonempty dict key is outside printable ASCII."""
    match data:
        case dict():
            for key in data:
                if isinstance(key, str) and (
                    key != "" and (not key.isprintable() or not key.isascii())
                ):
                    return True
            return any(
                has_non_printable_ascii_dict_keys(data=v)
                for v in data.values()
            )
        case list():
            return any(
                has_non_printable_ascii_dict_keys(data=item) for item in data
            )
        case _:
            return False


def has_invalid_dict_keys(
    *, data: CaseData, key_syntax: NewVariableNameSyntax
) -> bool:
    """Return whether a nested string key violates its producer
    grammar.
    """
    match data:
        case dict():
            return any(
                isinstance(key, str) and not key_syntax.accepts(name=key)
                for key in data
            ) or any(
                has_invalid_dict_keys(data=value, key_syntax=key_syntax)
                for value in data.values()
            )
        case list():
            return any(
                has_invalid_dict_keys(data=item, key_syntax=key_syntax)
                for item in data
            )
        case _:
            return False


def has_special_floats(data: CaseData) -> bool:
    """Return ``True`` if *data* contains a non-finite float (``inf``,
    ``-inf``, or ``nan``).
    """
    match data:
        case float():
            return not math.isfinite(data)
        case dict():
            return any(has_special_floats(data=v) for v in data.values())
        case list():
            return any(has_special_floats(data=item) for item in data)
        case _:
            return False
