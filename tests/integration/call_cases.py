"""``literalize_call`` golden-file case discovery and runner.

Each ``cases/call_*`` directory declares in its own ``case.toml`` how it
is driven through :func:`literalizer.literalize_call`; this module turns
those declarations into per-language renderings. Default and variant
cases share one runner and the same versioned fixture paths.
"""

import dataclasses
import functools
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._formatters.preamble_roles import import_preamble
from literalizer._literalize import (
    _resolve_refs_for_inference,
    call_result_discard_formatter,
)
from literalizer._parsing import parse_input
from literalizer.exceptions import (
    CallArgNotSupportedError,
    DottedCallTargetNotSupportedError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    InvalidCallTargetError,
    ReservedVariableNameError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from tests.enum_members import enum_member_by_name

from .call_collection import CallRendering
from .call_expectations import (
    invalid_target_grammar,
    skip_unsupported_wrapper,
)
from .call_receivers import (
    compose_integer_calls,
    uses_integer_receiver,
)
from .call_stubs import argument_values_for_stub, target_call_declarations
from .call_transforms import (
    call_transform_for_case,
    followup_result_slots,
    wrapper_call_declarations,
)
from .case_inputs import CaseInput
from .case_manifests import (
    BoundCallFixture,
    CallCaseSpec,
    CallTransform,
    ComposedCallFixture,
    WrappedCallFixture,
    case_input,
)
from .golden_checks import (
    GoldenSkips,
    SkipPolicy,
    SkipReason,
    check_golden,
    cleanup_stale_golden,
    fixture_contents,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    reference_case_for_declaration_style,
    with_per_fixture_module_name,
)
from .parsed_values import ParsedValue

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
            error=UnrepresentableEmptyDictError,
            reason="cannot preserve an empty mapping call argument",
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
            error=UnrepresentableEmptyDictError,
            reason="cannot preserve an empty mapping call argument",
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
        and config.transform is not None
        and not config.transform.reports_zip_usage
    ):
        call_transform = functools.partial(call_transform)
    if config.shared_invocation:
        result = literalizer.literalize_invocations(
            source=source,
            input_format=input_info.input_format,
            language=spec,
            invocation={
                "default": {
                    "target-function": config.target_function,
                    "parameter-names": list(config.parameter_names),
                },
            },
            per_element=config.per_element,
            variable_form=variable_form,
        )
    else:
        result = literalizer.literalize_call(
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
    if config.expected_source_data is not None:
        expected = parse_input(
            source=config.expected_source_data,
            input_format=literalizer.InputFormat.JSON,
        ).data
        assert result.source_data == expected  # noqa: S101
    return result


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
            for name in config.fixture.ref_declarations
            if not config.ref_case_per_language
        ),
    )
    return fixture_contents(
        code=code,
        language_id=spec.language_id,
        intentional_identifier=any(name != name.lower() for name in names),
    )


@beartype
def _parse_ref_sources(
    *, sources: Mapping[str, str], input_format: literalizer.InputFormat
) -> dict[str, ParsedValue]:
    """Parse each caller-owned reference source in its declared format."""
    return {
        name: parse_input(source=source, input_format=input_format).data
        for name, source in sources.items()
    }


@beartype
def run_wrap_in_file_case(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    source: str,
    input_info: CaseInput,
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
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
                else _parse_ref_sources(
                    sources=config.explicit_ref_value_sources,
                    input_format=config.ref_input_format,
                )
            ),
            bound_refs=_parse_ref_sources(
                sources=config.fixture.ref_declarations,
                input_format=config.ref_input_format,
            ),
        )
    check_golden(
        contents=_call_fixture_contents(
            code=wrap_result.code, spec=spec, config=config
        ),
        golden_path=golden_path,
        file_regression=file_regression,
    )


