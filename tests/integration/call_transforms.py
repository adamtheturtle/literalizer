"""Compose native call expressions and their wrapper declarations."""

import dataclasses
import functools
from collections.abc import Callable, Sequence
from typing import Protocol, runtime_checkable

from beartype import beartype
from pydantic import TypeAdapter

import literalizer
from literalizer._enums import enum_payload
from literalizer._language import (
    CallStubDeclarations,
    CallSupport,
    IntegerCallStubResult,
    KeywordCallStyle,
    NullableObjectCallStubResult,
    ObjectCallStyle,
    PositionalCallStyle,
    RenderedCallStub,
    validate_call_parameter_names,
)
from literalizer._literalize import (
    assemble_call_expression,
    format_rendered_call_arguments,
)
from literalizer._parsing import parse_input
from literalizer._types import CallStubData
from literalizer.exceptions import (
    InvalidCallParameterNameError,
)

from .case_manifests import (
    CallCaseSpec,
    CallTransform,
    CallWrapperSpec,
)
from .language_specs import (
    sorted_languages,
)
from .parsed_values import ParsedValue


@beartype
def _statement_stub_targets(
    *, config: CallCaseSpec
) -> list[tuple[str, tuple[str, ...]]]:
    """Pair each statement target with its own parameter names."""
    targets = [
        (name, config.transform_stub_param_names)
        for name in config.transform_stub_names
    ]
    if config.followup_target_function is not None:
        targets.append(
            (config.followup_target_function, config.parameter_names)
        )
    return targets


@runtime_checkable
class _CallExpressionGroupLanguage(Protocol):
    """A producer whose value grouping differs from parentheses."""

    def group_call_expression(self, expression: str, /) -> str:
        """Retain an expression's comments inside a native value group."""
        ...


@beartype
def _parenthesized_call_group(expression: str, /) -> str:
    """Group an expression in the ordinary parenthesized form."""
    return f"({expression})"


@dataclasses.dataclass(frozen=True)
class GroupedCallTransform:
    """Retain operand metadata while grouping a generated expression."""

    body: CallTransform
    suffix: str
    outer: CallTransform | None
    group: Callable[[str], str]

    @property
    def uses_zipped(self) -> bool:
        """Report zip usage from both the body and its outer transform."""
        transforms = (
            (self.body,) if self.outer is None else (self.body, self.outer)
        )
        return any(transform.uses_zipped for transform in transforms)

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Apply native grouping before the optional outer transform."""
        expression = self.group(self.body(context)) + self.suffix
        if self.outer is None:
            return expression
        return self.outer(dataclasses.replace(context, call=expression))


@dataclasses.dataclass(frozen=True)
class LiteralArgumentsTransform:
    """An expression with native operands and a real call convention."""

    call: str
    suffix: str
    outer: CallTransform | None

    @property
    def uses_zipped(self) -> bool:
        """Retain operand metadata from the optional outer transform."""
        return self.outer is not None and self.outer.uses_zipped

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Insert native operands before applying the outer transform."""
        expression = self.call + self.suffix
        if self.outer is None:
            return expression
        return self.outer(dataclasses.replace(context, call=expression))


@beartype
def _wrapper_call_spec(*, spec: literalizer.Language) -> literalizer.Language:
    """Use a positional wrapper convention where the producer exposes
    it.
    """
    for member in spec.call_styles:
        if isinstance(
            enum_payload(member=member, payload_type=object),
            PositionalCallStyle,
        ):
            return dataclasses.replace(spec, call_style=member)
    return spec


@beartype
def _wrapper_parameter_names(
    *, spec: literalizer.Language, params: tuple[str, ...]
) -> tuple[str, ...]:
    """Retain scratch names unless the producer rejects their declarations."""
    try:
        validate_call_parameter_names(
            language=spec, names=params, reject_reserved=True
        )
    except InvalidCallParameterNameError:
        names = tuple(f"argument{index}" for index in range(len(params)))
        validate_call_parameter_names(
            language=spec, names=names, reject_reserved=True
        )
        return names
    return params


