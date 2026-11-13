"""Parse reference inputs and prepare their declared bindings."""

import json
import tomllib
from collections.abc import Iterable, Iterator
from typing import assert_never

import json5_document
import jsonc_document
from beartype import beartype
from pydantic import TypeAdapter
from ruamel.yaml import YAML

import literalizer
from literalizer import ValueInput
from tests.yaml_support import as_yaml_parser

from .case_manifests import RefCaseSpec
from .language_specs import make_spec

type RefData = (
    dict[str, RefData]
    | list[RefData]
    | set[str | int | float | bool | None]
    | bytes
    | str
    | int
    | float
    | bool
    | None
)


@beartype
def collect_ref_names(data: RefData, *, ref_key: str) -> Iterator[str]:
    """Yield reference names in document order without intermediate lists.

    Binding preparation retains the first position of each repeated name,
    matching the order emitted by ``literalize`` for ``bound_refs``.
    """
    children: Iterable[RefData]
    match data:
        case dict():
            if len(data) == 1 and ref_key in data:
                name = data[ref_key]
                if isinstance(name, str):
                    yield name
                return
            children = data.values()
        case list():
            children = data
        case _:
            return
    for child in children:
        yield from collect_ref_names(data=child, ref_key=ref_key)


@beartype
def parse_ref_input(
    *,
    input_format: literalizer.InputFormat,
    input_source: str,
) -> RefData:
    """Parse *input_source* into raw data for ref-name collection.

    Mirrors the format dispatch in :func:`literalizer.parse_input` but
    yields plain Python containers so :func:`collect_ref_names` can
    walk them structurally.
    """
    parsed: object
    match input_format:
        case literalizer.InputFormat.JSON:
            parsed = json.loads(s=input_source)
        case literalizer.InputFormat.JSONC:
            parsed = jsonc_document.loads(source=input_source)
        case literalizer.InputFormat.JSON5:
            parsed = json5_document.loads(source=input_source)
        case literalizer.InputFormat.YAML:
            # Reference discovery needs plain values, including YAML sets;
            # the public renderer preserves comments from input_source.
            ruamel_yaml = as_yaml_parser(parser=YAML(typ="safe"))
            parsed = ruamel_yaml.load(stream=input_source)
        case literalizer.InputFormat.TOML:
            parsed = tomllib.loads(input_source)
        case _ as unreachable:
            assert_never(unreachable)
    return TypeAdapter[RefData](type=RefData).validate_python(
        parsed,
        strict=True,
    )


@beartype
def bound_ref_inputs(
    *,
    config: RefCaseSpec,
    raw_data: RefData,
    lang_cls: literalizer.LanguageCls,
) -> dict[str, ValueInput]:
    """Prepare referenced bindings and the case's additional
    declarations.
    """
    collected_bound_refs_input: dict[str, ValueInput] = {}
    key_syntax = make_spec(lang_cls=lang_cls).dict_format_config.key_syntax
    effective_s = '{"_": "_"}'
    if key_syntax is not None and not key_syntax.accepts(name="_"):
        effective_s = '{"key": "value"}'
    for entry_raw_name in collect_ref_names(
        data=raw_data, ref_key=config.ref_key
    ):
        collected_bound_refs_input[entry_raw_name] = json.loads(
            s=config.value_sources.get(entry_raw_name, effective_s)
        )
    bound_refs_input: dict[str, ValueInput] = collected_bound_refs_input
    bound_refs_input.update(
        {
            name: json.loads(s=source)
            for name, source in config.extra_ref_value_sources.items()
        },
    )
    if config.bound_refs is not None:
        bound_refs_input.update(config.bound_refs)
    bound_refs_input.update(config.bound_ref_times)
    bound_refs_input.update(config.bound_ref_datetimes)
    bound_refs_input.update(
        {
            name: source.to_value()
            for name, source in config.bound_ref_values.items()
        }
    )
    return bound_refs_input
