"""Read heterogeneous enum payloads at a checked type boundary."""

from enum import Enum
from typing import Protocol, runtime_checkable

from beartype import beartype


@runtime_checkable
class _EnumValue(Protocol):
    """The object-valued interface shared by arbitrary enum members."""

    @property
    def value(self) -> object:
        """Return the member's payload without propagating Any."""
        ...


@beartype
def enum_payload[T](*, member: Enum, payload_type: type[T]) -> T:
    """Read a payload and verify the configuration contract it must
    meet.
    """
    option: _EnumValue = member
    value = option.value
    if not isinstance(value, payload_type):
        msg = (
            f"{type(member).__name__}.{member.name} requires a "
            f"{payload_type.__name__} payload; got {type(value).__name__}"
        )
        raise TypeError(msg)
    return value
