from typing import Dict, Tuple, Union
my_data: Dict[str, Union[Tuple[int, ...], Dict[str, Tuple[int, ...]], Tuple[Union[int, str], ...]]] = {
    "numbers": (1, 2),
    "nested": {"inner": (3,)},
    "mixed": (4, "five"),
}
