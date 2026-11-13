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

    A gate reads the language default spec: a case selects languages,
    while a variant axis selects the specs its overrides build. Named
    language lists are not part of the root, reference or call schema.
    """

    gates: list[SuiteGate] = Field(default_factory=list[SuiteGate])

    @model_validator(mode="after")
    def _validate_language_selection(self) -> Self:
        """Validate every declared participation property."""
        validate_gate_names(subject="gates", gates=self.gates)
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
            return all(
                call_literal_gate_admits(
                    gate=gate, syntax=lang_cls.call_literal_syntax
                )
                for gate in literal_gates
            )
        return gates_admit(
            gates=self.gates,
            lang_cls=lang_cls,
            metadata=language_metadata(language_id=lang_cls.language_id),
            spec=make_spec(lang_cls=lang_cls),
        )
