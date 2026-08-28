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
from collections.abc import Mapping, Sequence
from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import StubReturn

# ``_literalize_call_with_declarations`` is the shared call/declaration
# reconciliation core; it is intentionally not part of the public API
# (the public surface is ``literalize_call(bound_refs=...)``).  This
# golden-file harness must interpose its own transform-wrapper stubs
# between rendering and composition, so it uses the internal core
# directly.  See issue #1946.
from literalizer._literalize import (
    _literalize_call_with_declarations,
    literalize_call_parsed,
)
from literalizer._parsing import ParsedInput, parse_input
from literalizer._types import ValueInput
from literalizer.exceptions import (
    CallArgNotSupportedError,
    DottedCallTargetNotSupportedError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    InvalidCallParameterNameError,
    InvalidCallTargetError,
    UnrepresentableInputError,
    UnsupportedCallShapeError,
    VariableNameNotSupportedError,
)

from .case_inputs import CaseInput
from .case_manifests import CallCaseSpec, call_case_specs, case_input
from .golden_checks import (
    GoldenSkips,
    SkipPolicy,
    SkipReason,
    check_golden,
    skip_golden,
)
from .language_specs import (
    make_golden_path,
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
    lang_cls: literalizer.LanguageCls,
    config: CallCaseSpec,
) -> bool:
    """Mirror ``_validate_call_preconditions``'s rejection of
    ``call_transform`` for non-substitution call styles.

    ``call_transform`` is only supported when the effective call style
    is positional, keyword, or object.  When ``call_style_type`` is set
    the test pins that style; otherwise the language's default
    (first-listed) style applies.
    """
    if config.call_transform is None:
        return False
    if config.call_style_type is not None:
        return not issubclass(
            config.call_style_type, _SUBSTITUTION_CALL_STYLES
        )
    default_style = next(iter(lang_cls.CallStyles)).value
    return not isinstance(default_style, _SUBSTITUTION_CALL_STYLES)


@beartype
def _wrapper_capability_skip_reason(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseSpec,
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
    golden_path: Path,
) -> None:
    """Skip (and drop any stale golden) when this language cannot host
    the case's wrapper stub.
    """
    reason = _wrapper_capability_skip_reason(lang_cls=lang_cls, config=config)
    if reason is not None:
        skip_golden(reason=reason, golden_path=golden_path, unlink=True)


@beartype
def _expected_call_shape_exception(
    *,
    lang_cls: literalizer.LanguageCls,
    config: CallCaseSpec,
) -> type[Exception] | None:
    """Return the exception ``literalize_call`` is expected to raise for
    this (lang, config) pair, or ``None`` if it should produce output.
    """
    parameter_count = len(config.parameter_names)
    max_params = lang_cls.max_call_parameters
    variable_form_exc = _variable_form_expected_exception(
        lang_cls=lang_cls, variable_form=config.variable_form
    )
    if variable_form_exc is not None:
        return variable_form_exc
    styles = list(lang_cls.CallStyles)
    effective_style = (
        next(
            style
            for style in styles
            if isinstance(style.value, config.call_style_type)
        )
        if config.call_style_type is not None
        else styles[0]
    )
    bound_refs_wrap = bool(
        config.ref_declarations
        and not config.unknown_ref_names
        and config.call_transform is None
        and not config.transform_stub_names
        and config.variable_form is None
    )
    rejects_reserved_parameters = (
        config.wrap_in_file
        or bound_refs_wrap
        or isinstance(effective_style.value, literalizer.KeywordCallStyle)
    )
    if rejects_reserved_parameters and any(
        name in lang_cls.reserved_variable_identifiers
        for name in config.parameter_names
    ):
        return InvalidCallParameterNameError
    innermost_target_function = config.target_function.split(sep=".")[-1]
    if innermost_target_function in lang_cls.reserved_identifiers:
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
        _call_transform_style_unsupported(lang_cls=lang_cls, config=config),
    )
    if any(unsupported_signals):
        return UnsupportedCallShapeError
    return None


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
                    if isinstance(s.value, config.call_style_type)
                ]
                if not matching:
                    continue
                default_style = styles[0]
                if isinstance(default_style.value, config.call_style_type):
                    continue
            expected_exception = _expected_call_shape_exception(
                lang_cls=lang_cls,
                config=config,
            )
            cases.append(
                CallCase(
                    config=config,
                    lang_cls=lang_cls,
                    expected_exception=expected_exception,
                )
            )
    return cases


@beartype
def _select_call_input_root(
    *,
    source: str,
    input_info: CaseInput,
    input_root_key: str,
) -> ParsedInput:
    """Parse a case and select a table entry as the call-row root."""
    parsed = parse_input(
        source=source,
        input_format=input_info.input_format,
    )
    if not isinstance(parsed.data, dict):
        message = (
            f"{input_info.path} config selects {input_root_key!r}, "
            f"but its parsed root is {type(parsed.data).__name__}"
        )
        raise TypeError(message)
    try:
        selected = parsed.data[input_root_key]
    except KeyError as exc:
        message = (
            f"{input_info.path} has no configured call root {input_root_key!r}"
        )
        raise KeyError(message) from exc
    return dataclasses.replace(parsed, data=selected)


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
    ref_values: Mapping[str, ValueInput] | None,
    bound_refs: Mapping[str, ValueInput] | None,
) -> literalizer.LiteralizeResult:
    """Run a configured call through the public or parsed-input path."""
    if config.input_root_key is None:
        return literalizer.literalize_call(
            source=source,
            input_format=input_info.input_format,
            language=spec,
            target_function=config.target_function,
            parameter_names=config.parameter_names,
            call_transform=config.call_transform,
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
            variable_form=variable_form,
            collection_layout=literalizer.CollectionLayout(
                value=config.collection_layout
            ),
        )
    return literalize_call_parsed(
        parsed=_select_call_input_root(
            source=source,
            input_info=input_info,
            input_root_key=config.input_root_key,
        ),
        language=spec,
        target_function=config.target_function,
        parameter_names=config.parameter_names,
        call_transform=config.call_transform,
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
def _run_wrap_in_file_case(
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
) -> None:
    """Run ``literalize_call(..., wrap_in_file=True)`` and check
    golden.
    """
    with GoldenSkips(
        policy=_WRAP_IN_FILE_SKIPS,
        golden_path=golden_path,
        prefix=lang_name,
    ):
        wrap_result = _literalize_call_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            variable_form=config.variable_form,
            wrap_in_file=True,
            ref_values=None,
            bound_refs=None,
        )
    check_golden(
        contents=wrap_result.code + "\n",
        extension=lang_extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )


