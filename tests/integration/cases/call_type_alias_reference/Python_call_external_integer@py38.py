_expected_events = (1, 1,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 2 and actual == _expected_events[_event_index]
    _event_index += 1
def process(value: int) -> int:
    observe_event(1); observe_event(value)
    return value + 100
def verify_events() -> None:
    assert _event_index == 2
value = 1
process(value=value)
verify_events()
