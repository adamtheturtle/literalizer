from __future__ import annotations
from typing import Any
my_data: tuple[dict[str, dict[str, dict[str, int]] | dict[str, dict[str, Any]]], ...] = (
    {"outer": {"inner": {"x": 1}}},
    {"outer": {"inner": {}}},
)
