from __future__ import annotations
from typing import Any, Dict, Set, Tuple, Union
my_data: Tuple[Dict[str, Union[int, Dict[str, Any], Dict[str, str], Set[str], Set[Any]]], ...] = (
    {"id": 1, "empty_map": {}, "int_map": {1: "a"}, "full_set": {"x", "y"}, "empty_set": set()},
    {"id": 2, "empty_map": {}, "int_map": {1: "b"}, "full_set": {"x"}, "empty_set": set()},
)
my_data = (
    {"id": 1, "empty_map": {}, "int_map": {1: "a"}, "full_set": {"x", "y"}, "empty_set": set()},
    {"id": 2, "empty_map": {}, "int_map": {1: "b"}, "full_set": {"x"}, "empty_set": set()},
)
