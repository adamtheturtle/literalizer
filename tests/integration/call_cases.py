"""``literalize_call`` golden-file case discovery and runner.

Each ``cases/call_*`` directory declares in its own ``case.toml`` how it
is driven through :func:`literalizer.literalize_call`; this module turns
those declarations into per-language cases.  The runner
(``run_call_golden_case``) is shared by ``test_call_golden_file`` and
``test_call_variant_golden_file``.
"""

import dataclasses
import enum
import functools
import json
import re
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Protocol, runtime_checkable

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._enums import enum_payload
from literalizer._language import (
    CallParameterShadowing,
    CallStubDeclarations,
    CallSupport,
    IntegerCallStubResult,
    KeywordCallStyle,
    NullableObjectCallStubResult,
    PositionalCallStyle,
    RenderedCallStub,
    is_reserved_identifier,
    validate_call_parameter_names,
)
from literalizer._literalize import (
    assemble_call_expression,
    call_result_discard_formatter,
    format_rendered_call_arguments,
)
from literalizer._parsing import parse_input
from literalizer._types import CallStubData
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    DottedCallTargetNotSupportedError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    InvalidCallParameterNameError,
    InvalidCallTargetError,
    InvalidNewVariableNameError,
    ReservedVariableNameError,
    UnrepresentableInputError,
    UnsupportedCallShapeError,
    VariableNameNotSupportedError,
)
from tests.enum_members import enum_member_by_name

from .case_inputs import CaseInput
from .case_manifests import (
    CallCaseSpec,
    CallTransform,
    CallWrapperSpec,
    call_case_specs,
    case_input,
)
from .golden_checks import (
    GoldenSkips,
    SkipPolicy,
    SkipReason,
    check_golden,
    skip_golden,
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
from .parsed_values import ParsedValue

CASES_DIR = Path(__file__).parent / "cases"

# A wrapped call is rendered straight to its golden, so the only thing
# that can stop it is the language refusing one of the call's arguments.
_WRAP_IN_FILE_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=HeterogeneousCollectionError,
            reason="cannot represent this heterogeneous input",
            unlink=True,
        ),
        SkipReason(
            error=UnrepresentableInputError,
            reason="cannot represent these call arguments",
            unlink=True,
        ),
        SkipReason(
            error=IncompatibleFormatsError,
            reason="cannot combine these call and representation options",
            unlink=True,
        ),
        SkipReason(
            error=ReservedVariableNameError,
            reason="rejects a declared reference identifier",
            unlink=True,
        ),
        SkipReason(
            error=CallArgNotSupportedError,
            reason="rejected call arg",
            unlink=True,
        ),
        SkipReason(
            error=ExistingVariableNotSelfContainedError,
            reason=(
                "binds a call result by assignment to a name a whole "
                "file never declares"
            ),
            unlink=True,
        ),
    ),
    suffix="",
)

# A case that binds its refs to declarations asks more of a language
# than the call alone: it must name the declared variables, represent
# their values, and spell whatever target the case calls.
_DECLARATION_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=IncompatibleFormatsError,
            reason="cannot combine these call and representation options",
            unlink=True,
        ),
        SkipReason(
            error=ReservedVariableNameError,
            reason="rejects a declared reference identifier",
            unlink=True,
        ),
        SkipReason(
            error=VariableNameNotSupportedError,
            reason=(
                "does not support variable-name wrapping for ref declarations"
            ),
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
            error=DottedCallTargetNotSupportedError,
            reason="does not support dotted call targets",
            unlink=True,
        ),
        SkipReason(
            error=CallArgNotSupportedError,
            reason="rejected call arg",
            unlink=True,
        ),
    ),
    suffix="",
)

# The typed preamble stub restates the call's argument types, which a
# language with no type for a heterogeneous collection cannot write even
# where the call itself renders.
_PREAMBLE_STUB_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=HeterogeneousCollectionError,
            reason=(
                "cannot represent this heterogeneous input in its typed "
                "call stub"
            ),
            unlink=True,
        ),
    ),
    suffix="",
)


@dataclasses.dataclass(frozen=True)
class CallCase:
    """A parameterized call-style golden-file test case."""

    config: CallCaseSpec
    lang_cls: literalizer.LanguageCls
    expected_exception: type[Exception] | None


_SUBSTITUTION_CALL_STYLES = (
    literalizer.PositionalCallStyle,
    literalizer.KeywordCallStyle,
    literalizer.ObjectCallStyle,
)


