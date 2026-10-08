from __future__ import annotations
from typing import Any
my_data: tuple[dict[str, tuple[dict[str, dict[str, int] | dict[str, Any]], ...]], ...] = (
    {"items": ({"inner": {"x": 1}}, {"inner": {}})},
    {"items": ({"inner": {"x": 2}}, {"inner": {}})},
)
