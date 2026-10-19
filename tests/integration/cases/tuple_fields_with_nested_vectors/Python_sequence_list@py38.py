from __future__ import annotations
from typing import Any
my_data: dict[str, list[int | list[Any]] | list[int | list[str]]] = {
    "lint": [2, []],
    "test": [5, ["compile"]],
    "package": [7, ["link", "test"]],
}
