_expected_events = (1, -1, 1, -2, 1, -3,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 6 and actual == _expected_events[_event_index]
    _event_index += 1
def process(value: int) -> int:
    observe_event(1); observe_event(value)
    return value + 100
def verify_events() -> None:
    assert _event_index == 6
process(value=-1)
process(value=-2)
process(value=-3)
verify_events()
