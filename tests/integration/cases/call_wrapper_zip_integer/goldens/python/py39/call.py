_expected_events = (1, 1, 2, 101, 3, 42,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 6 and actual == _expected_events[_event_index]
    _event_index += 1
def process(value: int) -> int:
    observe_event(1); observe_event(value)
    return value + 100
def emit(actual: int, zipped: int, /) -> None:
    observe_event(2); observe_event(actual)
    observe_event(3); observe_event(zipped)
def verify_events() -> None:
    assert _event_index == 6
emit(process(value=1), 42)
verify_events()
