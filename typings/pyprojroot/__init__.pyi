"""Correct pyprojroot 0.3.0's unparameterized PathLike annotations."""

from collections.abc import Callable, Iterable
from os import PathLike
from pathlib import Path

type _PathType = PathLike[str] | str
type _CriterionType = (
    Callable[[_PathType], bool]
    | Callable[[Path], bool]
    | _PathType
    | Path
    | Iterable[Callable[[_PathType], bool]]
    | Iterable[Callable[[Path], bool]]
)

def find_root(criterion: _CriterionType, start: _PathType | None = None) -> Path: ...
def has_file(file: _PathType) -> Callable[[Path], bool]: ...