@dataclasses.dataclass(frozen=True)
class _CallWithDeclarations:
    """Result of literalizing ref declarations and a call together."""

    decl_results: list[literalizer.LiteralizeResult]
    result: literalizer.LiteralizeResult


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
) -> _CallWithDeclarations:
    """Run ref declarations and the call, skipping on typed unsupported
    signals.
    """
    with GoldenSkips(
        policy=_DECLARATION_SKIPS,
        golden_path=golden_path,
        prefix=lang_name,
    ):
        decl_results_by_ref_name: dict[str, literalizer.LiteralizeResult] = {
            ref_name: literalizer.literalize(
                source=ref_source,
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(
                    name=declaration_names[ref_name],
                    modifiers=frozenset(),
                ),
                collection_layout=literalizer.CollectionLayout(
                    value=config.collection_layout,
                ),
            )
            for ref_name, ref_source in config.ref_declarations.items()
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
        result = _literalize_call_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            variable_form=config.variable_form,
            wrap_in_file=False,
            ref_values=ref_values or None,
            bound_refs=None,
        )
    return _CallWithDeclarations(decl_results=decl_results, result=result)


@beartype
def _arg_values_for_stub(
    *,
    source_data: ParsedValue,
    per_element: bool,
) -> Sequence[ParsedValue]:
    """Mirror ``_literalize.py``'s ``arg_values`` shape: a list of
    arguments rows for per-element calls; a single-entry list
    wrapping the whole data otherwise.

    A per-element call always yields a list ``source_data``; the
    ``isinstance`` check narrows the type for the static checker.
    """
    if per_element and isinstance(source_data, list):
        return source_data
    return [source_data]


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
        config=config, lang_cls=lang_cls, golden_path=golden_path
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    effective_ref_case: literalizer.IdentifierCase | None
    if config.ref_case_per_language:
        # First element of ``identifier_cases`` is the language's
        # default — convert declaration names to that case so the
        # ref-site and declaration-site spellings agree.
        default_case = spec.identifier_cases[0]
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
        _run_wrap_in_file_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            lang_name=lang_cls.__name__,
            lang_extension=lang_cls.extension,
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    call_outcome = _run_call_with_declarations(
        config=config,
        spec=spec,
        source=source,
        input_info=input_info,
        declaration_names=declaration_names,
        effective_ref_case=effective_ref_case,
        lang_name=lang_cls.__name__,
        golden_path=golden_path,
    )
    decl_results = call_outcome.decl_results
    result = call_outcome.result
    # Build stub declarations for undefined names.
    body_stubs: list[str] = []
    preamble_stubs: list[str] = []
    stub_return = (
        StubReturn.VALUE
        if config.call_transform is not None
        else StubReturn.VOID
    )
    target_function_parts = tuple(config.target_function.split(sep="."))
    call_arg_values = _arg_values_for_stub(
        source_data=result.source_data,
        per_element=config.per_element,
    )
    body_stubs.extend(
        spec.format_call_stub(
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
    ):
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                target_function_parts,
                config.parameter_names,
                stub_return,
                call_arg_values,
            ),
        )
    # Stubs for transform function names.  The parameter count matches
    # ``transform_stub_param_names`` so a wrapper called with the call
    # and the zipped value (two arguments) compiles in
    # fixed-parameter-count languages.
    for wrapper_name in config.transform_stub_names:
        wrapper_name_parts = tuple(wrapper_name.split(sep="."))
        body_stubs.extend(
            spec.format_call_stub(
                wrapper_name_parts,
                config.transform_stub_param_names,
                StubReturn.VOID,
                (),
            ),
        )
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                wrapper_name_parts,
                config.transform_stub_param_names,
                StubReturn.VOID,
                (),
            ),
        )
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
    composed = _literalize_call_with_declarations(
        language=spec,
        declarations=decl_results,
        call=result,
        extra_body_preamble=tuple(body_stubs),
        extra_preamble=tuple(preamble_stubs),
    )
    # Anchor the public ``literalize_call(bound_refs=...)`` path to this
    # golden-verified composer output.  ``bound_refs`` injects only the
    # target stub, so the equivalence holds exactly when this case
    # synthesizes no extra (transform-wrapper) stubs and binds no
    # variable; those cases are exercised through the composer call
    # directly above.
    if (
        config.ref_declarations
        and not config.unknown_ref_names
        and config.call_transform is None
        and not config.transform_stub_names
        and config.variable_form is None
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
        divergence_message = (
            "literalize_call(bound_refs=...) diverged from the shared "
            f"call/declaration composition for {lang_cls.__name__} / "
            f"{config.case_dir_name}"
        )
        assert bound.code == composed.code, divergence_message  # noqa: S101
    check_golden(
        contents=composed.code + "\n",
        extension=lang_cls.extension,
        golden_path=golden_path,
        file_regression=file_regression,
    )
