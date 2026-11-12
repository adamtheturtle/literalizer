"""Compose native consumers around rendered reference results."""

import dataclasses
import json
from pathlib import Path

from beartype import beartype
from pydantic import TypeAdapter

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
    UnrepresentableInputError,
)

from .call_cases import call_stub_spec
from .case_manifests import (
    RefCaseSpec,
    RefConsumerSpec,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    reference_case_for_declaration_style,
)
from .reference_inputs import RefData


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
        call_stub_spec(spec=spec, argument_values=([stub_data],))
        if expression
        else spec
    )

    if expression:
        spec.validate_call_arg(stub_data)
        style = TypeAdapter[CallStyle](type=CallStyle).validate_python(
            spec.call_style_config
        )
        arguments = format_rendered_call_arguments(
            formatted=[stub_spec.format_call_arg(stub_data, result.bare_code)],
            params=parameters,
            style=style,
            allows_empty_call_parens=True,
        )
        call_expression = assemble_call_expression(
            target_function=stub_spec.format_call_target(target),
            args_str=arguments,
            style=style,
        )
        call = dataclasses.replace(
            result,
            declaration_code=spec.format_call_statement(
                call_expression + spec.statement_terminator
            ),
            pre_declaration_comments=(),
            is_call_statement=True,
            sections=(),
        )
    else:
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
    *, spec: literalizer.Language, config: RefCaseSpec, raw_data: RefData
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
    raw_data: RefData,
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
def compose_external_ref_fixture(
    *,
    config: RefCaseSpec,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
    raw_data: RefData,
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
def ref_fixture_contents(
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
