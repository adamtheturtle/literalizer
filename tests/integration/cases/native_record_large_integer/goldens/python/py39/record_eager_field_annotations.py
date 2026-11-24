import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    value: int
my_data = Record0(
    value=2147483648,
)