@beartype
def wrapper_call_declarations(
    *,
    spec: literalizer.Language,
    config: CallCaseSpec,
    bound_result_slots: frozenset[int],
) -> CallStubDeclarations:
    """Keep actual operand representations and wrapper calling conventions."""
    body: list[str | RenderedCallStub] = []
    class_scope: list[str] = []
    file_scope: list[str] = []
    wrapper = config.call_transform_wrapper
    for name, parameter_names in _statement_stub_targets(config=config):
        params = parameter_names
        wrapper_spec = spec
        arguments: Sequence[ParsedValue] = ()
        if name == config.followup_target_function:
            arguments = CallStubData(
                data=(),
                keyword_arguments=isinstance(
                    spec.call_style_config, KeywordCallStyle
                ),
                call_result_slots=bound_result_slots,
            )
        if wrapper is not None and name == wrapper.target:
            wrapper_spec = _wrapper_call_spec(spec=spec)
            params = _wrapper_parameter_names(spec=wrapper_spec, params=params)
            arguments = CallStubData(
                data=(),
                keyword_arguments=isinstance(
                    wrapper_spec.call_style_config, KeywordCallStyle
                ),
                call_result_slots=frozenset(
                    index
                    for index, role in enumerate(iterable=wrapper.arguments)
                    if role == "call"
                ),
            )
        parts = tuple(name.split(sep="."))
        body.extend(
            wrapper_spec.format_call_stub(
                parts, params, literalizer.StubReturn.VOID, arguments
            )
        )
        class_scope.extend(
            wrapper_spec.format_call_class_scope_stub(
                parts, params, literalizer.StubReturn.VOID, arguments
            )
        )
        file_scope.extend(
            wrapper_spec.format_call_preamble_stub(
                parts, params, literalizer.StubReturn.VOID, arguments
            )
        )
    return CallStubDeclarations(
        body=tuple(body),
        class_scope=tuple(class_scope),
        file_scope=tuple(file_scope),
    )


@beartype
def followup_result_slots(
    *,
    config: CallCaseSpec,
    input_format: literalizer.InputFormat,
) -> frozenset[int]:
    """Identify direct bound-result operands in the parsed follow-up
    call.
    """
    if config.followup_source is None or config.variable_form is None:
        return frozenset[int]()
    data = parse_input(
        source=config.followup_source, input_format=input_format
    ).data
    rows = data if config.per_element and isinstance(data, list) else [data]
    slots: set[int] = set()
    for row in rows:
        arguments = (
            row if config.per_element and isinstance(row, list) else [row]
        )
        slots.update(
            index
            for index, value in enumerate(iterable=arguments)
            if value == {config.ref_key: config.variable_form.name}
        )
    return frozenset(slots)


@dataclasses.dataclass(frozen=True)
class WrapperCallTransform:
    """A call producer retaining wrapper operands and declaration
    scopes.
    """

    spec: literalizer.Language
    config: CallCaseSpec
    wrapper: CallWrapperSpec
    zip_data: ParsedValue

    @property
    def uses_zipped(self) -> bool:
        """Report only the operand roles declared by the recipe."""
        outer = self.config.call_transform
        return "zipped" in self.wrapper.arguments or (
            outer is not None and outer.uses_zipped
        )

    @functools.cached_property
    def call_stub_declarations(self) -> CallStubDeclarations:
        """Supply the same native wrappers to the production file
        builder.
        """
        return wrapper_call_declarations(
            spec=self.spec,
            config=self.config,
            bound_result_slots=frozenset(),
        )

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Apply the real wrapper convention to rendered native
        operands.
        """
        wrapper = self.wrapper
        spec = _wrapper_call_spec(spec=self.spec)
        # Discovery admits only expression calls. Validate that boundary
        # once here instead of supporting malformed internal invocations.
        style = TypeAdapter(
            type=PositionalCallStyle | KeywordCallStyle | ObjectCallStyle
        ).validate_python(spec.call_style_config)
        operands: list[str] = []
        for role in wrapper.arguments:
            if role == "call":
                operands.append(context.call)
                continue
            operand = TypeAdapter(type=str).validate_python(context.zipped)
            value = self.zip_data
            if self.config.per_element:
                value = TypeAdapter(type=list[ParsedValue]).validate_python(
                    value
                )[context.index]
            operands.append(spec.format_call_arg(value, operand))
        args = format_rendered_call_arguments(
            formatted=operands,
            params=_wrapper_parameter_names(
                spec=spec, params=self.config.transform_stub_param_names
            ),
            style=style,
            allows_empty_call_parens=spec.allows_empty_call_parens,
        )
        expression = assemble_call_expression(
            target_function=spec.format_call_target(
                tuple(wrapper.target.split(sep="."))
            ),
            args_str=args,
            style=style,
        )
        if self.config.call_transform is not None:
            return self.config.call_transform(
                dataclasses.replace(context, call=expression)
            )
        return expression


@runtime_checkable
class _NativeSequenceExpressionLanguage(Protocol):
    """A producer of native lists independent of literal value
    carriers.
    """

    def format_sequence_expression(self, expressions: Sequence[str], /) -> str:
        """Build a sequence from arbitrary native expressions."""
        ...


@dataclasses.dataclass(frozen=True)
class SequenceCallTransform:
    """A one-element native sequence containing the call's actual
    result.
    """

    spec: literalizer.Language
    outer: CallTransform | None

    @property
    def uses_zipped(self) -> bool:
        """Preserve any operand use declared by an outer transform."""
        return self.outer is not None and self.outer.uses_zipped

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Let the literal producer choose its real sequence
        construction.
        """
        if isinstance(self.spec, _NativeSequenceExpressionLanguage):
            expression = self.spec.format_sequence_expression((context.call,))
        else:
            expression = self._literal_sequence(context.call)
        if self.outer is not None:
            return self.outer(dataclasses.replace(context, call=expression))
        return expression

    def _literal_sequence(self, call: str, /) -> str:
        """Use the native sequence delimiters for a result expression."""
        config = self.spec.sequence_format_config
        return self.spec.sequence_open([]) + call + config.close