@dataclasses.dataclass(frozen=True)
class _CallWithDeclarations:
    """Result of literalizing ref declarations and a call together."""

    decl_results: list[literalizer.LiteralizeResult]
    result: literalizer.LiteralizeResult
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
    observable: bool,
) -> _RefDeclaration:
    """Declare caller values, retaining legacy carriers for stub cases."""
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
        if observable:
            result = literalizer.literalize(
                source=ref_source,
                input_format=config.ref_input_format,
                language=seed_spec,
                variable_form=variable_form,
            )
            return _RefDeclaration(result=result, seed_argument_values=())
        result = literalizer.literalize_call(
            source=ref_source,
            input_format=config.ref_input_format,
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
        input_format=config.ref_input_format,
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
    fixture: ComposedCallFixture,
    spec: literalizer.Language,
    source: str,
    input_info: CaseInput,
    declaration_names: dict[str, str],
    effective_ref_case: literalizer.IdentifierCase | None,
    lang_name: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
    observable: bool,
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
                observable=observable,
            )
            for ref_name, ref_source in config.fixture.ref_declarations.items()
        }
        decl_results = [
            declaration.result for declaration in rendered_by_ref_name.values()
        ]
        ref_values = {
            ref_name: declaration.result.source_data
            for ref_name, declaration in rendered_by_ref_name.items()
            if ref_name not in fixture.unknown_ref_names
        }
        ref_values.update(
            _parse_ref_sources(
                sources=config.extra_ref_value_sources,
                input_format=config.ref_input_format,
            )
        )
        effective_ref_values = None
        if len(ref_values) > 0:
            effective_ref_values = ref_values
        if config.explicit_ref_value_sources is not None:
            effective_ref_values = _parse_ref_sources(
                sources=config.explicit_ref_value_sources,
                input_format=config.ref_input_format,
            )
        followup_result = None
        followup_target = config.target_function
        if fixture.followup is not None:
            followup_target = (
                fixture.followup.target_function
                if fixture.followup.target_function is not None
                else config.target_function
            )
            followup_result = literalizer.literalize_call(
                source=fixture.followup.source,
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
            observable
            and followup_result is not None
            and isinstance(config.variable_form, literalizer.ExistingVariable)
        ):
            # Observe the caller's initial binding through the same public
            # consumer before the assignment, without modifying any fragment.
            decl_results.append(followup_result)
        if observable:
            if followup_result is not None:
                decl_results.append(result)
                result = followup_result
            return _CallWithDeclarations(
                decl_results=decl_results,
                result=result,
                stub_argument_values=(),
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
        # A deliberately absent inference hint must not erase the actual
        # declaration's type from the compiler fixture's consumer signature.
        stub_source_data = result.source_data
        if len(fixture.unknown_ref_names) > 0:
            stub_source_data = _resolve_refs_for_inference(
                value=parse_input(
                    source=source, input_format=input_info.input_format
                ).data,
                ref_values={
                    name: declaration.result.source_data
                    for name, declaration in rendered_by_ref_name.items()
                },
                ref_key=config.ref_key,
            )
        stub_argument_values = argument_values_for_stub(
            source_data=stub_source_data,
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
        stub_argument_values=stub_argument_values,
    )


@beartype
def _render_call_golden_case(
    *,
    rendering: CallRendering,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Assemble one call rendering and compare its native golden file."""
    config = rendering.config
    fixture = config.fixture
    spec = rendering.spec
    lang_cls = rendering.lang_cls
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    source = input_info.path.read_text(encoding="utf-8")
    golden_path = rendering.golden_path(cases_dir=cases_dir)
    observable = uses_integer_receiver(config=config, spec=spec)
    if not observable:
        skip_unsupported_wrapper(
            config=config,
            lang_cls=lang_cls,
            spec=spec,
            golden_path=golden_path,
            file_regression=file_regression,
        )
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
            for ref_name in fixture.ref_declarations
        }
    else:
        effective_ref_case = None
        declaration_names = {
            ref_name: ref_name for ref_name in fixture.ref_declarations
        }
    if isinstance(fixture, WrappedCallFixture):
        run_wrap_in_file_case(
            config=config,
            spec=spec,
            source=source,
            input_info=input_info,
            effective_ref_case=effective_ref_case,
            lang_name=lang_cls.__name__,
            golden_path=golden_path,
            file_regression=file_regression,
            pytest_config=file_regression.request.config,
        )
        return
    if isinstance(fixture, BoundCallFixture) and not observable:
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
                bound_refs=_parse_ref_sources(
                    sources=fixture.ref_declarations,
                    input_format=config.ref_input_format,
                ),
            )
        check_golden(
            contents=_call_fixture_contents(
                code=bound.code, spec=spec, config=config
            ),
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    if isinstance(fixture, BoundCallFixture):
        # Native receivers supply declarations around the same public fragment.
        fixture = ComposedCallFixture(
            ref_declarations=fixture.ref_declarations
        )
    if invalid_target_grammar(
        lang_cls=lang_cls,
        target=config.target_function,
        wrapped=fixture.include_target_stub,
        spec=spec,
    ) and not invalid_target_grammar(
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
        fixture=fixture,
        config=config,
        spec=spec,
        source=source,
        input_info=input_info,
        declaration_names=declaration_names,
        effective_ref_case=effective_ref_case,
        lang_name=lang_cls.__name__,
        golden_path=golden_path,
        file_regression=file_regression,
        observable=observable,
    )
    decl_results = call_outcome.decl_results
    result = call_outcome.result
    if observable:
        code = compose_integer_calls(
            config=config,
            spec=spec,
            fragments=(*decl_results, result),
            return_increment=100,
        )
        check_golden(
            contents=_call_fixture_contents(
                code=code, spec=spec, config=config
            ),
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    # Build stub declarations for undefined names.
    target_stubs = target_call_declarations(
        fixture=fixture,
        config=config,
        spec=spec,
        argument_values=call_outcome.stub_argument_values,
        golden_path=golden_path,
        file_regression=file_regression,
        lang_name=lang_cls.__name__,
    )
    # Statement stubs cover transform wrappers and a separate follow-up
    # consumer. Keep each target's parameter names so their argument
    # counts remain valid in languages with fixed parameter counts.
    wrapper_stubs = wrapper_call_declarations(
        spec=spec,
        config=config,
        followup=fixture.followup,
        bound_result_slots=followup_result_slots(
            followup=fixture.followup,
            config=config,
            input_format=input_info.input_format,
        ),
    )
    body_stubs = (
        *target_stubs.body,
        *(import_preamble(code=entry) for entry in fixture.caller_imports),
        *fixture.caller_body_preamble,
        *wrapper_stubs.body,
    )
    class_stubs = (*target_stubs.class_scope, *wrapper_stubs.class_scope)
    preamble_stubs = (
        *target_stubs.file_scope,
        *wrapper_stubs.file_scope,
        *(
            spec.format_call_binding_file_pragmas()
            if config.variable_form is not None
            else ()
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
    composed = literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=decl_results,
        call=result,
        extra_body_preamble=body_stubs,
        extra_class_preamble=class_stubs,
        extra_preamble=preamble_stubs,
    )
    check_golden(
        contents=_call_fixture_contents(
            code=composed.code, spec=spec, config=config
        ),
        golden_path=golden_path,
        file_regression=file_regression,
    )


@beartype
def run_call_golden_case(
    *,
    rendering: CallRendering,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    pytest_config: pytest.Config,
) -> None:
    """Check a call rendering, including its declared rejection policy."""
    if rendering.expected_exception is None:
        _render_call_golden_case(
            rendering=rendering,
            cases_dir=cases_dir,
            file_regression=file_regression,
        )
        return
    with pytest.raises(expected_exception=rendering.expected_exception):
        _render_call_golden_case(
            rendering=rendering,
            cases_dir=cases_dir,
            file_regression=file_regression,
        )
    cleanup_stale_golden(
        golden_path=rendering.golden_path(cases_dir=cases_dir),
        config=pytest_config,
    )
