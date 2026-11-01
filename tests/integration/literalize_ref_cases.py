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
from literalizer._language import CallStyle
from literalizer._literalize import (
    assemble_call_expression,
    format_rendered_call_arguments,
    materialize_value_input,
)
from literalizer._types import Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    InvalidDictKeyError,
    NullInCollectionError,
    ReservedVariableNameError,
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from tests.enum_members import enum_member_by_name
from tests.yaml_support import as_yaml_parser

from .call_cases import _call_stub_spec
from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    OwnerName,
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
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_golden_path,
    make_spec,
    reference_case_for_declaration_style,
    sorted_languages,
    with_per_fixture_module_name,
)
from .variant_cases import Variant, variants_for_axis

CASES_DIR = Path(__file__).parent / "cases"

# A ``$ref`` case is written once for every language, so an input a
# language cannot represent, or a ref identifier it will not spell,
# skips rather than fails.
_REF_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=CallsNotSupportedByLanguageError,
            reason="has no generated consumer call syntax",
            unlink=True,
        ),
        SkipReason(
            error=CallsNotSupportedByToolError,
            reason="cannot generate consumer calls",
            unlink=True,
        ),
        SkipReason(
            error=IncompatibleFormatsError,
            reason="reference input is incompatible with the selected formats",
            unlink=True,
        ),
        SkipReason(
            error=ReservedVariableNameError,
            reason="rejects a declared reference identifier",
            unlink=True,
        ),
        SkipReason(
            error=VariableNameNotSupportedError,
            reason="cannot declare the reference binding",
            unlink=True,
        ),
        SkipReason(
            error=ExistingVariableNotSelfContainedError,
            reason=(
                "cannot wrap an assignment without its destination declaration"
            ),
            unlink=True,
        ),
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
        if not config.variant_only
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
        if config.variable_form != "both"
        or bool(find_redefinition_styles(spec=make_spec(lang_cls=lang_cls)))
        if config.ref_case_for(lang_cls=lang_cls) is None
        or config.ref_case_for(lang_cls=lang_cls)
        in lang_cls.supported_ref_cases
    ]


@dataclasses.dataclass(frozen=True)
class LiteralizeRefVariantCase:
    """A reference scenario paired with an effective language variant."""

    config: RefCaseSpec
    variant: Variant
    ref_case: literalizer.IdentifierCase | None

    @property
    def golden_name(self) -> str:
        """Retain whether the public API receives an explicit ref case."""
        suffix = "ref_default" if self.ref_case is None else "ref"
        return f"{self.variant.name}_{suffix}"


@beartype
def _reference_variant_case(
    *, config: RefCaseSpec, variant: Variant, owner: OwnerName
) -> LiteralizeRefVariantCase | None:
    """Retain selected options and reject unsupported reference styles."""
    lang_cls = variant.lang_cls
    if not config.admits_language(lang_cls=lang_cls):
        return None
    ref_case = config.ref_case_for(lang_cls=lang_cls)
    if ref_case is not None and ref_case not in lang_cls.supported_ref_cases:
        return None
    spec = _ref_language_options(
        config=config, lang_cls=lang_cls, spec=variant.spec
    )
    if (
        config.variable_form == "both"
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        return None
    # A selected declaration variant is an explicit choice. The base
    # suite's automatic mutable-style fallback must not relabel it.
    names = language_metadata(
        language_id=lang_cls.language_id
    ).variants.declaration_style_variable_names
    reference_case = config.ref_case_for(lang_cls=lang_cls)
    if owner == REF_DEFAULT_OWNER:
        reference_case = None
    elif reference_case is None:
        reference_case = reference_case_for_declaration_style(
            lang_cls=lang_cls, spec=spec
        )
    selected_config = config.model_copy(
        update={
            "declaration_style": spec.declaration_style.name,
            "variable_name": names.get(
                spec.declaration_style.name, config.variable_name
            ),
            "ref_case_override": reference_case,
        }
    )
    return LiteralizeRefVariantCase(
        config=selected_config,
        variant=dataclasses.replace(variant, spec=spec),
        ref_case=reference_case,
    )


@functools.cache
@beartype
def build_literalize_ref_variant_cases() -> list[LiteralizeRefVariantCase]:
    """Discover reference variants through the existing typed axis
    plans.
    """
    return [
        case
        for owner in (REF_OWNER, REF_DEFAULT_OWNER)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        for entry in config.variants
        for variant in variants_for_axis(axis_key=entry.axis)
        if (
            case := _reference_variant_case(
                config=config, variant=variant, owner=owner
            )
        )
        is not None
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
        if not config.variant_only
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
def ref_language_versions(
    *, config: RefCaseSpec, lang_cls: literalizer.LanguageCls
) -> tuple[enum.Enum, ...]:
    """Return each effective target version once after applying
    options.
    """
    return tuple(
        dict.fromkeys(
            _ref_language_options(
                config=config,
                lang_cls=lang_cls,
                spec=make_spec(lang_cls=lang_cls, language_version=version),
            ).language_version
            for version in lang_cls.VersionFormats
        )
    )


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
    argument_data: ValueInput,
    expression: bool,
) -> literalizer.LiteralizeResult:
    """Compose a generated consumer around an external-reference
    result.
    """
    stub_data = materialize_value_input(
        value=argument_data, argument_name="consumer value"
    )
    parameters = ("arg_value",)
    target = tuple(consumer.target_function.split(sep="."))
    stub_spec = (
        _call_stub_spec(spec=spec, argument_values=([stub_data],))
        if expression
        else spec
    )

    def consume_expression(_context: literalizer.CallContext) -> str:
        """Splice the actual unwrapped result into a native caller."""
        style = TypeAdapter[CallStyle](type=CallStyle).validate_python(
            spec.call_style_config
        )
        arguments = format_rendered_call_arguments(
            formatted=[result.code],
            params=parameters,
            style=style,
            allows_empty_call_parens=True,
        )
        return assemble_call_expression(
            target_function=consumer.target_function,
            args_str=arguments,
            style=style,
        )

    call = literalizer.literalize_call(
        source='{"$ref": "my_data"}',
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        target_function=consumer.target_function,
        parameter_names=parameters,
        per_element=False,
        ref_key="$ref",
        call_transform=consume_expression if expression else None,
    )
    if expression:
        call = dataclasses.replace(
            result,
            declaration_code=call.declaration_code,
            pre_declaration_comments=call.pre_declaration_comments,
            is_call_statement=True,
            sections=(),
        )
    else:
        if consumer.before_assignment:
            declarations.append(call)
        declarations.append(result)
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=declarations,
        call=call,
        extra_body_preamble=stub_spec.format_call_stub(
            target, parameters, literalizer.StubReturn.VOID, ([stub_data],)
        ),
        extra_class_preamble=stub_spec.format_call_class_scope_stub(
            target, parameters, literalizer.StubReturn.VOID, ([stub_data],)
        ),
        extra_preamble=stub_spec.format_call_preamble_stub(
            target, parameters, literalizer.StubReturn.VOID, ([stub_data],)
        ),
    )


