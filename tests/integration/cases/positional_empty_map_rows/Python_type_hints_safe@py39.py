from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[tuple[int | str, ...] | tuple[Any, ...], ...] | tuple[tuple[Any, ...] | tuple[int | str, ...], ...]] = {
    "first": ((1, "value"), ()),
    "second": ((), (2, "other")),
}
