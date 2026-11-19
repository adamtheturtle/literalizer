"""Observe Python fixture values and independently projected expectations."""

from __future__ import annotations

import dataclasses
import datetime as dt
import math
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import JsonValue
    from typing_extensions import TypeIs

_EPOCH = dt.datetime(year=1970, month=1, day=1, tzinfo=dt.UTC)
_MICROSECOND = dt.timedelta(microseconds=1)


def is_native_mapping(value: object, /) -> TypeIs[dict[object, object]]:
    """Identify native dictionaries without narrowing their key types."""
    return isinstance(value, dict)


def is_native_sequence(
    value: object, /
) -> TypeIs[list[object] | tuple[object, ...]]:
    """Identify the two supported Python sequence representations."""
    return isinstance(value, (list, tuple))


def epoch_microseconds(value: dt.datetime) -> int:
    """Return an exact epoch count, interpreting naive times as UTC."""
    offset = value.utcoffset()
    elapsed = value.replace(tzinfo=dt.UTC) - _EPOCH
    if offset is not None:
        elapsed -= offset
    return elapsed // _MICROSECOND


def _observe_scalar(value: object) -> list[JsonValue]:
    """Encode a scalar with a tag and a JSON payload."""
    match value:
        case None:
            return ["null", None]
        case bool():
            return ["bool", value]
        case int():
            return ["int", str(object=value)]
        case str():
            return ["string", value]
        case bytes():
            return ["bytes", value.hex()]
        case dt.date():
            return ["date", value.isoformat()]
        case _:
            msg = f"unsupported native value: {type(value).__name__}"
            raise TypeError(msg)


def observe(value: object) -> list[JsonValue]:
    """Encode tagged values, retaining typed mapping keys and exact floats."""
    match value:
        case float():
            if math.isnan(value):
                payload = "nan"
            elif math.isinf(value):
                payload = "+inf" if value > 0 else "-inf"
            else:
                payload = struct.pack("!d", value).hex()
            return ["float", payload]
        case dt.datetime():
            offset = value.utcoffset()
            return [
                "datetime",
                [
                    str(object=epoch_microseconds(value=value)),
                    None
                    if offset is None
                    else str(object=offset // _MICROSECOND),
                ],
            ]
        case _ if is_native_sequence(value):
            return ["sequence", [observe(value=item) for item in value]]
        case _ if is_native_mapping(value):
            return [
                "mapping",
                [
                    [observe(value=key), observe(value=item)]
                    for key, item in value.items()
                ],
            ]
        case _:
            return _observe_scalar(value=value)


def observe_record(value: object) -> list[JsonValue]:
    """Project a native dataclass instance onto its declared fields."""
    if not dataclasses.is_dataclass(obj=value) or isinstance(value, type):
        msg = "expected a native dataclass instance"
        raise TypeError(msg)
    # Pyrefly only narrows the TypeIs argument when passed positionally.
    fields = dataclasses.fields(
        class_or_instance=value  # pyrefly: ignore[bad-argument-type]
    )
    return observe(
        value={field.name: getattr(value, field.name) for field in fields}
    )
