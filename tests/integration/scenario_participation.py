"""Prerequisites for golden scenarios, evaluated on the resolved spec."""

import enum
from collections.abc import Iterable
from typing import assert_never

import literalizer
from literalizer._language import CallSupport, redefinition_config

from .golden_outcomes import Exclusion


class Requirement(enum.Enum):
    """A capability the native fixture needs from its configuration."""

    COLLECTION_COMMENTS = (
        "the configuration cannot preserve collection comments"
    )
    REDEFINITION = (
        "the selected declaration style does not permit redefinition"
    )
    CALL_SYNTAX = "the native reference consumer requires call syntax"
    CONSTRUCTOR_BINDING = (
        "the configuration cannot bind a nullary constructor result"
    )

    def satisfied_by(self, *, spec: literalizer.Language) -> bool:
        """Read the capability from the language that will render the case."""
        match self:
            case Requirement.COLLECTION_COMMENTS:
                return spec.supports_collection_comments
            case Requirement.REDEFINITION:
                return redefinition_config(
                    spec.declaration_style
                ).supports_redefinition
            case Requirement.CALL_SYNTAX:
                return not isinstance(spec.call_style_config, CallSupport)
            case Requirement.CONSTRUCTOR_BINDING:
                return (
                    Requirement.CALL_SYNTAX.satisfied_by(spec=spec)
                    and spec.supports_variable_names
                    and spec.supports_zero_parameter_calls
                    and spec.call_returns_expression
                )
            case _ as unreachable:
                assert_never(unreachable)


def scenario_exclusion(
    *,
    case_id: str,
    spec: literalizer.Language,
    requirements: Iterable[Requirement],
    fixture_reason: str | None,
) -> Exclusion | None:
    """Return the first unmet prerequisite with its case and version."""
    reason = next(
        (
            requirement.value
            for requirement in requirements
            if not requirement.satisfied_by(spec=spec)
        ),
        fixture_reason,
    )
    if reason is None:
        return None
    return Exclusion(
        reason=f"{case_id}@{spec.language_version.name}: {reason}",
    )
