import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    payload: str
my_data = Record0(
    payload="48656c6c6f",
)
