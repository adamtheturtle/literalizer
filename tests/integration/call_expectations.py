"""Predict call outcomes and reject unsupported native wrappers."""

import dataclasses
import re
from collections.abc import Sequence
from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._enums import enum_payload
from literalizer._language import (
    CallParameterShadowing,
    CallSupport,
    is_reserved_identifier,
)
from literalizer._literalize import (
    _NormalizesDottedCallPartCase,
    _RequiresUniqueDottedCallParts,
)
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    DottedCallTargetNotSupportedError,
    InvalidCallParameterNameError,
    InvalidCallTargetError,
    InvalidNewVariableNameError,
    UnsupportedCallShapeError,
    VariableNameNotSupportedError,
)

from .case_manifests import (
    CallCaseSpec,
)
from .golden_checks import (
    skip_golden,
)
from .language_specs import (
    find_redefinition_styles,
)

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
def skip_unsupported_wrapper(
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
def invalid_target_grammar(
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
def uses_bound_ref_wrapper(*, config: CallCaseSpec) -> bool:
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
def _dotted_helper_parts_collide(
    *, spec: literalizer.Language, parts: Sequence[str]
) -> bool:
    """Recognize declaration collisions without narrowing success
    cases.
    """
    compared_parts = (
        [part.casefold() for part in parts]
        if isinstance(spec, _NormalizesDottedCallPartCase)
        and spec.dotted_call_stub_normalizes_part_case
        else parts
    )
    return (
        isinstance(spec, _RequiresUniqueDottedCallParts)
        and spec.dotted_call_stub_requires_unique_parts
        and len(set(compared_parts)) != len(compared_parts)
    )


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
    bound_refs_wrap = uses_bound_ref_wrapper(config=config)
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
    # A manual fixture can supply its own native target declaration.
    if (
        invalid_target_grammar(
            lang_cls=lang_cls,
            target=config.target_function,
            wrapped=config.wrap_in_file
            or bound_refs_wrap
            or config.include_target_stub,
            spec=spec,
        )
        or _is_reserved_call_target(
            lang_cls=lang_cls, target_function=config.target_function
        )
        or _dotted_helper_parts_collide(spec=spec, parts=target_parts)
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
