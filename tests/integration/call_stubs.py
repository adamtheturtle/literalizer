"""Synthetic call targets shared by call and reference fixtures."""

import dataclasses
from collections.abc import Sequence
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._language import CallStubDeclarations

from .case_manifests import (
    CallCaseSpec,
    ComposedCallFixture,
)
from .parsed_values import ParsedValue


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
    fixture: ComposedCallFixture,
    spec: literalizer.Language,
    argument_values: Sequence[ParsedValue],
    case_dir: Path,
) -> CallStubDeclarations:
    """Use the authored target or synthesize a stub for the call."""
    if fixture.target_source is not None:
        source = (case_dir / fixture.target_source).read_text(encoding="utf-8")
        return CallStubDeclarations(
            body=(), class_scope=(), file_scope=(source.rstrip("\n"),)
        )
    if not fixture.include_target_stub:
        return CallStubDeclarations(body=(), class_scope=(), file_scope=())
    stub_return = (
        literalizer.StubReturn.VALUE
        if (config.transform is not None) or config.variable_form is not None
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
    file_scope = stub_spec.format_call_preamble_stub(
        target_parts,
        config.parameter_names,
        stub_return,
        argument_values,
    )
    return CallStubDeclarations(
        body=body, class_scope=class_scope, file_scope=file_scope
    )
