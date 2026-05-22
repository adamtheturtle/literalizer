"""Render a :class:`Value` as a single-line JSON document.

Shared between language back-ends that emit values through a JSON
value type (Java's ``JsonNode`` via ``ObjectMapper.readTree``, Haskell's
``Data.Aeson.Value`` via the ``aesonQQ`` quasi-quote bracket, and any
future ports).  Temporal values are folded into ISO-8601 strings, bytes
become hex strings, and sets / :class:`OrderedMap` collapse into list /
dict so :func:`json.dumps` can serialize them.
"""

import datetime
import json

from beartype import beartype

from literalizer._types import OrderedMap, Value


@beartype
def _temporal_to_iso(data: datetime.date | datetime.time) -> str:
    """Return ISO-8601 text for a date / datetime / time value.

    Naive datetimes are anchored to UTC so JSON consumers that require an
    offset (Jackson's ``readTree`` and the ``Data.Aeson`` parsers) can
    round-trip the value without raising.
    """
    if isinstance(data, datetime.datetime):
        iso = data.isoformat()
        if data.tzinfo is None:
            iso += "Z"
        return iso
    return data.isoformat()


@beartype
def _to_jsonable(data: Value) -> object:
    """Convert *data* into a value that :func:`json.dumps` can serialize.

    Dates, datetimes, and times become ISO-8601 strings (JSON has no
    temporal type).  Bytes become a hex-encoded string.  Sets and
    :class:`OrderedMap` are folded into list / dict respectively.
    Non-string dict keys are not handled here; the caller validates first.
    """
    match data:
        case datetime.datetime() | datetime.date() | datetime.time():
            return _temporal_to_iso(data=data)
        case bytes():
            return data.hex()
        case OrderedMap() | dict():
            return {
                key: _to_jsonable(data=value) for key, value in data.items()
            }
        case set():
            items = [_to_jsonable(data=item) for item in data]
            items.sort(key=repr)
            return items
        case list():
            return [_to_jsonable(data=item) for item in data]
        case _:
            return data


@beartype
def format_json_value_text(data: Value) -> str:
    """Serialize *data* as a single-line JSON expression."""
    return json.dumps(obj=_to_jsonable(data=data), ensure_ascii=False)
