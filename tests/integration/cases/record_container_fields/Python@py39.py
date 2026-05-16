from __future__ import annotations
from typing import Any
my_data: tuple[dict[str, int | dict[str, Any] | dict[str, str] | set[str] | set[Any]], ...] = (
    {"id": 1, "empty_map": {}, "int_map": {1: "a"}, "full_set": {"x", "y"}, "empty_set": set()},
    {"id": 2, "empty_map": {}, "int_map": {1: "b"}, "full_set": {"x"}, "empty_set": set()},
)
