from __future__ import annotations
from typing import Any, Dict, Tuple
my_data: Dict[str, Tuple[int | Tuple[Any, ...], ...] | Tuple[int | Tuple[str, ...], ...]] = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
my_data = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
