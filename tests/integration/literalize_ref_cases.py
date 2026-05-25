"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

The configurations describe how each ``cases/literalize_ref_*`` directory is
driven through :func:`literalizer.literalize` with a ``ref_case`` set to the
language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import dataclasses
import datetime
import enum
import functools
import json
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import assert_never

import pyjson5
import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML as _YAML

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
    VariableNameNotSupportedError,
)

from .case_discovery import (
    LITERALIZE_DEFAULT_REF_CASE_CONFIGS,
    LITERALIZE_REF_CASE_CONFIGS,
    LiteralizeRefCaseConfig,
    case_input,
)
from .language_specs import (
    make_golden_path,
    sorted_languages,
    with_per_fixture_module_name,
)
from .variant_cases import wrap_variable_form

type _Scalar = (
    str
    | int
    | float
    | bool
    | None
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
)
type _ValueInput = (
    _Scalar
    | Sequence[_ValueInput]
    | Mapping[_Scalar, _ValueInput]
    | set[_Scalar]
)


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: LiteralizeRefCaseConfig
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def discover_literalize_ref_cases() -> list[LiteralizeRefCase]:
    """Return literalize-ref test cases for all languages.

    A case carrying a ``ref_case_override`` is filtered to languages
    whose ``supported_ref_cases`` includes that override; the remaining
    languages cannot produce a golden file for the forced ref case and
    are excluded from discovery so the orphan-files check stays
    accurate.
    """
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in LITERALIZE_REF_CASE_CONFIGS
        for lang_cls in sorted_languages()
        if config.ref_case_override is None
        or config.ref_case_override in lang_cls.supported_ref_cases
    ]


@functools.cache
@beartype
def discover_literalize_default_ref_cases() -> list[LiteralizeRefCase]:
    """Return default literalize-ref test cases for all languages."""
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in LITERALIZE_DEFAULT_REF_CASE_CONFIGS
        for lang_cls in sorted_languages()
    ]


type _RefData = (
    dict[str, _RefData] | list[_RefData] | str | int | float | bool | None
)


@beartype
def _collect_ref_names(data: _RefData, *, ref_key: str) -> list[str]:
    """Recursively collect all ref name values from parsed data.

    Names are returned in first-use (document) order with duplicates
    removed at their first occurrence, matching the order
    :func:`literalizer.literalize` emits the ``bound_refs`` bindings.
    """
    match data:
        case dict():
            if len(data) == 1 and ref_key in data:
                name = data[ref_key]
                return [name] if isinstance(name, str) else []
            return [
                n
                for v in data.values()
                for n in _collect_ref_names(data=v, ref_key=ref_key)
            ]
        case list():
            return [
                n
                for item in data
                for n in _collect_ref_names(data=item, ref_key=ref_key)
            ]
        case _:
            return []


@beartype
def _parse_ref_input(
    *,
    input_format: literalizer.InputFormat,
    input_source: str,
) -> _RefData:
    """Parse *input_source* into raw data for ref-name collection.

    Mirrors the format dispatch in :func:`literalizer.parse_input` but
    yields plain Python containers so :func:`_collect_ref_names` can
    walk them structurally.
    """
    parsed: _RefData
    match input_format:
        case literalizer.InputFormat.JSON:
            parsed = json.loads(s=input_source)
        case literalizer.InputFormat.JSON5:
            parsed = pyjson5.decode(data=input_source)  # pylint: disable=no-member
        case literalizer.InputFormat.YAML:
            ruamel_yaml = _YAML()
            parsed = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
                stream=input_source,
            )
        case literalizer.InputFormat.TOML:
            parsed = tomllib.loads(input_source)
        case _ as unreachable:
            assert_never(unreachable)
    return parsed


@beartype
def run_literalize_ref_golden_case(
    *,
    config: LiteralizeRefCaseConfig,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    ref_case: literalizer.IdentifierCase | None,
    version: enum.Enum,
) -> None:
    """Run a literalize ``$ref`` golden-file case against *golden_name*.

    When *ref_case* is set, the ref identifier is spelled idiomatically
    for each language.  Each referenced identifier is supplied through
    ``bound_refs`` so a single :func:`literalizer.literalize` call
    emits the binding before its first use and the golden file is a
    complete unit that compiles, with per-language declaration
    sequencing.
    """
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    input_path = input_info.path
    input_source = input_path.read_text(encoding="utf-8")
    golden_path = make_golden_path(
        parent=input_path.parent,
        name=golden_name,
        extension=lang_cls.extension,
        lang_cls=lang_cls,
        version=version,
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    variable_form_obj: literalizer.NewVariable | None = wrap_variable_form()
    try:
        literalizer.literalize(
            source='{"_": "_"}',
            input_format=literalizer.InputFormat.JSON,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=True,
        )
    except VariableNameNotSupportedError:
        variable_form_obj = None
    explicit_sources = dict(config.ref_value_sources)
    raw_data = _parse_ref_input(
        input_format=input_info.input_format,
        input_source=input_source,
    )
    bound_refs_input: dict[str, _ValueInput] = {
        raw_name: json.loads(
            s=explicit_sources.get(raw_name, '{"_": "_"}'),
        )
        for raw_name in _collect_ref_names(
            data=raw_data,
            ref_key=config.ref_key,
        )
    }
    try:
        result = literalizer.literalize(
            source=input_source,
            input_format=input_info.input_format,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=True,
            ref_case=ref_case,
            bound_refs=bound_refs_input or None,
            ref_key=config.ref_key,
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} cannot represent this heterogeneous input",
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} rejected ref identifier: {exc.reason}"
        )
    file_regression.check(
        contents=result.code + "\n",
        encoding="utf-8",
        extension=lang_cls.extension,
        newline="",
        fullpath=golden_path,
    )
