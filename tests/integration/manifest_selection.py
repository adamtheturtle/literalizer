"""Language participation rules shared by case manifest entries."""

from typing import Self

from beartype import beartype
from pydantic import BaseModel, Field, model_validator

import literalizer

from .suite_gates import SuiteGate, gate_admits, validate_gate_names


# Defaults represent omitted participation gates.
class CapabilitySelection(  # noqa: NOD001
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Select participation through declared properties and syntax support.

    Gates describe backend availability. A default_behavior_flag
    explicitly selects by the unmodified configuration.
    """

    gates: list[SuiteGate] = Field(default_factory=list[SuiteGate])
    # Every required gate must match. At least one alternative must match
    # when alternatives are supplied.
    any_gates: list[SuiteGate] = Field(default_factory=list[SuiteGate])

    @model_validator(mode="after")
    def _validate_language_selection(self) -> Self:
        """Validate every declared participation property."""
        validate_gate_names(subject="gates", gates=self.gates)
        validate_gate_names(subject="any_gates", gates=self.any_gates)
        return self

    @beartype
    def admits_language(self, *, lang_cls: literalizer.LanguageCls) -> bool:
        """Discover a backend before resolving the fixture
        configuration.
        """
        return all(
            gate_admits(gate=gate, lang_cls=lang_cls) for gate in self.gates
        ) and (
            len(self.any_gates) == 0
            or any(
                gate_admits(gate=gate, lang_cls=lang_cls)
                for gate in self.any_gates
            )
        )
