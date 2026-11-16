_expected_events = (1, 1,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 2 and actual == _expected_events[_event_index]
    _event_index += 1
def process(data: int) -> int:
    observe_event(1); observe_event(data)
    return data + 100
def verify_events() -> None:
    assert _event_index == 2
process(data=1)
verify_events()
