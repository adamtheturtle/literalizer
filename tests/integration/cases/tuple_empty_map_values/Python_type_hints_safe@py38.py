from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[int | str, ...] | tuple[Any, ...]] = {
    "filled": (1, "value"),
    "empty": (),
}