@dataclasses.dataclass(frozen=True)
class IntegerResultCallTransform:
    """Retain arithmetic, inner comments, and outer operand metadata."""

    syntax: IntegerCallStubResult
    outer: CallTransform | None

    @property
    def uses_zipped(self) -> bool:
        """Preserve the outer transform's zipped-operand contract."""
        return self.outer is not None and self.outer.uses_zipped

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Add one using the integer result producer's native grammar."""
        expression = self.syntax.addition_template.format(
            left=context.call,
            right="1",
            comment=" " + self.syntax.comment_prefix + " inner",
        )
        if self.outer is not None:
            return self.outer(dataclasses.replace(context, call=expression))
        return expression


@dataclasses.dataclass(frozen=True)
class ConditionalCallTransform:
    """Retain both conditional arms, comments, and outer operand use."""

    template: str
    null_value: str
    comment_prefix: str
    indent: str
    outer: CallTransform | None

    @property
    def uses_zipped(self) -> bool:
        """Preserve the outer transform's zipped-operand contract."""
        return self.outer is not None and self.outer.uses_zipped

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Use the native conditional expression and null object value."""
        expression = self.template.format(
            call=context.call,
            null=self.null_value,
            inner_comment=" " + self.comment_prefix + " inner",
            trailing_comment=" " + self.comment_prefix + " trailing",
            indent=self.indent,
        )
        if self.outer is not None:
            return self.outer(dataclasses.replace(context, call=expression))
        return expression


@beartype
def _result_call_transform(
    *, spec: literalizer.Language, config: CallCaseSpec
) -> IntegerResultCallTransform | ConditionalCallTransform:
    """Build an admitted result expression from its producer metadata."""
    result = next(
        cls.call_stub_result
        for cls in sorted_languages()
        if cls.language_id == spec.language_id
    )
    # The manifest gates admit only producers of the required result type.
    if config.call_transform_add_one:
        syntax = TypeAdapter(type=IntegerCallStubResult).validate_python(
            result
        )
        return IntegerResultCallTransform(
            syntax=syntax, outer=config.call_transform
        )
    nullable = TypeAdapter(type=NullableObjectCallStubResult).validate_python(
        result
    )
    return ConditionalCallTransform(
        template=TypeAdapter(type=str).validate_python(
            nullable.conditional_template
        ),
        null_value=nullable.value,
        comment_prefix=nullable.comment_prefix,
        indent=spec.indent,
        outer=config.call_transform,
    )


@beartype
def call_transform_for_case(
    *, spec: literalizer.Language, config: CallCaseSpec
) -> Callable[[literalizer.CallContext], str] | None:
    """Compose the declared expression recipe with the actual call
    syntax.
    """
    if config.call_transform_wrapper is not None:
        zip_data: ParsedValue = None
        if (
            config.zip_source is not None
            and config.zip_input_format is not None
        ):
            zip_data = parse_input(
                source=config.zip_source, input_format=config.zip_input_format
            ).data
        return WrapperCallTransform(
            spec=spec,
            config=config,
            wrapper=config.call_transform_wrapper,
            zip_data=zip_data,
        )
    if (
        config.call_transform_add_one
        or config.call_transform_nullable_conditional
    ):
        return _result_call_transform(spec=spec, config=config)
    if config.call_transform_sequence:
        return SequenceCallTransform(spec=spec, outer=config.call_transform)
    style = spec.call_style_config
    if config.call_transform_arguments is not None and not isinstance(
        style, CallSupport
    ):
        native_arguments = config.call_transform_arguments
        args = format_rendered_call_arguments(
            formatted=list(native_arguments.arguments),
            params=config.parameter_names,
            style=style,
            allows_empty_call_parens=spec.allows_empty_call_parens,
        )
        target = spec.format_call_target(
            tuple(config.target_function.split(sep="."))
        )
        return LiteralArgumentsTransform(
            call=assemble_call_expression(
                target_function=target,
                args_str=args,
                style=style,
            ),
            suffix=native_arguments.suffix,
            outer=config.call_transform,
        )
    if config.call_transform_group is not None:
        group = (
            spec.group_call_expression
            if isinstance(spec, _CallExpressionGroupLanguage)
            else _parenthesized_call_group
        )
        return GroupedCallTransform(
            body=config.call_transform_group.body,
            suffix=config.call_transform_group.suffix,
            outer=config.call_transform,
            group=group,
        )
    return config.call_transform
