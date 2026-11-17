"""Language participation rules shared by case manifest entries."""

from typing import Self

from beartype import beartype
from pydantic import BaseModel, Field, model_validator

import literalizer

from .language_metadata import language_metadata
from .language_specs import make_spec
from .suite_gates import (
    CallCharacterQuoteGate,
    CallHashRawPrefixGate,
    CallIdentifierPrefixGate,
    CallInterpolationGate,
    CallLiteralFlagGate,
    CallRawStringPrefixGate,
    SuiteGate,
    call_literal_gate_admits,
    gates_admit,
    validate_gate_names,
)


# Defaults represent omitted participation gates.
class CapabilitySelection(  # noqa: NOD001
    BaseModel,
    arbitrary_types_allowed=True,
    extra="forbid",
    frozen=True,
    strict=True,
):
    """Select participation through declared properties and syntax support.

    Gates read properties of the language and its default spec.
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
        """Return whether this narrowing selects *lang_cls*."""
        literal_gates = tuple(
            gate
            for gate in self.gates
            if isinstance(
                gate,
                (
                    CallLiteralFlagGate,
                    CallRawStringPrefixGate,
                    CallInterpolationGate,
                    CallCharacterQuoteGate,
                    CallHashRawPrefixGate,
                    CallIdentifierPrefixGate,
                ),
            )
        )
        if len(literal_gates) == len(self.gates):
            admitted = all(
                call_literal_gate_admits(
                    gate=gate, syntax=lang_cls.call_literal_syntax
                )
                for gate in literal_gates
            )
        else:
            admitted = gates_admit(
                gates=self.gates,
                lang_cls=lang_cls,
                metadata=language_metadata(language_id=lang_cls.language_id),
                spec=make_spec(lang_cls=lang_cls),
            )
        if not admitted or len(self.any_gates) == 0:
            return admitted
        return any(
            gates_admit(
                gates=(gate,),
                lang_cls=lang_cls,
                metadata=language_metadata(language_id=lang_cls.language_id),
                spec=make_spec(lang_cls=lang_cls),
            )
            for gate in self.any_gates
        )
