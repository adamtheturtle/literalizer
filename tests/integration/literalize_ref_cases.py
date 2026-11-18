"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

Each ``cases/literalize_ref_*`` directory declares in its own ``case.toml``
how it is driven through :func:`literalizer.literalize` with a ``ref_case``
set to the language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import copy
import dataclasses
import functools
import json
from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
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

from .case_manifests import (
    BoundRefContext,
    ExternalRefContext,
    RefExpressionContext,
    case_input,
)
from .golden_checks import (
    GoldenSkips,
    check_golden,
    check_outcome,
)
from .golden_skip_policy import SkipPolicy, SkipReason
from .language_specs import (
    find_redefinition_styles,
    with_per_fixture_module_name,
)
from .ref_consumers import (
    compose_external_ref_fixture,
    compose_ref_expression_fixture,
    external_assignment_spec,
    ref_fixture_contents,
)
from .reference_cases import RefRendering
from .reference_inputs import bound_ref_inputs, parse_ref_input

CASES_DIR = Path(__file__).parent / "cases"


# A ``$ref`` case is written once for every language, so an input a
# language cannot represent, or a ref identifier it will not spell,
# skips rather than fails.
_REF_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=CallsNotSupportedByLanguageError,
            reason="has no generated consumer call syntax",
        ),
        SkipReason(
            error=CallsNotSupportedByToolError,
            reason="cannot generate consumer calls",
        ),
        SkipReason(
            error=IncompatibleFormatsError,
            reason="reference input is incompatible with the selected formats",
        ),
        SkipReason(
            error=ReservedVariableNameError,
            reason="rejects a declared reference identifier",
        ),
        SkipReason(
            error=VariableNameNotSupportedError,
            reason="cannot declare the reference binding",
        ),
        SkipReason(
            error=ExistingVariableNotSelfContainedError,
            reason=(
                "cannot wrap an assignment without its destination declaration"
            ),
        ),
        SkipReason(
            error=NullInCollectionError,
            reason="cannot represent null in this collection",
        ),
        SkipReason(
            error=HeterogeneousCollectionError,
            reason="cannot represent this heterogeneous input",
        ),
        SkipReason(
            error=UnrepresentableInputError,
            reason="cannot represent this heterogeneous input",
        ),
        SkipReason(
            error=CallArgNotSupportedError,
            reason="rejected ref identifier",
        ),
        SkipReason(
            error=InvalidDictKeyError,
            reason="cannot represent a dictionary key",
        ),
    ),
    suffix="",
)


@beartype
def _render_reference_golden(
    *,
    rendering: RefRendering,
    cases_dir: Path,
) -> str:
    """Run one collected reference rendering against its golden file.

    Selected ref cases use the language's identifier spelling.
    Each referenced identifier is supplied through ``bound_refs``.
    Bindings precede their first use so the fixture is a complete
    program with the language's declaration order.
    """
    config = rendering.config
    context = config.context
    lang_cls = rendering.lang_cls
    ref_case = rendering.ref_case
    spec = rendering.spec
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    input_path = input_info.path
    input_source = input_path.read_text(encoding="utf-8")
    golden_path = rendering.artifact(cases_dir=cases_dir).path
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    if (
        config.variable_form == "both"
        and config.declaration_style is None
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        spec = dataclasses.replace(
            spec, declaration_style=find_redefinition_styles(spec=spec)[0]
        )
    wrap_in_file = isinstance(context, BoundRefContext)
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
    if not spec.supports_variable_names:
        variable_form_obj = None
    raw_data = parse_ref_input(
        input_format=input_info.input_format,
        input_source=input_source,
    )
    effective_bound_refs = None
    if isinstance(context, ExternalRefContext):
        spec = external_assignment_spec(
            context=context,
            spec=spec,
            config=config,
            raw_data=raw_data,
        )
    else:
        bound_refs_input = bound_ref_inputs(
            context=context,
            config=config,
            raw_data=raw_data,
            lang_cls=lang_cls,
        )
        if len(bound_refs_input) > 0:
            effective_bound_refs = bound_refs_input
    effective_ref_values = None
    if config.explicit_ref_value_sources is not None:
        effective_ref_values = {
            name: json.loads(s=source)
            for name, source in (config.explicit_ref_value_sources.items())
        }
    original_ref_values = copy.deepcopy(x=effective_ref_values)
    result = literalizer.literalize(
        source=input_source,
        input_format=input_info.input_format,
        language=spec,
        variable_form=variable_form_obj,
        wrap_in_file=wrap_in_file,
        ref_case=ref_case,
        bound_refs=(effective_bound_refs),
        ref_values=(effective_ref_values),
        ref_key=config.ref_key,
        include_delimiters=config.include_delimiters,
        pre_indent_level=config.pre_indent_level,
        collection_layout=literalizer.CollectionLayout(
            value=config.collection_layout
        ),
    )
    assert effective_ref_values == original_ref_values, (  # noqa: S101
        "literalize mutated caller-owned ref_values"
    )
    if isinstance(context, RefExpressionContext):
        result = compose_ref_expression_fixture(
            context=context,
            spec=spec,
            result=result,
        )
    elif isinstance(context, ExternalRefContext):
        result = compose_external_ref_fixture(
            context=context,
            config=config,
            spec=spec,
            result=result,
            raw_data=raw_data,
        )
    return ref_fixture_contents(
        code=result.code,
        spec=spec,
        lang_cls=lang_cls,
        ref_case=ref_case,
    )


@beartype
def run_literalize_ref_golden_case(
    *,
    rendering: RefRendering,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Exercise the resolved expectation for the reference."""
    golden_path = rendering.artifact(cases_dir=cases_dir).path
    render = functools.partial(
        _render_reference_golden, rendering=rendering, cases_dir=cases_dir
    )
    if rendering.outcome is None:
        with GoldenSkips(
            policy=_REF_SKIPS,
            golden_path=golden_path,
            prefix=rendering.lang_cls.__name__,
        ):
            contents = render()
        check_golden(
            contents=contents,
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    check_outcome(
        outcome=rendering.outcome,
        render=render,
        golden_path=golden_path,
        file_regression=file_regression,
    )
