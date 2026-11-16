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

from .call_stubs import call_stub_spec
from .case_manifests import (
    ExternalRefContext,
    RefAssignmentConsumerSpec,
    RefCaseSpec,
    RefConsumerSpec,
    RefExpressionContext,
    RefValueCheckSpec,
)
from .golden_checks import fixture_contents
from .language_specs import (
    find_redefinition_styles,
    reference_case_for_declaration_style,
)
from .reference_inputs import RefData


@beartype
def _compose_ref_value_check(
    *,
    context: ExternalRefContext,
    consumer: RefValueCheckSpec,
    spec: literalizer.Language,
    declarations: list[literalizer.LiteralizeResult],
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Assert a reference result against an independently rendered value.

    Expected data is rendered separately, after the operation under test,
    and never participates in its reference inference.
    """
    if "my_data" in context.declarations:
        initial_source = context.declarations["my_data"]
        initial_check = literalizer.literalize_call(
            source=f'[[{{"$ref": "my_data"}}, {initial_source}]]',
            target_function="assert_equal",
            parameter_names=("actual", "expected"),
            input_format=literalizer.InputFormat.JSON,
            language=spec,
            ref_key="$ref",
        )
        declarations.append(initial_check)
    expected = literalizer.literalize(
        source=consumer.expected_source,
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
    consumer: RefConsumerSpec | RefAssignmentConsumerSpec,
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
        if isinstance(consumer, RefAssignmentConsumerSpec):
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
def _external_result_value(
    *, source: Value, context: ExternalRefContext, config: RefCaseSpec
) -> Value:
    """Resolve caller values only for the independent consumer's signature."""
    if isinstance(source, dict):
        name = source.get(config.ref_key)
        if len(source) == 1 and isinstance(name, str):
            return TypeAdapter[Value](type=Value).validate_python(
                json.loads(s=context.declarations[name])
            )
        return {
            key: _external_result_value(
                source=value, config=config, context=context
            )
            for key, value in source.items()
        }
    if isinstance(source, list):
        return [
            _external_result_value(
                source=value, config=config, context=context
            )
            for value in source
        ]
    return source


@beartype
def external_assignment_spec(
    *,
    spec: literalizer.Language,
    config: RefCaseSpec,
    context: ExternalRefContext,
    raw_data: RefData,
) -> literalizer.Language:
    """Use a length-independent sequence for a caller's changing-size
    binding.

    The source and destination values remain unchanged. A fixed-arity
    tuple cannot model reassignment between their different native types.
    """
    if (
        config.variable_form != "existing"
        or "my_data" not in context.declarations
    ):
        return spec
    initial = TypeAdapter[Value](type=Value).validate_python(
        json.loads(s=context.declarations["my_data"])
    )
    assigned = _external_result_value(
        source=TypeAdapter[Value](type=Value).validate_python(raw_data),
        config=config,
        context=context,
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
    context: ExternalRefContext,
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
        and config.variable_name not in context.declarations
    ):
        value = _external_result_value(
            source=TypeAdapter[Value](type=Value).validate_python(raw_data),
            config=config,
            context=context,
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
    context: ExternalRefContext,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
    raw_data: RefData,
) -> literalizer.LiteralizeResult:
    """Compose caller declarations and optional generated checks."""
    result = _with_caller_binding_signature(
        config=config,
        context=context,
        spec=spec,
        result=result,
        raw_data=raw_data,
    )
    declarations: list[literalizer.LiteralizeResult] = []
    for name, source in context.declarations.items():
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
        declaration = literalizer.literalize(
            source=source,
            input_format=literalizer.InputFormat.JSON,
            language=declaration_spec,
            variable_form=literalizer.NewVariable(
                name=name, modifiers=frozenset()
            ),
        )
        declarations.append(
            dataclasses.replace(
                declaration,
                preamble=(*context.caller_preamble, *declaration.preamble),
            )
        )
    result = dataclasses.replace(
        result, preamble=(*context.caller_preamble, *result.preamble)
    )
    assertion_helper = (
        Path(__file__).parent / "support" / f"assert_equal{spec.extension}"
    )
    consumer = context.consumer
    if isinstance(consumer, RefValueCheckSpec) and assertion_helper.is_file():
        return _compose_ref_value_check(
            context=context,
            consumer=consumer,
            spec=spec,
            declarations=declarations,
            result=result,
        )
    if isinstance(consumer, RefValueCheckSpec):
        if (
            config.variable_form == "existing"
            and "my_data" in context.declarations
        ):
            consumer = RefAssignmentConsumerSpec(
                kind="assignment", target_function="consume_widget"
            )
        else:
            consumer = RefConsumerSpec(
                kind="call", target_function="consume_widget"
            )
    return _compose_ref_consumer(
        consumer=consumer,
        expression=config.variable_form == "none",
        spec=spec,
        declarations=declarations,
        result=result,
        argument_data=_external_result_value(
            source=TypeAdapter[Value](type=Value).validate_python(raw_data),
            config=config,
            context=context,
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
    return fixture_contents(
        code=code,
        language_id=spec.language_id,
        intentional_identifier=ref_case is not None
        and ref_case is not native_case,
    )


@beartype
def compose_ref_expression_fixture(
    *,
    context: RefExpressionContext,
    spec: literalizer.Language,
    result: literalizer.LiteralizeResult,
) -> literalizer.LiteralizeResult:
    """Pass the rendered expression to its explicitly selected
    consumer.
    """
    return _compose_ref_consumer(
        consumer=context.consumer,
        expression=True,
        spec=spec,
        declarations=[],
        result=result,
        argument_data=result.source_data,
    )
