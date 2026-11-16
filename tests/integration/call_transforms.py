"""Compose native call expressions and their wrapper declarations."""

import dataclasses
import functools
from collections.abc import Callable, Sequence
from typing import Protocol, assert_never, runtime_checkable

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
    CallAddOneSpec,
    CallArgumentsSpec,
    CallCaseSpec,
    CallConditionalSpec,
    CallGroupSpec,
    CallSequenceSpec,
    CallStubRecipeSpec,
    CallTemplateSpec,
    CallTransform,
    CallWrapperSpec,
    FollowupCallSpec,
)
from .language_specs import (
    sorted_languages,
)
from .parsed_values import ParsedValue


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


@beartype
def _apply_outer_transform(
    *,
    context: literalizer.CallContext,
    expression: str,
    outer: CallTransform | None,
) -> str:
    """Pass a native expression through the optional outer recipe."""
    if outer is None:
        return expression
    return outer(dataclasses.replace(context, call=expression))


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
        return _apply_outer_transform(
            context=context, expression=expression, outer=self.outer
        )


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
        return _apply_outer_transform(
            context=context, expression=expression, outer=self.outer
        )


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
def transform_stub_targets(
    *, config: CallCaseSpec
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Read wrapper declarations from the selected recipe's own
    operands.
    """
    match config.transform:
        case CallWrapperSpec() as wrapper:
            return (
                (
                    wrapper.target,
                    tuple(operand.parameter for operand in wrapper.arguments),
                ),
            )
        case CallStubRecipeSpec() as recipe:
            return tuple(
                (name, recipe.stub_param_names) for name in recipe.stub_names
            )
        case None:
            return ()


@beartype
def wrapper_call_declarations(
    *,
    spec: literalizer.Language,
    config: CallCaseSpec,
    followup: FollowupCallSpec | None,
    bound_result_slots: frozenset[int],
) -> CallStubDeclarations:
    """Keep actual operand representations and wrapper calling conventions."""
    body: list[str | RenderedCallStub] = []
    class_scope: list[str] = []
    file_scope: list[str] = []
    wrapper = (
        config.transform
        if isinstance(config.transform, CallWrapperSpec)
        else None
    )
    targets = list(transform_stub_targets(config=config))
    followup_target = None if followup is None else followup.target_function
    if followup_target is not None:
        targets.append((followup_target, config.parameter_names))
    for name, parameter_names in targets:
        params = parameter_names
        wrapper_spec = spec
        arguments: Sequence[ParsedValue] = ()
        if name == followup_target:
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
                    if role.role == "call"
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
    followup: FollowupCallSpec | None,
    input_format: literalizer.InputFormat,
) -> frozenset[int]:
    """Identify direct bound-result operands in the parsed follow-up
    call.
    """
    if followup is None or config.variable_form is None:
        return frozenset[int]()
    data = parse_input(source=followup.source, input_format=input_format).data
    rows = data if config.per_element and isinstance(data, list) else [data]
    return frozenset(
        index
        for row in rows
        for index, value in enumerate(
            iterable=row
            if config.per_element and isinstance(row, list)
            else [row]
        )
        if value == {config.ref_key: config.variable_form.name}
    )


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
        outer = self.wrapper.outer
        return any(
            operand.role == "zipped" for operand in self.wrapper.arguments
        ) or (outer is not None and outer.uses_zipped)

    @functools.cached_property
    def call_stub_declarations(self) -> CallStubDeclarations:
        """Supply the same native wrappers to the production file
        builder.
        """
        return wrapper_call_declarations(
            spec=self.spec,
            config=self.config,
            followup=None,
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
            if role.role == "call":
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
                spec=spec,
                params=tuple(
                    operand.parameter for operand in wrapper.arguments
                ),
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
        return _apply_outer_transform(
            context=context,
            expression=expression,
            outer=self.wrapper.outer,
        )


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
        return _apply_outer_transform(
            context=context, expression=expression, outer=self.outer
        )

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
        return _apply_outer_transform(
            context=context, expression=expression, outer=self.outer
        )


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
        return _apply_outer_transform(
            context=context, expression=expression, outer=self.outer
        )


@beartype
def _result_call_transform(
    *, spec: literalizer.Language, recipe: CallAddOneSpec | CallConditionalSpec
) -> IntegerResultCallTransform | ConditionalCallTransform:
    """Build an admitted result expression from its producer metadata."""
    result = next(
        cls.call_stub_result
        for cls in sorted_languages()
        if cls.language_id == spec.language_id
    )
    # The manifest gates admit only producers of the required result type.
    if isinstance(recipe, CallAddOneSpec):
        syntax = TypeAdapter(type=IntegerCallStubResult).validate_python(
            result
        )
        return IntegerResultCallTransform(syntax=syntax, outer=recipe.outer)
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
        outer=recipe.outer,
    )


@beartype
def _wrapper_transform(
    *,
    spec: literalizer.Language,
    config: CallCaseSpec,
    recipe: CallWrapperSpec,
) -> WrapperCallTransform:
    """Parse the independent zip input for a native wrapper recipe."""
    zip_data: ParsedValue = None
    if config.zip_source is not None and config.zip_input_format is not None:
        zip_data = parse_input(
            source=config.zip_source,
            input_format=config.zip_input_format,
        ).data
    return WrapperCallTransform(
        spec=spec, config=config, wrapper=recipe, zip_data=zip_data
    )


@beartype
def _arguments_transform(
    *,
    spec: literalizer.Language,
    config: CallCaseSpec,
    recipe: CallArgumentsSpec,
) -> LiteralArgumentsTransform | CallTransform | None:
    """Render lexical operands with the selected native calling convention."""
    style = spec.call_style_config
    if isinstance(style, CallSupport):
        return recipe.outer
    args = format_rendered_call_arguments(
        formatted=list(recipe.arguments),
        params=config.parameter_names,
        style=style,
        allows_empty_call_parens=spec.allows_empty_call_parens,
    )
    target = spec.format_call_target(
        tuple(config.target_function.split(sep="."))
    )
    return LiteralArgumentsTransform(
        call=assemble_call_expression(
            target_function=target, args_str=args, style=style
        ),
        suffix=recipe.suffix,
        outer=recipe.outer,
    )


@beartype
def call_transform_for_case(
    *, spec: literalizer.Language, config: CallCaseSpec
) -> Callable[[literalizer.CallContext], str] | None:
    """Execute the selected recipe without reconstructing its mode."""
    match config.transform:
        case None | CallTemplateSpec() as recipe:
            return None if recipe is None else recipe.template
        case CallWrapperSpec() as recipe:
            return _wrapper_transform(spec=spec, config=config, recipe=recipe)
        case (CallAddOneSpec() | CallConditionalSpec()) as recipe:
            return _result_call_transform(spec=spec, recipe=recipe)
        case CallSequenceSpec() as recipe:
            return SequenceCallTransform(spec=spec, outer=recipe.outer)
        case CallArgumentsSpec() as recipe:
            return _arguments_transform(
                spec=spec, config=config, recipe=recipe
            )
        case CallGroupSpec() as recipe:
            group = (
                spec.group_call_expression
                if isinstance(spec, _CallExpressionGroupLanguage)
                else _parenthesized_call_group
            )
            return GroupedCallTransform(
                body=recipe.body,
                suffix=recipe.suffix,
                outer=recipe.outer,
                group=group,
            )
        case _ as unreachable:
            assert_never(unreachable)
