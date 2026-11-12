"""Validated call-transform templates declared by fixture manifests."""

from __future__ import annotations

import dataclasses
import string
from functools import cached_property

from beartype import beartype

import literalizer

CALL_TRANSFORM_PLACEHOLDERS = frozenset({"call", "zipped"})
"""Every name a ``call_transform`` template may substitute."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class CallTransform:
    """A validated ``call_transform`` template, applied per call.

    The template substitutes only :data:`CALL_TRANSFORM_PLACEHOLDERS`,
    so a manifest describes the wrapper text without carrying code.
    """

    template: str

    @cached_property
    def uses_zipped(self) -> bool:
        """Retain operand usage from the validated substitution
        template.
        """
        return any(
            field_name == "zipped"
            for _, field_name, _, _ in string.Formatter().parse(
                format_string=self.template
            )
        )

    @beartype
    def __call__(self, context: literalizer.CallContext, /) -> str:
        """Return transformed text and the template's operand usage."""
        return self.template.format(call=context.call, zipped=context.zipped)


def call_transform_from_template(value: object, /) -> object:
    """Build a :class:`CallTransform` from a validated template."""
    if not isinstance(value, str):
        return value
    for _, field_name, _, _ in string.Formatter().parse(format_string=value):
        if field_name is not None and (
            field_name not in CALL_TRANSFORM_PLACEHOLDERS
        ):
            msg = (
                f"unknown call_transform placeholder {field_name!r}; "
                f"expected one of {sorted(CALL_TRANSFORM_PLACEHOLDERS)}"
            )
            raise ValueError(msg)
    return CallTransform(template=value)
