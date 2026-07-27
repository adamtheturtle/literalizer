from __future__ import annotations
from typing import Any, Union
my_data: tuple[dict[str, Union[int, str, tuple[Any, ...]]], ...] = (
    {"id": 1, "label": "first", "tags": ()},
    {"id": 2, "label": "second", "tags": ()},
    {"id": 3, "label": "third", "tags": ()},
)
