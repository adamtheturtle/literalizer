import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    scores: tuple[int, ...]
my_data = (
    Record0(scores=(1, 2)),
    Record0(scores=(3, 4)),
)
