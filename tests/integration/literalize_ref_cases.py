"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

Each ``cases/literalize_ref_*`` directory declares in its own ``case.toml``
how it is driven through :func:`literalizer.literalize` with a ``ref_case``
set to the language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import dataclasses
import enum
import functools
import json
import tomllib
from pathlib import Path
from typing import assert_never

import json5
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML as _YAML

import literalizer
from literalizer._types import ValueInput  # noqa: TC001
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
    InvalidDictKeyError,
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from literalizer.languages import Matlab

from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    RefCaseSpec,
    case_input,
    ref_case_specs,
)
from .golden_checks import (
    GoldenSkips,
    SkipPolicy,
    SkipReason,
    check_golden,
)
from .language_specs import (
    make_golden_path,
    sorted_languages,
    with_per_fixture_module_name,
)

CASES_DIR = Path(__file__).parent / "cases"

# A ``$ref`` case is written once for every language, so an input a
# language cannot represent, or a ref identifier it will not spell,
# skips rather than fails.
_REF_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=HeterogeneousCollectionError,
            reason="cannot represent this heterogeneous input",
            unlink=True,
        ),
        SkipReason(
            error=UnrepresentableInputError,
            reason="cannot represent this heterogeneous input",
            unlink=True,
        ),
        SkipReason(
            error=CallArgNotSupportedError,
            reason="rejected ref identifier",
            unlink=True,
        ),
        SkipReason(
            error=InvalidDictKeyError,
            reason="cannot represent a dictionary key",
            unlink=True,
        ),
    ),
    suffix="",
)


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: RefCaseSpec
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
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=REF_OWNER)
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
        if config.ref_case_override is None
        or config.ref_case_override in lang_cls.supported_ref_cases
    ]


@functools.cache
@beartype
def discover_literalize_default_ref_cases() -> list[LiteralizeRefCase]:
    """Return default literalize-ref test cases for all languages."""
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in ref_case_specs(
            cases_dir=CASES_DIR,
            owner=REF_DEFAULT_OWNER,
        )
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
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
            parsed = json5.loads(s=input_source, allow_duplicate_keys=False)
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
    config: RefCaseSpec,
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
    if config.heterogeneous_strategy is not None:
        spec = dataclasses.replace(
            spec,
            heterogeneous_strategy=lang_cls.HeterogeneousStrategies[
                config.heterogeneous_strategy
            ],
        )
    variable_form_obj: literalizer.VariableForm | None = (
        config.resolved_variable_form()
    )
    try:
        literalizer.literalize(
            source='{"key": "value"}',
            input_format=literalizer.InputFormat.JSON,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=True,
        )
    except VariableNameNotSupportedError:
        variable_form_obj = None
    raw_data = _parse_ref_input(
        input_format=input_info.input_format,
        input_source=input_source,
    )
    bound_refs_input: dict[str, ValueInput] = {
        raw_name: json.loads(
            s=config.value_sources.get(
                raw_name,
                '{"key": "value"}' if lang_cls is Matlab else '{"_": "_"}',
            ),
        )
        for raw_name in _collect_ref_names(
            data=raw_data,
            ref_key=config.ref_key,
        )
    }
    bound_refs_input.update(
        {
            name: json.loads(s=source)
            for name, source in config.extra_ref_value_sources.items()
        },
    )
    with GoldenSkips(
        policy=_REF_SKIPS,
        golden_path=golden_path,
        prefix=lang_cls.__name__,
    ):
        result = literalizer.literalize(
            source=input_source,
            input_format=input_info.input_format,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=True,
            ref_case=ref_case,
            bound_refs=bound_refs_input or None,
            ref_values={
                name: json.loads(s=source)
                for name, source in config.explicit_ref_value_sources.items()
            }
            or None,
            ref_key=config.ref_key,
            pre_indent_level=config.pre_indent_level,
            collection_layout=literalizer.CollectionLayout(
                value=config.collection_layout
            ),
        )
    check_golden(
        contents=result.code + "\n",
        extension=lang_cls.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )
