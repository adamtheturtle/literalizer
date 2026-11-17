"""Fixed, lossless observations for deterministic native value checks.

JSON is only the envelope. Integers use decimal strings and binary64 floats
use network-order IEEE bits (or nan/+inf/-inf classifications). Mappings
carry typed key/value pairs. Datetimes carry local wall time and an exact
offset in microseconds, including an explicit naive marker.
"""

import dataclasses
import datetime as dt
import json
import math
import re
import struct
from collections.abc import Mapping
from typing import ClassVar, Protocol, runtime_checkable

from pydantic import JsonValue
from typing_extensions import TypeIs


@runtime_checkable
class NativeRecord(Protocol):
    """The standard dataclass field table used by record projections."""

    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[object]]]


def is_native_mapping(value: object, /) -> TypeIs[Mapping[object, object]]:
    """Narrow unknown runtime mapping keys and values without coercion."""
    return isinstance(value, Mapping)


def is_native_sequence(
    value: object, /
) -> TypeIs[list[object] | tuple[object, ...]]:
    """Narrow the two containers sharing the ordered sequence contract."""
    return isinstance(value, (list, tuple))


# The fixed scalar tags are intentionally dispatched together.
def observe(*, value: object) -> JsonValue:  # noqa: C901, PLR0911, PLR0912
    """Inspect Python values using only runtime/standard-library APIs.

    Lists and tuples share the ordered sequence contract. Dataclasses
    project to mappings of authored field names, as the record contract
    requires. No numeric, string/byte, or datetime conversions occur here.
    """
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["bool", value]
    if isinstance(value, int):
        return ["int", str(object=value)]
    if isinstance(value, float):
        if math.isnan(value):
            payload = "nan"
        elif math.isinf(value):
            payload = "+inf" if value > 0 else "-inf"
        else:
            payload = struct.pack("!d", value).hex()
        return ["float", payload]
    if isinstance(value, str):
        return ["string", value]
    if isinstance(value, bytes):
        return ["bytes", value.hex()]
    if isinstance(value, dt.datetime):
        offset = value.utcoffset()
        return [
            "datetime",
            value.replace(tzinfo=None).isoformat(timespec="microseconds"),
            "naive"
            if offset is None
            else str(object=offset // dt.timedelta(microseconds=1)),
        ]
    if isinstance(value, dt.date):
        return ["date", value.isoformat()]
    if isinstance(value, NativeRecord) and not isinstance(value, type):
        value = dataclasses.asdict(obj=value)
    if is_native_mapping(value):
        return [
            "mapping",
            [
                [observe(value=key), observe(value=item)]
                for key, item in value.items()
            ],
        ]
    if is_native_sequence(value):
        return ["sequence", [observe(value=item) for item in value]]
    msg = f"unsupported native observation type: {type(value).__name__}"
    raise TypeError(msg)


def _canonical(*, node: JsonValue) -> JsonValue:
    """Validate the fixed wire format and normalize mapping entry
    order.
    """
    if not isinstance(node, list) or len(node) == 0:
        msg = f"expected a tagged observation, got {node!r}"
        raise ValueError(msg)
    tag = node[0]
    if node == ["null"]:
        return node
    if tag == "datetime" and _valid_datetime(node=node):
        return node
    if len(node) == _PAIR_LENGTH:
        payload = node[1]
        if _valid_scalar(tag=tag, payload=payload):
            return node
        if isinstance(payload, list):
            if tag == "sequence":
                return [tag, [_canonical(node=item) for item in payload]]
            if tag == "mapping":
                return [tag, _mapping_entries(payload=payload)]
    msg = f"invalid native observation: {node!r}"
    raise ValueError(msg)


_PAIR_LENGTH = 2
_DATETIME_LENGTH = 3


def _valid_datetime(*, node: list[JsonValue]) -> bool:
    """Validate wall time and an exact, bounded UTC offset."""
    if len(node) != _DATETIME_LENGTH:
        return False
    wall, offset = node[1:]
    if not isinstance(wall, str) or not isinstance(offset, str):
        return False
    stamp = dt.datetime.fromisoformat(wall)
    return (
        stamp.tzinfo is None
        and stamp.isoformat(timespec="microseconds") == wall
        and (
            offset == "naive"
            or (
                str(object=int(offset)) == offset
                and abs(int(offset))
                < dt.timedelta(days=1) // dt.timedelta(microseconds=1)
            )
        )
    )


def _valid_scalar(*, tag: JsonValue, payload: JsonValue) -> bool:  # noqa: PLR0911
    """Validate the finite set of scalar payload encodings."""
    if tag == "bool":
        return isinstance(payload, bool)
    if not isinstance(payload, str):
        return False
    if tag == "string":
        return True
    if tag == "int":
        return (
            re.fullmatch(pattern=r"-?(0|[1-9][0-9]*)", string=payload)
            is not None
            and payload != "-0"
        )
    if tag == "float":
        if payload in {"nan", "+inf", "-inf"}:
            return True
        return re.fullmatch(
            pattern=r"[0-9a-f]{16}", string=payload
        ) is not None and math.isfinite(
            struct.unpack("!d", bytes.fromhex(payload))[0]
        )
    if tag == "bytes":
        return (
            re.fullmatch(pattern=r"(?:[0-9a-f]{2})*", string=payload)
            is not None
        )
    return (
        tag == "date" and dt.date.fromisoformat(payload).isoformat() == payload
    )


def _mapping_entries(*, payload: list[JsonValue]) -> list[JsonValue]:
    """Normalize entry order while rejecting duplicate typed keys."""
    entries: list[JsonValue] = []
    keys: set[str] = set()
    for entry in payload:
        if not isinstance(entry, list) or len(entry) != _PAIR_LENGTH:
            msg = f"invalid mapping entry: {entry!r}"
            raise ValueError(msg)
        key = _canonical(node=entry[0])
        encoded_key = json.dumps(obj=key, allow_nan=False)
        if encoded_key in keys:
            msg = f"duplicate observed mapping key: {key!r}"
            raise ValueError(msg)
        keys.add(encoded_key)
        entries.append([key, _canonical(node=entry[1])])
    return sorted(
        entries, key=lambda item: json.dumps(obj=item, allow_nan=False)
    )


def verify_observation(
    *, label: str, actual: JsonValue, expected: JsonValue
) -> None:
    """Compare typed observations, reporting the case and both values."""
    try:
        want = _canonical(node=expected)
        got = _canonical(node=actual)
        # Serialized comparison also prevents Python's True == 1 equality.
        equal = json.dumps(obj=want, allow_nan=False) == json.dumps(
            obj=got, allow_nan=False
        )
    except (ValueError, TypeError) as exc:
        msg = f"{label}: invalid typed observation: {exc}"
        raise ValueError(msg) from exc
    if not equal:
        msg = (
            f"{label}: typed observation mismatch\n"
            f"expected: {want!r}\nactual:   {got!r}"
        )
        raise ValueError(msg)