@beartype
def _call_transform_style_unsupported(
    *,
    spec: literalizer.Language,
    config: CallCaseSpec,
) -> bool:
    """Mirror ``_validate_call_preconditions``'s rejection of
    ``call_transform`` for non-substitution call styles.

    ``call_transform`` is only supported when the effective call style
    is positional, keyword, or object.  When ``call_style_type`` is set
    the test pins that style; otherwise the language's default
    (first-listed) style applies.
    """
    if not config.has_call_transform:
        return False
    if config.call_style_type is not None:
        return not issubclass(
            config.call_style_type, _SUBSTITUTION_CALL_STYLES
        )
    default_style = spec.call_style_config
    return not isinstance(default_style, _SUBSTITUTION_CALL_STYLES)


@beartype
def _wrapper_capability_skip_reason(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseSpec,
    spec: literalizer.Language,
) -> str | None:
    """Return why this language cannot host the case's wrapper stub.

    ``call_transform`` is now opaque to the core (no sentinel probe),
    so the harness -- which knows the wrapper names from
    ``transform_stub_names`` -- decides whether the stub it injects can
    compile in this language: a dotted wrapper (e.g. ``tracer.emit``)
    needs ``supports_dotted_call_stub``; a bare wrapper (e.g. ``emit``)
    needs ``has_free_function_calls``.  A wrapper invoked with more than
    one parameter (the call's result alongside another value, e.g. the
    ``$zipped`` companion) needs
    ``supports_multi_param_call_wrapper_stub``; a case that splices a
    map literal as a free expression needs
    ``supports_dict_literal_as_free_expression``.  Languages that fail a
    check are skipped (no golden) rather than emitting a non-compiling
    fixture.
    """
    if (
        isinstance(config.variable_form, literalizer.ExistingVariable)
        and config.variable_form.name in config.ref_declarations
        and spec.call_assignment_declares_binding
        and len(find_redefinition_styles(spec=spec)) == 0
    ):
        return (
            f"{lang_cls.__name__} cannot redefine the seeded binding "
            f"for the {config.case_dir_name} fixture"
        )
    if (
        len(config.transform_stub_param_names) > 1
        and not lang_cls.supports_multi_param_call_wrapper_stub
    ):
        return (
            f"{lang_cls.__name__} cannot host a multi-parameter wrapper "
            f"stub for the {config.case_dir_name} fixture"
        )
    if (
        config.requires_dict_literal_as_free_expression
        and not lang_cls.supports_dict_literal_as_free_expression
    ):
        return (
            f"{lang_cls.__name__} cannot splice a map literal as a free "
            f"expression for the {config.case_dir_name} fixture"
        )
    for wrapper_name in config.transform_stub_names:
        if "." in wrapper_name:
            if not lang_cls.supports_dotted_call_stub:
                return (
                    f"{lang_cls.__name__} cannot declare a dotted call "
                    f"stub for {wrapper_name!r}"
                )
        elif not lang_cls.has_free_function_calls:
            return (
                f"{lang_cls.__name__} has no free function call syntax "
                f"for {wrapper_name!r}"
            )
    return None


