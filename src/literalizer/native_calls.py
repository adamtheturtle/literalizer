"""Structured, explicitly typed native invocation expressions.

Called functions and classes belong to the caller: native output never
invents stub receivers or infers signatures from input values.
"""

from __future__ import annotations

import dataclasses
import enum
from typing import Protocol, runtime_checkable

# Keep public type annotations resolvable at runtime.
from literalizer._language import Language  # noqa: TC001
from literalizer._types import ValueInput  # noqa: TC001


class ScalarType(enum.Enum):
    """Scalar roles whose spelling is owned by the native renderer."""

    BOOL = "bool"
    INTEGER = "integer"
    UNSIGNED = "unsigned"
    FLOAT = "float"
    VOID = "void"


@dataclasses.dataclass(frozen=True, kw_only=True)
class ObjectType:
    """A caller-owned object type, optionally with generic arguments."""

    name: str
    arguments: tuple[NativeType, ...] = ()


type NativeType = ScalarType | ObjectType


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeReference:
    """An existing value with its caller-declared native type."""

    name: str
    type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeClass:
    """A class receiver, distinct from an instance reference."""

    name: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeLiteral:
    """A literal value; its parameter signature controls boxing."""

    value: ValueInput


@dataclasses.dataclass(frozen=True, kw_only=True)
class FunctionTarget:
    """A genuine free-function target with an explicit signature."""

    name: str
    parameter_types: tuple[NativeType, ...]
    return_type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageTarget:
    """An instance or class message with a complete native selector."""

    receiver: NativeLiteral | NativeReference | NativeClass | NativeInvocation
    selector: str
    parameter_types: tuple[NativeType, ...]
    return_type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorTarget:
    """Allocation followed by the explicitly named initializer."""

    class_name: str
    selector: str = "init"
    parameter_types: tuple[NativeType, ...] = ()

    @property
    def return_type(self) -> ObjectType:
        """The allocated object's declared type."""
        return ObjectType(name=self.class_name)


type NativeTarget = FunctionTarget | MessageTarget | ConstructorTarget


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeInvocation:
    """A call expression whose arguments may themselves be calls."""

    target: NativeTarget
    arguments: tuple[NativeLiteral | NativeReference | NativeInvocation, ...]


@runtime_checkable
class NativeInvocationLanguage(Protocol):
    """Optional native syntax renderer, selected through a capability."""

    supports_native_invocations: bool

    @staticmethod
    def render_native_invocation(
        language: Language, invocation: NativeInvocation, /
    ) -> str:
        """Render one validated expression without a terminator."""
        ...

    @staticmethod
    def native_type_name(native_type: NativeType, /) -> str:
        """Spell a declared native type."""
        ...
