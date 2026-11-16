"""Observable integer receivers for the ordinary composed call corpus.

The event stream is authored next to each input, never reconstructed from
rendered source knowledge. Native receivers observe each actual argument,
return argument + 100, and observe the actual result at the next consumer.
Only native declaration syntax varies between backends; no source is patched.
"""

import dataclasses
import functools
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

import literalizer
from literalizer._language import CallStubDeclarations

from .case_manifests import CallCaseSpec, CaseManifestError


# Omitted table entries retain the ordinary native syntax and placement.
class IntegerReceiverSyntax(  # noqa: NOD001
    BaseModel, extra="forbid", frozen=True
):
    """Explicit native declarations sharing a unary integer signature."""

    scope: Literal["body", "class_scope", "file_scope"]
    event_separator: str = ", "
    event_suffix: str = ""
    state: str
    target: str
    target_void: str | None = None
    target_binding: str | None = None
    consumer: str
    wrapper: str
    wrapper_unary: str
    verify: str
    compile: list[str] = Field(default_factory=list[str])
    execute: list[str]
    path_on_stdin: bool = False


@functools.cache
def integer_receiver_syntax() -> dict[str, IntegerReceiverSyntax]:
    """Load syntax after capabilities have selected participants."""
    path = Path(__file__).with_name(name="call_receivers.toml")
    return {
        name: IntegerReceiverSyntax.model_validate(obj=syntax)
        for name, syntax in tomllib.loads(
            path.read_text(encoding="utf-8")
        ).items()
    }


def uses_integer_receiver(
    *, config: CallCaseSpec, spec: literalizer.Language
) -> bool:
    """Select native free-function observers by capabilities."""
    return (
        config.integer_receiver_events is not None
        and not config.wrap_in_file
        and spec.supports_stateful_free_call_consumers
        and spec.has_free_function_calls
        and spec.supports_zero_parameter_calls
    )


def integer_receiver_declarations(
    *, config: CallCaseSpec, spec: literalizer.Language, return_increment: int
) -> CallStubDeclarations:
    """Bind independently authored events to native signature syntax."""
    events = config.integer_receiver_events
    if events is None or len(events) == 0:
        msg = "an observable integer receiver needs an authored event stream"
        raise CaseManifestError(msg)
    try:
        syntax = integer_receiver_syntax()[spec.language_id]
    except KeyError as exc:
        msg = f"missing integer receiver syntax for {spec.language_id}"
        raise CaseManifestError(msg) from exc
    (parameter,) = config.parameter_names
    tags = {"call": 1, "result": 2, "zipped": 3}
    observations = tuple(
        value for kind, actual in events for value in (tags[kind], actual)
    )
    fields = {
        "events": syntax.event_separator.join(
            str(object=value) + syntax.event_suffix for value in observations
        ),
        "count": len(observations),
        "return_increment": return_increment,
        "target": config.target_function,
        "parameter": parameter,
        "consumer": config.followup_target_function,
        "wrapper": (
            None
            if config.call_transform_wrapper is None
            else config.call_transform_wrapper.target
        ),
    }
    target = syntax.target
    if config.variable_form is not None and syntax.target_binding is not None:
        target = syntax.target_binding
    elif (
        syntax.target_void is not None
        and config.variable_form is None
        and not config.has_call_transform
    ):
        target = syntax.target_void
    parts = [syntax.state, target]
    if config.followup_target_function is not None:
        parts.append(syntax.consumer)
    if config.call_transform_wrapper is not None:
        parts.append(
            syntax.wrapper
            if "zipped" in config.call_transform_wrapper.arguments
            else syntax.wrapper_unary
        )
    parts.append(syntax.verify)
    code = "\n".join(part.format(**fields) for part in parts)
    return dataclasses.replace(
        CallStubDeclarations(body=(), class_scope=(), file_scope=()),
        **{syntax.scope: (code,)},
    )


def compose_integer_calls(
    *,
    config: CallCaseSpec,
    spec: literalizer.Language,
    fragments: Sequence[literalizer.LiteralizeResult],
    return_increment: int,
) -> str:
    """Assemble real calls and a final count check using public APIs."""
    receiver = integer_receiver_declarations(
        config=config, spec=spec, return_increment=return_increment
    )
    return literalizer.literalize_call_with_declarations(
        language=spec,
        declarations=fragments,
        call=receiver_verification(spec=spec),
        extra_body_preamble=receiver.body,
        extra_class_preamble=receiver.class_scope,
        extra_preamble=receiver.file_scope,
    ).code


def receiver_verification(
    *, spec: literalizer.Language
) -> literalizer.LiteralizeResult:
    """Use the public composition API to check the final event count."""
    return literalizer.literalize_call(
        source="[[]]",
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        target_function="verify_events",
        parameter_names=(),
        per_element=True,
    )
