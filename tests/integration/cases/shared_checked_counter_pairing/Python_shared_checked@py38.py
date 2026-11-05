
from typing import List, Tuple
class Counter:
    def __init__(self) -> None:
        self.seen: List[Tuple[str, float]] = []
    def accept(self, user: str, timestamp: float, /) -> bool:
        self.seen.append((user, timestamp))
        return user == "user_1"
counter = Counter()
reasons: List[str] = []
def check_result(actual: bool, expected: Tuple[bool, str], /) -> None:
    assert actual is expected[0]
    reasons.append(expected[1])
def run() -> None:
    check_result(counter.accept("user_1", 100.0), (True, "first"))
    check_result(counter.accept("user_2", 101.0), (False, "second"))
run()
assert counter.seen == [('user_1', 100.0), ('user_2', 101.0)]
assert reasons == ['first', 'second']
