"""Synthetic call targets shared by call and reference fixtures."""

import dataclasses
from collections.abc import Sequence
from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer._language import CallStubDeclarations
from literalizer.exceptions import HeterogeneousCollectionError

from .case_manifests import CallCaseSpec
from .golden_checks import GoldenSkips, SkipPolicy, SkipReason
from .parsed_values import ParsedValue

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


@beartype
def argument_values_for_stub(
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
def call_stub_spec(
    *, spec: literalizer.Language, argument_values: Sequence[ParsedValue]
) -> literalizer.Language:
    """Infer consumer types without changing the composer's inference
    state.
    """
    stub_spec = dataclasses.replace(spec)
    compute_record_shapes = (
        stub_spec.heterogeneous_behavior.compute_record_shapes
    )
    if compute_record_shapes is not None:
        _ = compute_record_shapes(list(argument_values))
    return stub_spec


@beartype
def target_call_declarations(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    argument_values: Sequence[ParsedValue],
    golden_path: Path,
    file_regression: FileRegressionFixture,
    lang_name: str,
) -> CallStubDeclarations:
    """Declare synthetic targets unless the case uses a built-in."""
    if not config.include_target_stub:
        return CallStubDeclarations(body=(), class_scope=(), file_scope=())
    stub_return = (
        literalizer.StubReturn.VALUE
        if config.has_call_transform or config.variable_form is not None
        else literalizer.StubReturn.VOID
    )
    stub_spec = call_stub_spec(spec=spec, argument_values=argument_values)
    target_parts = tuple(config.target_function.split(sep="."))
    body = stub_spec.format_call_stub(
        target_parts, config.parameter_names, stub_return, argument_values
    )
    class_scope = stub_spec.format_call_class_scope_stub(
        target_parts, config.parameter_names, stub_return, argument_values
    )
    file_scope: list[str] = []
    with GoldenSkips(
        policy=_PREAMBLE_STUB_SKIPS,
        golden_path=golden_path,
        prefix=lang_name,
        config=file_regression.request.config,
    ):
        file_scope.extend(
            stub_spec.format_call_preamble_stub(
                target_parts,
                config.parameter_names,
                stub_return,
                argument_values,
            ),
        )
    return CallStubDeclarations(
        body=body, class_scope=class_scope, file_scope=tuple(file_scope)
    )