@beartype
def _external_result_value(*, source: Value, config: RefCaseSpec) -> Value:
    """Resolve caller values only for the independent consumer's signature."""
    if isinstance(source, dict):
        name = source.get(config.ref_key)
        if len(source) == 1 and isinstance(name, str):
            return TypeAdapter[Value](type=Value).validate_python(
                json.loads(s=config.external_declarations[name])
            )
        return {
            key: _external_result_value(source=value, config=config)
            for key, value in source.items()
        }
    if isinstance(source, list):
        return [
            _external_result_value(source=value, config=config)
            for value in source
        ]
    return source


@beartype
def external_assignment_spec(
    *, spec: literalizer.Language, config: RefCaseSpec, raw_data: _RefData
) -> literalizer.Language:
    """Use a length-independent sequence for a caller's changing-size
    binding.

    The source and destination values remain unchanged. A fixed-arity
    tuple cannot model reassignment between their different native types.
    """
    if (
        config.variable_form != "existing"
        or "my_data" not in config.external_declarations
    ):
        return spec
    initial = TypeAdapter[Value](type=Value).validate_python(
        json.loads(s=config.external_declarations["my_data"])
    )
    assigned = _external_result_value(
        source=TypeAdapter[Value](type=Value).validate_python(raw_data),
        config=config,
    )
    if not (
        isinstance(initial, list)
        and isinstance(assigned, list)
        and len(initial) != len(assigned)
        and spec.sequence_format_config.length_is_part_of_type
    ):
        return spec
    if config.sequence_format is None:
        for sequence_format in spec.sequence_formats:
            candidate = dataclasses.replace(
                spec, sequence_format=sequence_format
            )
            if not candidate.sequence_format_config.length_is_part_of_type:
                return candidate
    msg = "the selected sequence type cannot change length on reassignment"
    raise UnrepresentableInputError(msg)


@beartype
def _with_caller_binding_signature(
    *,
    config: RefCaseSpec,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
    raw_data: _RefData,
) -> literalizer.LiteralizeResult:
    """Let the caller annotate a new equation without supplying API
    hints.
    """
    if (
        config.variable_form == "existing"
        and config.variable_name not in config.external_declarations
    ):
        value = _external_result_value(
            source=TypeAdapter[Value](type=Value).validate_python(raw_data),
            config=config,
        )
        placeholder = "caller_value"
        assignment = spec.format_variable_assignment(
            config.variable_name, placeholder, value
        )
        declaration = spec.format_variable_declaration(
            config.variable_name, placeholder, value, frozenset()
        )
        if declaration.endswith("\n" + assignment):
            signature = declaration.removesuffix(assignment)
            result = dataclasses.replace(
                result,
                declaration_code=(
                    signature + result.declaration_code.removeprefix(signature)
                ),
            )
    return result


