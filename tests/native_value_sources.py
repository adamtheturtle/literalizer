"""Typed native values that TOML fixtures cannot express directly."""

from __future__ import annotations

import datetime as dt
from typing import Annotated, Literal

from beartype import beartype
from pydantic import BaseModel, BeforeValidator, Field, NaiveDatetime

from literalizer import ValueInput
from literalizer._types import Scalar


class OffsetDatetimeSource(
    BaseModel, extra="forbid", frozen=True, strict=True
):
    """Native offsets finer than a TOML timestamp permits."""

    wall_time: NaiveDatetime
    offset_microseconds: int


def _parse_ref_datetime(value: object, /) -> object:
    """Construct exact offsets without relying on ISO parser precision."""
    if isinstance(value, dict):
        source = OffsetDatetimeSource.model_validate(obj=value)
        return source.wall_time.replace(
            tzinfo=dt.timezone(
                offset=dt.timedelta(microseconds=source.offset_microseconds)
            )
        )
    return value


type RefDatetimeInput = Annotated[
    dt.datetime, BeforeValidator(func=_parse_ref_datetime)
]
type RefScalarInput = Annotated[
    Scalar, BeforeValidator(func=_parse_ref_datetime)
]


class ScalarValueSource(BaseModel, extra="forbid", frozen=True, strict=True):
    """A scalar, including an exact native datetime."""

    kind: Literal["scalar"]
    value: RefScalarInput

    @beartype
    def to_value(self) -> ValueInput:
        """Return the declared native scalar."""
        return self.value


class SequenceValueSource(BaseModel, extra="forbid", frozen=True, strict=True):
    """A sequence whose elements may themselves be native containers."""

    kind: Literal["sequence"]
    items: Annotated[tuple[RefValueSource, ...], Field(strict=False)]

    @beartype
    def to_value(self) -> ValueInput:
        """Build the declared native sequence."""
        return [item.to_value() for item in self.items]


class MappingEntrySource(BaseModel, extra="forbid", frozen=True, strict=True):
    """A mapping entry retaining the native type of its key."""

    key: RefScalarInput
    value: RefValueSource


class MappingValueSource(BaseModel, extra="forbid", frozen=True, strict=True):
    """A mapping with native keys and recursively declared values."""

    kind: Literal["mapping"]
    entries: Annotated[tuple[MappingEntrySource, ...], Field(strict=False)]

    @beartype
    def to_value(self) -> ValueInput:
        """Build the declared mapping in entry order."""
        return {entry.key: entry.value.to_value() for entry in self.entries}


type RefValueSource = Annotated[
    ScalarValueSource | SequenceValueSource | MappingValueSource,
    Field(discriminator="kind"),
]
