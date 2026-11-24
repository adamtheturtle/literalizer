from typing import Any, Tuple
import dataclasses
from typing import Any, Tuple, Union
@dataclasses.dataclass(frozen=True)
class Record1:
    item: int
@dataclasses.dataclass(frozen=True)
class Record2:
    item: None
@dataclasses.dataclass(frozen=True)
class Record0:
    integers: Tuple[Union[Tuple[Any, ...], Tuple[Record1, ...]], ...]
    nulls: Tuple[Union[Tuple[Any, ...], Tuple[Record2, ...]], ...]
    nested: Tuple[Union[Tuple[Union[Tuple[Any, ...], Tuple[Record1, ...]], ...], Tuple[Union[Tuple[Record1, ...], Tuple[Any, ...]], ...]], ...]
    reversed: Tuple[Union[Tuple[Record1, ...], Tuple[Any, ...]], ...]
my_data = Record0(
    integers=(
        (),
        (
            Record1(
                item=1,
            ),
        ),
    ),
    nulls=(
        (),
        (
            Record2(
                item=None,
            ),
        ),
    ),
    nested=(
        (
            (),
            (
                Record1(
                    item=2,
                ),
            ),
        ),
        (
            (
                Record1(
                    item=3,
                ),
            ),
            (),
        ),
    ),
    reversed=(
        (
            Record1(
                item=4,
            ),
        ),
        (),
    ),
)