@beartype
def _compose_external_ref_fixture(
    *,
    config: RefCaseSpec,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
    raw_data: _RefData,
) -> literalizer.LiteralizeResult:
    """Compose caller declarations and optional generated checks."""
    result = _with_caller_binding_signature(
        config=config, spec=spec, result=result, raw_data=raw_data
    )
    declarations: list[literalizer.LiteralizeResult] = []
    for name, source in config.external_declarations.items():
        declaration_spec = spec
        if config.variable_form == "existing" and name == "my_data":
            styles = find_redefinition_styles(spec=spec)
            if len(styles) == 0:
                msg = (
                    "the external destination needs a reassignable declaration"
                )
                raise UnrepresentableInputError(msg)
            if styles[0] is not spec.declaration_style:
                declaration_spec = dataclasses.replace(
                    spec, declaration_style=styles[0]
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
    result = dataclasses.replace(
        result, preamble=(*config.caller_preamble, *result.preamble)
    )
    declarations = [
        dataclasses.replace(
            declaration,
            preamble=(*config.caller_preamble, *declaration.preamble),
        )
        for declaration in declarations
    ]
    assertion_helper = (
        Path(__file__).parent / "support" / f"assert_equal{spec.extension}"
    )
    if config.expected_value_source is not None and assertion_helper.is_file():
        return _compose_ref_value_check(
            source=config.expected_value_source,
            spec=spec,
            declarations=declarations,
            result=result,
        )
    consumer = config.consumer
    if consumer is None:
        consumer = RefConsumerSpec(target_function="consume_widget")
    return _compose_ref_consumer(
        consumer=consumer,
        expression=config.variable_form == "none",
        spec=spec,
        declarations=declarations,
        result=result,
        argument_data=_external_result_value(
            source=TypeAdapter[Value](type=Value).validate_python(raw_data),
            config=config,
        ),
    )


@beartype
def _ref_fixture_contents(
    *,
    code: str,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    ref_case: literalizer.IdentifierCase | None,
) -> str:
    """Keep explicitly requested reference spelling in compiler
    fixtures.
    """
    native_case = reference_case_for_declaration_style(
        lang_cls=lang_cls, spec=spec
    )
    preamble = (
        language_metadata(
            language_id=lang_cls.language_id
        ).golden.intentional_identifier_preamble
        if ref_case is not None and ref_case is not native_case
        else ()
    )
    return "\n".join((*preamble, code, ""))


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
    spec = _ref_language_options(config=config, lang_cls=lang_cls, spec=spec)
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    input_path = input_info.path
    input_source = input_path.read_text(encoding="utf-8")
    golden_path = make_golden_path(
        parent=input_path.parent,
        name=config.golden_name(name=golden_name),
        extension=lang_cls.extension,
        lang_cls=lang_cls,
        version=version,
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    if (
        config.variable_form == "both"
        and config.declaration_style is None
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        spec = dataclasses.replace(
            spec, declaration_style=find_redefinition_styles(spec=spec)[0]
        )
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
    with GoldenSkips(
        policy=_REF_SKIPS,
        golden_path=golden_path,
        prefix=lang_cls.__name__,
        config=file_regression.request.config,
    ):
        try:
            _ = literalizer.literalize(
                source='{"key": "value"}',
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=variable_form_obj,
                wrap_in_file=(
                    len(config.external_declarations) == 0
                    and config.consumer is None
                ),
            )
        except VariableNameNotSupportedError:
            variable_form_obj = None
        raw_data = _parse_ref_input(
            input_format=input_info.input_format,
            input_source=input_source,
        )
        spec = external_assignment_spec(
            spec=spec, config=config, raw_data=raw_data
        )
        bound_refs_input = _bound_ref_inputs(
            config=config,
            raw_data=raw_data,
            lang_cls=lang_cls,
        )
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
            wrap_in_file=(
                len(config.external_declarations) == 0
                and config.consumer is None
            ),
            ref_case=ref_case,
            bound_refs=(effective_bound_refs),
            ref_values=(effective_ref_values),
            ref_key=config.ref_key,
            pre_indent_level=config.pre_indent_level,
            collection_layout=literalizer.CollectionLayout(
                value=config.collection_layout
            ),
        )
        if (
            len(config.external_declarations) > 0
            or config.consumer is not None
        ):
            result = _compose_external_ref_fixture(
                config=config,
                spec=spec,
                result=result,
                raw_data=raw_data,
            )
    check_golden(
        contents=_ref_fixture_contents(
            code=result.code,
            spec=spec,
            lang_cls=lang_cls,
            ref_case=ref_case,
        ),
        extension=lang_cls.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )
