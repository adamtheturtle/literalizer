_expected_events = (1, 42, 2, 142,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 4 and actual == _expected_events[_event_index]
    _event_index += 1
def make_widget(value: int) -> int:
    observe_event(1); observe_event(value)
    return value + 100
def consume(value: int) -> None:
    observe_event(2); observe_event(value)
def verify_events() -> None:
    assert _event_index == 4
my_data = make_widget(value=42)
consume(value=my_data)
verify_events()
