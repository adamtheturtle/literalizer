from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[dict[str, Any], ...] | tuple[tuple[int, ...], ...] | tuple[tuple[tuple[int, ...], ...], ...]] = {
    "single_map": ({},),
    "single_list": ((1,),),
    "single_deep": (((2,),),),
}
