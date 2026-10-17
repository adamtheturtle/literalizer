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

import json5_document
import jsonc_document
from beartype import beartype
from pydantic import TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML

import literalizer
from literalizer import ValueInput
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
    InvalidDictKeyError,
    NullInCollectionError,
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from literalizer.languages import Matlab
from tests.enum_members import enum_member_by_name
from tests.yaml_support import as_yaml_parser

from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    RefCaseSpec,
    RefConsumerSpec,
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
            error=NullInCollectionError,
            reason="cannot represent null in this collection",
            unlink=True,
        ),
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
        if config.ref_case_for(lang_cls=lang_cls) is None
        or config.ref_case_for(lang_cls=lang_cls)
        in lang_cls.supported_ref_cases
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
    dict[str, _RefData]
    | list[_RefData]
    | set[str | int | float | bool | None]
    | str
    | int
    | float
    | bool
    | None
)


@beartype
def collect_ref_names(data: _RefData, *, ref_key: str) -> list[str]:
    """Recursively collect all ref name values from parsed data.

    Names are returned in first-use (document) order with duplicates
    removed at their first occurrence, matching the order
    :func:`literalizer.literalize` emits the ``bound_refs`` bindings.
    """
    match data:
        case dict():
            if len(data) == 1 and ref_key in data:
                name = data[ref_key]
                if isinstance(name, str):
                    return [name]
                return []
            return [
                n
                for v in data.values()
                for n in collect_ref_names(data=v, ref_key=ref_key)
            ]
        case list():
            return [
                n
                for item in data
                for n in collect_ref_names(data=item, ref_key=ref_key)
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
    return TypeAdapter[_RefData](type=_RefData).validate_python(
        parsed,
        strict=True,
    )


@beartype
def _bound_ref_inputs(
    *,
    config: RefCaseSpec,
    raw_data: _RefData,
    lang_cls: literalizer.LanguageCls,
) -> dict[str, ValueInput]:
    """Prepare referenced bindings and the case's additional
    declarations.
    """
    collected_bound_refs_input: dict[str, ValueInput] = {}
    for entry_raw_name in collect_ref_names(
        data=raw_data, ref_key=config.ref_key
    ):
        effective_s = '{"_": "_"}'
        if lang_cls is Matlab:
            effective_s = '{"key": "value"}'
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
    return bound_refs_input


@beartype
def _ref_language_options(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
) -> literalizer.Language:
    """Apply the output modes explicitly selected by a reference case."""
    for name, enum_cls, choice in (
        (
            "variable_type_hints",
            lang_cls.VariableTypeHints,
            config.variable_type_hints,
        ),
        (
            "heterogeneous_strategy",
            lang_cls.HeterogeneousStrategies,
            config.heterogeneous_strategy,
        ),
        ("sequence_format", lang_cls.SequenceFormats, config.sequence_format),
        (
            "declaration_style",
            lang_cls.DeclarationStyles,
            config.declaration_style,
        ),
        ("json_type", lang_cls.JsonTypes, config.json_type),
        ("dict_format", lang_cls.DictFormats, config.dict_format),
    ):
        if choice is not None:
            spec = dataclasses.replace(
                spec,
                **{name: enum_member_by_name(enum_cls=enum_cls, name=choice)},
            )
    if config.default_sequence_element_type is not None:
        spec = dataclasses.replace(
            spec,
            default_sequence_element_type=config.default_sequence_element_type,
        )
    return spec


@beartype
def _compose_ref_value_check(
    *,
    source: str,
    spec: literalizer.Language,
    declarations: list[literalizer.LiteralizeResult],
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Assert a reference result against an independently rendered value.

    Expected data is rendered separately, after the operation under test,
    and never participates in its reference inference.
    """
    expected = literalizer.literalize(
        source=source,
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        variable_form=literalizer.NewVariable(
            name="expected_data", modifiers=frozenset()
        ),
    )
    assertion = literalizer.literalize_call(
        source='[[{"$ref": "my_data"}, {"$ref": "expected_data"}]]',
        target_function="assert_equal",
        parameter_names=("actual", "expected"),
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        ref_key="$ref",
    )
    helper = (
        Path(__file__).parent / "support" / f"assert_equal{spec.extension}"
    )
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=[*declarations, result, expected],
        call=assertion,
        extra_preamble=(helper.read_text(encoding="utf-8").rstrip(),),
    )


@beartype
def _compose_ref_consumer(
    *,
    consumer: RefConsumerSpec,
    spec: literalizer.Language,
    declarations: list[literalizer.LiteralizeResult],
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Compose a generated consumer around an external-reference
    result.
    """
    parameters = ("_arg",)
    target = tuple(consumer.target_function.split(sep="."))
    call = literalizer.literalize_call(
        source='{"$ref": "my_data"}',
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        target_function=consumer.target_function,
        parameter_names=parameters,
        per_element=False,
        ref_key="$ref",
    )
    if consumer.before_assignment:
        declarations.append(call)
    declarations.append(result)
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=declarations,
        call=call,
        extra_body_preamble=spec.format_call_stub(
            target, parameters, literalizer.StubReturn.VOID, ()
        ),
        extra_class_preamble=spec.format_call_class_scope_stub(
            target, parameters, literalizer.StubReturn.VOID, ()
        ),
        extra_preamble=spec.format_call_preamble_stub(
            target, parameters, literalizer.StubReturn.VOID, ()
        ),
    )


@beartype
def _compose_external_ref_fixture(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Compose caller declarations and optional generated checks."""
    declarations: list[literalizer.LiteralizeResult] = []
    for name, source in config.external_declarations.items():
        declaration_spec = spec
        style = config.external_declaration_styles.get(name)
        if style is not None:
            declaration_spec = dataclasses.replace(
                spec,
                declaration_style=enum_member_by_name(
                    enum_cls=lang_cls.DeclarationStyles, name=style
                ),
            )
        declarations.append(
            literalizer.literalize(
                source=source,
                input_format=literalizer.InputFormat.JSON,
                language=declaration_spec,
                variable_form=literalizer.NewVariable(
                    name=name, modifiers=frozenset()
                ),
            )
        )
    if config.expected_value_source is not None:
        return _compose_ref_value_check(
            source=config.expected_value_source,
            spec=spec,
            declarations=declarations,
            result=result,
        )
    if config.consumer is not None:
        return _compose_ref_consumer(
            consumer=config.consumer,
            spec=spec,
            declarations=declarations,
            result=result,
        )
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=declarations,
        call=result,
    )


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
    spec = _ref_language_options(config=config, lang_cls=lang_cls, spec=spec)
    variable_form_obj: literalizer.VariableForm | None = (
        config.resolved_variable_form()
    )
    if isinstance(variable_form_obj, literalizer.NewVariable):
        variable_form_obj = dataclasses.replace(
            variable_form_obj,
            modifiers=frozenset(
                enum_member_by_name(enum_cls=spec.modifiers, name=name)
                for name in config.variable_modifiers
            ),
        )
    try:
        _ = literalizer.literalize(
            source='{"key": "value"}',
            input_format=literalizer.InputFormat.JSON,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=len(config.external_declarations) == 0,
        )
    except VariableNameNotSupportedError:
        variable_form_obj = None
    raw_data = _parse_ref_input(
        input_format=input_info.input_format,
        input_source=input_source,
    )
    bound_refs_input = _bound_ref_inputs(
        config=config,
        raw_data=raw_data,
        lang_cls=lang_cls,
    )
    with GoldenSkips(
        policy=_REF_SKIPS,
        golden_path=golden_path,
        prefix=lang_cls.__name__,
        config=file_regression.request.config,
    ):
        effective_bound_refs = None
        if len(bound_refs_input) > 0 and config.external_declarations == {}:
            effective_bound_refs = bound_refs_input
        effective_ref_values = None
        if config.explicit_ref_value_sources is not None:
            effective_ref_values = {
                name: json.loads(s=source)
                for name, source in (config.explicit_ref_value_sources.items())
            }
        result = literalizer.literalize(
            source=input_source,
            input_format=input_info.input_format,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=len(config.external_declarations) == 0,
            ref_case=ref_case,
            bound_refs=(effective_bound_refs),
            ref_values=(effective_ref_values),
            ref_key=config.ref_key,
            pre_indent_level=config.pre_indent_level,
            collection_layout=literalizer.CollectionLayout(
                value=config.collection_layout
            ),
        )
    if len(config.external_declarations) > 0:
        result = _compose_external_ref_fixture(
            config=config,
            lang_cls=lang_cls,
            spec=spec,
            result=result,
        )
    check_golden(
        contents=result.code + "\n",
        extension=lang_cls.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )
