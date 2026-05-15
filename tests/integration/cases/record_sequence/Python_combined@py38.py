from __future__ import annotations
from typing import Any, Dict, Tuple, Union
my_data: Tuple[Dict[str, Union[int, str, Tuple[Any, ...]]], ...] = (
    {"id": 1, "label": "first", "tags": ()},
    {"id": 2, "label": "second", "tags": ()},
    {"id": 3, "label": "third", "tags": ()},
)
my_data = (
    {"id": 1, "label": "first", "tags": ()},
    {"id": 2, "label": "second", "tags": ()},
    {"id": 3, "label": "third", "tags": ()},
)