@beartype
def _skip_if_wrapper_unsupported(
    *,
    config: CallCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Skip (and check any stale golden) when this language cannot host
    the case's wrapper stub.
    """
    reason = _wrapper_capability_skip_reason(
        lang_cls=lang_cls, config=config, spec=spec
    )
    if reason is not None:
        skip_golden(
            reason=reason,
            golden_path=golden_path,
            unlink=True,
            config=file_regression.request.config,
        )


@beartype
def _is_reserved_parameter_name(
    *, lang_cls: literalizer.LanguageCls, name: str
) -> bool:
    """Compare reserved names using the identifier case policy."""
    pattern = lang_cls.reserved_variable_identifier_pattern
    return (
        pattern is not None and pattern.fullmatch(string=name) is not None
    ) or is_reserved_identifier(
        case_sensitive=lang_cls.reserved_variable_identifiers_case_sensitive,
        name=name,
        reserved_identifiers=lang_cls.reserved_variable_identifiers,
    )


@beartype
def _invalid_parameter_grammar(
    *, lang_cls: literalizer.LanguageCls, name: str
) -> bool:
    """Apply the declared grammar and parameter-only restrictions."""
    pattern = lang_cls.reserved_call_parameter_identifier_pattern
    return (
        not lang_cls.new_variable_name_syntax.accepts(name=name)
        or (
            lang_cls.max_variable_identifier_length is not None
            and len(name) > lang_cls.max_variable_identifier_length
        )
        or name in lang_cls.reserved_call_parameter_identifiers
        or (pattern is not None and pattern.fullmatch(string=name) is not None)
    )


@beartype
def _invalid_target_grammar(
    *,
    lang_cls: literalizer.LanguageCls,
    target: str,
    wrapped: bool,
    spec: literalizer.Language,
) -> bool:
    """Recognize targets a call or its generated declarations reject."""
    parts = target.split(sep=".")
    syntax = lang_cls.call_target_name_syntax
    if syntax is None:
        syntax = lang_cls.new_variable_name_syntax
    constructor = any(
        spec.format_constructor_target(candidate) == target
        for candidate in re.findall(pattern=r"[^\W\d]\w*", string=target)
        if re.fullmatch(pattern=r"[A-Z][A-Za-z0-9_]*", string=candidate)
        is not None
    )
    if any(
        part == ""
        or (
            lang_cls.max_variable_identifier_length is not None
            and len(part) > lang_cls.max_variable_identifier_length
        )
        or (
            not syntax.accepts(name=part)
            and not (
                constructor
                and (len(parts) > 1 or lang_cls.accepts_type_name_call_target)
            )
        )
        for part in parts
    ):
        return True
    return (
        wrapped
        and not (constructor and lang_cls.declares_type_name_call_target)
        and any(
            not lang_cls.new_variable_name_syntax.accepts(name=part)
            for part in parts
        )
    )


@beartype
def _is_reserved_call_target(
    *, lang_cls: literalizer.LanguageCls, target_function: str
) -> bool:
    """Apply declaration keywords to the head and member keywords to
    every target component.
    """
    parts = target_function.split(sep=".")
    case_sensitive = (
        lang_cls.reserved_variable_identifiers_case_sensitive
        and lang_cls.reserved_call_target_keywords_case_sensitive
    )
    bare_identifiers = (
        lang_cls.reserved_bare_call_target_identifiers
        if len(parts) == 1
        else frozenset[str]()
    )
    head_identifiers = (
        lang_cls.reserved_variable_identifiers
        | lang_cls.reserved_call_target_head_identifiers
        | bare_identifiers
    ) - lang_cls.contextual_call_target_identifiers
    return is_reserved_identifier(
        case_sensitive=case_sensitive,
        name=parts[0],
        reserved_identifiers=head_identifiers,
    ) or any(
        is_reserved_identifier(
            case_sensitive=case_sensitive,
            name=part,
            reserved_identifiers=lang_cls.reserved_identifiers,
        )
        for part in parts
    )


@beartype
def _uses_bound_ref_wrapper(*, config: CallCaseSpec) -> bool:
    """Select the same reference wrapper for validation and rendering."""
    return (
        len(config.ref_declarations) > 0
        and len(config.unknown_ref_names) == 0
        and config.explicit_ref_value_sources is None
        and not config.has_call_transform
        and (len(config.transform_stub_names) == 0)
        and (config.variable_form is None)
    )


@beartype
def _call_support_exception(
    *, spec: literalizer.Language
) -> type[Exception] | None:
    """Preserve the API call-support error before shape checks."""
    match spec.call_style_config:
        case CallSupport.NOT_IN_LANGUAGE:
            return CallsNotSupportedByLanguageError
        case CallSupport.NOT_IMPLEMENTED_BY_TOOL:
            return CallsNotSupportedByToolError
        case _:
            return None


@beartype
def expected_call_shape_exception(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseSpec,
    spec: literalizer.Language,
) -> type[Exception] | None:
    """Return the exception ``literalize_call`` is expected to raise for
    this (lang, config) pair, or ``None`` if it should produce output.
    """
    parameter_count = len(config.parameter_names)
    max_params = lang_cls.max_call_parameters
    prerequisite_error = _call_support_exception(spec=spec)
    if prerequisite_error is None:
        prerequisite_error = _variable_form_expected_exception(
            lang_cls=lang_cls, variable_form=config.variable_form
        )
    if prerequisite_error is not None:
        return prerequisite_error
    if config.call_style_type is not None:
        style = next(
            style
            for style in lang_cls.CallStyles
            if isinstance(
                enum_payload(member=style, payload_type=object),
                config.call_style_type,
            )
        )
        spec = dataclasses.replace(spec, call_style=style)
    effective_style = spec.call_style_config
    bound_refs_wrap = _uses_bound_ref_wrapper(config=config)
    rejects_reserved_parameters = (
        config.wrap_in_file
        or bound_refs_wrap
        or isinstance(effective_style, literalizer.KeywordCallStyle)
    )
    target_parts = config.target_function.split(sep=".")
    shadowing = spec.call_parameter_shadowing
    declared_parts = (
        target_parts
        if shadowing is CallParameterShadowing.ANY_DECLARATION
        else target_parts[-1:]
        if shadowing is CallParameterShadowing.TARGET_NAME
        else []
    )
    case_sensitive = spec.reserved_variable_identifiers_case_sensitive
    invalid_parameter_signals = (
        any(
            _invalid_parameter_grammar(lang_cls=lang_cls, name=name)
            for name in config.parameter_names
        ),
        rejects_reserved_parameters
        and lang_cls.declares_call_parameter_names
        and any(
            _is_reserved_parameter_name(lang_cls=lang_cls, name=name)
            for name in config.parameter_names
        ),
        (config.wrap_in_file or bound_refs_wrap)
        and any(
            (
                parameter == declared
                if case_sensitive
                else parameter.casefold() == declared.casefold()
            )
            for parameter in config.parameter_names
            for declared in declared_parts
        ),
    )
    if any(invalid_parameter_signals):
        return InvalidCallParameterNameError
    # Every golden declares a stub, including the manual wrapper path.
    if _invalid_target_grammar(
        lang_cls=lang_cls,
        target=config.target_function,
        wrapped=True,
        spec=spec,
    ) or _is_reserved_call_target(
        lang_cls=lang_cls, target_function=config.target_function
    ):
        return InvalidCallTargetError
    unsupported_signals = (
        parameter_count == 0 and not lang_cls.supports_zero_parameter_calls,
        parameter_count > max_params,
        config.requires_inline_multiline_dict_args
        and not lang_cls.supports_inline_multiline_dict_args,
        config.requires_call_returns_expression
        and not lang_cls.call_returns_expression,
        config.requires_standalone_wrapped_comments
        and not lang_cls.supports_standalone_comments_in_wrapped_calls,
        _call_transform_style_unsupported(spec=spec, config=config),
    )
    if any(unsupported_signals):
        return UnsupportedCallShapeError
    if len(target_parts) > 1 and not spec.supports_dotted_calls:
        return DottedCallTargetNotSupportedError
    return (
        InvalidNewVariableNameError
        if not config.ref_case_per_language
        and any(
            not lang_cls.new_variable_name_syntax.accepts(name=name)
            or (
                lang_cls.max_variable_identifier_length is not None
                and len(name) > lang_cls.max_variable_identifier_length
            )
            for name in config.ref_declarations
        )
        else None
    )


@beartype
def _variable_form_expected_exception(
    *,
    lang_cls: literalizer.LanguageCls,
    variable_form: literalizer.VariableForm | None,
) -> type[Exception] | None:
    """Mirror ``_validate_call_variable_form`` rejection paths."""
    if variable_form is None:
        return None
    if not lang_cls.supports_variable_names:
        return VariableNameNotSupportedError
    if not lang_cls.call_returns_expression:
        return UnsupportedCallShapeError
    return None


@functools.cache
@beartype
def default_call_case_specs() -> tuple[CallCaseSpec, ...]:
    """Return every call case driven by the default per-language
    matrix.
    """
    return tuple(
        spec
        for spec in call_case_specs(cases_dir=CASES_DIR)
        if not spec.variant_only
    )


@functools.cache
@beartype
def discover_call_cases() -> list[CallCase]:
    """Return call test cases for all languages."""
    cases: list[CallCase] = []
    for config in default_call_case_specs():
        for lang_cls in sorted_languages():
            if not config.admits_language(lang_cls=lang_cls):
                continue
            if len(lang_cls.CallStyles) == 0:
                continue
            if (
                config.requires_heterogeneous_dict_values
                and not lang_cls.dict_supports_heterogeneous_values
            ):
                continue
            if config.call_style_type is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = list(lang_cls.CallStyles)
                matching = [
                    s
                    for s in styles
                    if isinstance(
                        enum_payload(member=s, payload_type=object),
                        config.call_style_type,
                    )
                ]
                if len(matching) == 0:
                    continue
                default_style = styles[0]
                if isinstance(
                    enum_payload(member=default_style, payload_type=object),
                    config.call_style_type,
                ):
                    continue
            expected_exception = expected_call_shape_exception(
                lang_cls=lang_cls,
                config=config,
                spec=make_spec(lang_cls=lang_cls),
            )
            cases.append(
                CallCase(
                    config=config,
                    lang_cls=lang_cls,
                    expected_exception=expected_exception,
                )
            )
    return cases


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
def _wrapper_declarations(
    *, spec: literalizer.Language, config: CallCaseSpec
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
        return _wrapper_declarations(spec=self.spec, config=self.config)

    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Apply the real wrapper convention to rendered native
        operands.
        """
        wrapper = self.wrapper
        spec = _wrapper_call_spec(spec=self.spec)
        style = spec.call_style_config
        if isinstance(style, CallSupport):
            msg = "Native call wrapper requires a supported call convention"
            raise TypeError(msg)
        operands: list[str] = []
        for role in wrapper.arguments:
            if role == "call":
                operands.append(context.call)
                continue
            operand = context.zipped
            if operand is None:
                msg = "Native call wrapper requires a zipped operand"
                raise ValueError(msg)
            value = self.zip_data
            if self.config.per_element:
                if not isinstance(value, list):
                    msg = "Per-element call wrapper requires a zipped list"
                    raise TypeError(msg)
                value = value[context.index]
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
    if config.call_transform_add_one:
        syntax = result
        if not isinstance(syntax, IntegerCallStubResult):
            msg = "call_transform_add_one requires an integer-returning stub"
            raise ValueError(msg)
        return IntegerResultCallTransform(
            syntax=syntax, outer=config.call_transform
        )
    if (
        not isinstance(result, NullableObjectCallStubResult)
        or result.conditional_template is None
    ):
        msg = (
            "call_transform_nullable_conditional requires a nullable "
            "object result and a native conditional expression"
        )
        raise ValueError(msg)
    return ConditionalCallTransform(
        template=result.conditional_template,
        null_value=result.value,
        comment_prefix=result.comment_prefix,
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


@beartype
def _literalize_call_case(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    source: str,
    input_info: CaseInput,
    effective_ref_case: literalizer.IdentifierCase | None,
    variable_form: literalizer.NewVariable
    | literalizer.ExistingVariable
    | None,
    wrap_in_file: bool,
    ref_values: Mapping[str, literalizer.ValueInput] | None,
    bound_refs: Mapping[str, literalizer.ValueInput] | None,
) -> literalizer.LiteralizeResult:
    """Run a configured call through the public API."""
    if isinstance(variable_form, literalizer.NewVariable):
        variable_form = dataclasses.replace(
            variable_form,
            modifiers=frozenset(
                enum_member_by_name(enum_cls=spec.modifiers, name=name)
                for name in config.variable_modifiers
            ),
        )
    call_transform = call_transform_for_case(spec=spec, config=config)
    if (
        call_transform is not None
        and not config.call_transform_reports_zip_usage
    ):
        call_transform = functools.partial(call_transform)
    return literalizer.literalize_call(
        source=source,
        input_format=input_info.input_format,
        input_root_key=config.input_root_key,
        language=spec,
        target_function=config.target_function,
        parameter_names=config.parameter_names,
        call_transform=call_transform,
        zip_source=config.zip_source,
        zip_input_format=config.zip_input_format,
        comment_source=config.comment_source,
        per_element=config.per_element,
        wrap_in_file=wrap_in_file,
        ref_case=effective_ref_case,
        consumable_refs=config.consumable_refs,
        ref_values=ref_values,
        bound_refs=bound_refs,
        ref_key=config.ref_key,
        collection_layout=literalizer.CollectionLayout(
            value=config.collection_layout
        ),
        variable_form=variable_form,
    )


@beartype
def _call_fixture_contents(
    *, code: str, spec: literalizer.Language, config: CallCaseSpec
) -> str:
    """Keep intentional identifier spellings in compiler fixtures."""
    names = (
        *config.target_function.split(sep="."),
        *config.parameter_names,
        *(
            name
            for name in config.ref_declarations
            if not config.ref_case_per_language
        ),
    )
    preamble = (
        language_metadata(
            language_id=spec.language_id
        ).golden.intentional_identifier_preamble
        if any(name != name.lower() for name in names)
        else ()
    )
    return "\n".join((*preamble, code, ""))


@beartype
def run_wrap_in_file_case(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    source: str,
    input_info: CaseInput,
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
    lang_extension: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
    pytest_config: pytest.Config,
) -> None:
    """Run ``literalize_call(..., wrap_in_file=True)`` and check
    golden.
    """
    with GoldenSkips(
        policy=_WRAP_IN_FILE_SKIPS,
        golden_path=golden_path,
        prefix=lang_name,
        config=pytest_config,
    ):
        wrap_result = _literalize_call_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            variable_form=config.variable_form,
            wrap_in_file=True,
            ref_values=(
                None
                if config.explicit_ref_value_sources is None
                else {
                    name: json.loads(s=ref_source)
                    for name, ref_source in (
                        config.explicit_ref_value_sources.items()
                    )
                }
            ),
            bound_refs={
                ref_name: json.loads(s=ref_source)
                for ref_name, ref_source in config.ref_declarations.items()
            },
        )
    check_golden(
        contents=_call_fixture_contents(
            code=wrap_result.code, spec=spec, config=config
        ),
        extension=lang_extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )


@dataclasses.dataclass(frozen=True)
class _CallWithDeclarations:
    """Result of literalizing ref declarations and a call together."""

    decl_results: list[literalizer.LiteralizeResult]
    result: literalizer.LiteralizeResult
    seeded_feedback: bool
    stub_argument_values: Sequence[ParsedValue]


@dataclasses.dataclass(frozen=True)
class _RefDeclaration:
    """A caller declaration and the actual calls used to seed it."""

    result: literalizer.LiteralizeResult
    seed_argument_values: Sequence[ParsedValue]


@beartype
def _render_ref_declaration(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    declaration_name: str,
    ref_source: str,
) -> _RefDeclaration:
    """Seed an existing binding using the synthetic function return
    carrier.
    """
    variable_form = literalizer.NewVariable(
        name=declaration_name,
        modifiers=frozenset(),
    )
    if (
        isinstance(config.variable_form, literalizer.ExistingVariable)
        and config.variable_form.name == declaration_name
    ):
        styles = find_redefinition_styles(spec=spec)
        seed_spec = spec
        seed_style = language_metadata(
            language_id=spec.language_id
        ).golden.call_seed_declaration_style
        if seed_style is not None:
            seed_spec = dataclasses.replace(
                spec,
                declaration_style=enum_member_by_name(
                    enum_cls=spec.declaration_styles, name=seed_style
                ),
            )
        elif len(styles) > 0:
            seed_spec = dataclasses.replace(spec, declaration_style=styles[0])
        result = literalizer.literalize_call(
            source=ref_source,
            input_format=literalizer.InputFormat.JSON,
            language=seed_spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            per_element=False,
            variable_form=variable_form,
        )
        return _RefDeclaration(
            result=result,
            seed_argument_values=([result.source_data],),
        )
    result = literalizer.literalize(
        source=ref_source,
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        variable_form=variable_form,
        collection_layout=literalizer.CollectionLayout(
            value=config.collection_layout
        ),
    )
    return _RefDeclaration(result=result, seed_argument_values=())


@beartype
def _run_call_with_declarations(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    source: str,
    input_info: CaseInput,
    declaration_names: dict[str, str],
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> _CallWithDeclarations:
    """Run ref declarations and the call, skipping on typed unsupported
    signals.
    """
    with GoldenSkips(
        policy=_DECLARATION_SKIPS,
        golden_path=golden_path,
        prefix=lang_name,
        config=file_regression.request.config,
    ):
        rendered_by_ref_name: dict[str, _RefDeclaration] = {
            ref_name: _render_ref_declaration(
                config=config,
                spec=spec,
                declaration_name=declaration_names[ref_name],
                ref_source=ref_source,
            )
            for ref_name, ref_source in config.ref_declarations.items()
        }
        decl_results_by_ref_name = {
            name: declaration.result
            for name, declaration in rendered_by_ref_name.items()
        }
        decl_results = list(decl_results_by_ref_name.values())
        ref_values = {
            ref_name: declaration.source_data
            for ref_name, declaration in decl_results_by_ref_name.items()
            if ref_name not in config.unknown_ref_names
        }
        ref_values.update(
            {
                ref_name: json.loads(s=ref_source)
                for ref_name, ref_source in (
                    config.extra_ref_value_sources.items()
                )
            }
        )
        effective_ref_values = None
        if len(ref_values) > 0:
            effective_ref_values = ref_values
        if config.explicit_ref_value_sources is not None:
            effective_ref_values = {
                name: json.loads(s=ref_source)
                for name, ref_source in (
                    config.explicit_ref_value_sources.items()
                )
            }
        followup_result = None
        followup_target = (
            config.target_function
            if config.followup_target_function is None
            else config.followup_target_function
        )
        if config.followup_source is not None:
            followup_result = literalizer.literalize_call(
                source=config.followup_source,
                input_format=input_info.input_format,
                language=spec,
                target_function=followup_target,
                parameter_names=config.parameter_names,
                per_element=config.per_element,
                ref_case=effective_ref_case,
                ref_key=config.ref_key,
                ref_values=effective_ref_values,
                call_transform=(
                    CallTransform(template="{call}")
                    if followup_target == config.target_function
                    and isinstance(
                        config.variable_form, literalizer.ExistingVariable
                    )
                    and call_result_discard_formatter(language=spec)
                    is not None
                    else None
                ),
            )
        result = _literalize_call_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            variable_form=config.variable_form,
            wrap_in_file=False,
            ref_values=(effective_ref_values),
            bound_refs=None,
        )
        if (
            followup_result is not None
            and isinstance(config.variable_form, literalizer.ExistingVariable)
            and config.variable_form.name in declaration_names.values()
        ):
            # Keep the seed use in the executable assignment fragment,
            # retaining its binding role for declarative-section wrappers.
            result = dataclasses.replace(
                result,
                declaration_code=(
                    f"{followup_result.bare_code}\n{result.bare_code}"
                ),
                pre_declaration_comments=(),
            )
        seeded_feedback = (
            isinstance(config.variable_form, literalizer.ExistingVariable)
            and followup_result is not None
            and followup_target == config.target_function
        )
        stub_argument_values = _arg_values_for_stub(
            source_data=result.source_data,
            per_element=config.per_element,
            seeded_feedback=seeded_feedback,
            seed_argument_values=tuple(
                value
                for declaration in rendered_by_ref_name.values()
                for value in declaration.seed_argument_values
            ),
        )
        if followup_result is not None:
            decl_results.append(result)
            result = followup_result
    return _CallWithDeclarations(
        decl_results=decl_results,
        result=result,
        seeded_feedback=seeded_feedback,
        stub_argument_values=stub_argument_values,
    )


@beartype
def _arg_values_for_stub(
    *,
    source_data: ParsedValue,
    per_element: bool,
    seeded_feedback: bool,
    seed_argument_values: Sequence[ParsedValue],
) -> Sequence[ParsedValue]:
    """Return argument rows for stubs, preserving a whole list as
    one argument.

    A per-element call always yields a list ``source_data``; the
    ``isinstance`` check narrows the type for the static checker.
    """
    if seeded_feedback:
        # The synthetic return carrier becomes an argument in later calls.
        # Original argument metadata cannot type every use of the callee.
        return ()
    if per_element and isinstance(source_data, list):
        return (*seed_argument_values, *source_data)
    return (*seed_argument_values, [source_data])


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


@beartype
def run_call_golden_case(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    version: enum.Enum,
) -> None:
    """Assemble a literalize_call golden-file case against *golden_name*.

    Shared by ``test_call_golden_file`` (default-spec per language)
    and ``test_call_variant_golden_file`` (non-default language
    variants, e.g. Rust's ``TAGGED_ENUM`` on an input the default
    ``ERROR`` strategy rejects).
    """
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    source = input_info.path.read_text(encoding="utf-8")
    golden_path = make_golden_path(
        parent=input_info.path.parent,
        name=golden_name,
        extension=lang_cls.extension,
        lang_cls=lang_cls,
        version=version,
    )
    _skip_if_wrapper_unsupported(
        config=config,
        lang_cls=lang_cls,
        spec=spec,
        golden_path=golden_path,
        file_regression=file_regression,
    )
    if config.call_style_type is not None:
        # Apply the manifest's style to variant specs as well as defaults.
        style = next(
            member
            for member in lang_cls.CallStyles
            if isinstance(
                enum_payload(member=member, payload_type=object),
                config.call_style_type,
            )
        )
        spec = dataclasses.replace(spec, call_style=style)
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    effective_ref_case: literalizer.IdentifierCase | None
    if config.ref_case_per_language:
        # First element of ``identifier_cases`` is the language's
        # default — convert declaration names to that case so the
        # ref-site and declaration-site spellings agree.
        default_case = reference_case_for_declaration_style(
            lang_cls=lang_cls, spec=spec
        )
        effective_ref_case = default_case
        declaration_names = {
            ref_name: default_case.convert(name=ref_name)
            for ref_name in config.ref_declarations
        }
    else:
        effective_ref_case = None
        declaration_names = {
            ref_name: ref_name for ref_name in config.ref_declarations
        }
    if config.wrap_in_file:
        run_wrap_in_file_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            lang_name=lang_cls.__name__,
            lang_extension=lang_cls.extension,
            golden_path=golden_path,
            file_regression=file_regression,
            pytest_config=file_regression.request.config,
        )
        return
    if _uses_bound_ref_wrapper(config=config):
        with GoldenSkips(
            policy=_DECLARATION_SKIPS,
            golden_path=golden_path,
            prefix=lang_cls.__name__,
            config=file_regression.request.config,
        ):
            bound = _literalize_call_case(
                config=config,
                spec=spec,
                source=source,
                input_info=input_info,
                effective_ref_case=effective_ref_case,
                variable_form=config.variable_form,
                wrap_in_file=True,
                ref_values=None,
                bound_refs={
                    ref_name: json.loads(s=ref_source)
                    for ref_name, ref_source in config.ref_declarations.items()
                },
            )
        check_golden(
            contents=_call_fixture_contents(
                code=bound.code, spec=spec, config=config
            ),
            extension=lang_cls.extension,
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    if _invalid_target_grammar(
        lang_cls=lang_cls,
        target=config.target_function,
        wrapped=True,
        spec=spec,
    ) and not _invalid_target_grammar(
        lang_cls=lang_cls,
        target=config.target_function,
        wrapped=False,
        spec=spec,
    ):
        raise InvalidCallTargetError(
            language_name=lang_cls.__name__,
            target_function=config.target_function,
            reason="cannot name a declaration in the generated file",
        )
    call_outcome = _run_call_with_declarations(
        config=config,
        spec=spec,
        source=source,
        input_info=input_info,
        declaration_names=declaration_names,
        effective_ref_case=effective_ref_case,
        lang_name=lang_cls.__name__,
        golden_path=golden_path,
        file_regression=file_regression,
    )
    decl_results = call_outcome.decl_results
    result = call_outcome.result
    # Build stub declarations for undefined names.
    body_stubs: list[str | RenderedCallStub] = []
    class_stubs: list[str] = []
    preamble_stubs: list[str] = []
    if config.has_call_transform or isinstance(
        config.variable_form, literalizer.ExistingVariable
    ):
        stub_return = literalizer.StubReturn.VALUE
    else:
        stub_return = literalizer.StubReturn.VOID
    target_function_parts = tuple(config.target_function.split(sep="."))
    call_arg_values = call_outcome.stub_argument_values
    body_stubs.extend(
        spec.format_call_stub(
            target_function_parts,
            config.parameter_names,
            stub_return,
            call_arg_values,
        ),
    )
    class_stubs.extend(
        spec.format_call_class_scope_stub(
            target_function_parts,
            config.parameter_names,
            stub_return,
            call_arg_values,
        ),
    )
    with GoldenSkips(
        policy=_PREAMBLE_STUB_SKIPS,
        golden_path=golden_path,
        prefix=lang_cls.__name__,
        config=file_regression.request.config,
    ):
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                target_function_parts,
                config.parameter_names,
                stub_return,
                call_arg_values,
            ),
        )
    # Statement stubs cover transform wrappers and a separate follow-up
    # consumer. Keep each target's parameter names so their argument
    # counts remain valid in languages with fixed parameter counts.
    wrapper_stubs = _wrapper_declarations(spec=spec, config=config)
    body_stubs.extend(wrapper_stubs.body)
    class_stubs.extend(wrapper_stubs.class_scope)
    preamble_stubs.extend(wrapper_stubs.file_scope)
    # One library entry point assembles the declarations and the call
    # into a single coherent file: it recomputes the body preamble
    # across the union of types in every declaration *and* the call,
    # recomputes the data-dependent header block over their combined
    # source data (so a single block covers every type, replacing the
    # old multi-line filter heuristic), wraps the pieces via
    # ``wrap_calls_with_declarations``, and places the deduplicated
    # preamble in front.  The call-stub lines this harness synthesizes
    # for the otherwise-undefined target/transform names are folded in
    # as the ``extra_*`` arguments.
    composed = literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=decl_results,
        call=result,
        extra_body_preamble=tuple(body_stubs),
        extra_class_preamble=tuple(class_stubs),
        extra_preamble=tuple(preamble_stubs),
    )
    check_golden(
        contents=_call_fixture_contents(
            code=composed.code, spec=spec, config=config
        ),
        extension=lang_cls.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )
