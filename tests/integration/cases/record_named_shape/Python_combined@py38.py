from __future__ import annotations
from typing import Any, Dict, Tuple, Union
my_data: Tuple[Dict[str, Union[int, str, bool, Tuple[int, ...], Tuple[Any, ...]]], ...] = (
    {"id": 100, "description": "first task", "is_done": False, "blocks": (102, 103)},
    {"id": 101, "description": "second task", "is_done": True, "blocks": ()},
)
my_data = (
    {"id": 100, "description": "first task", "is_done": False, "blocks": (102, 103)},
    {"id": 101, "description": "second task", "is_done": True, "blocks": ()},
)
