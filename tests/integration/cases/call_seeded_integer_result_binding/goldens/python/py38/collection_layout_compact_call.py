_expected_events = (2, 42, 1, 42, 2, 142,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 6 and actual == _expected_events[_event_index]
    _event_index += 1
def make_widget(count: int) -> int:
    observe_event(1); observe_event(count)
    return count + 100
def consume(count: int) -> None:
    observe_event(2); observe_event(count)
def verify_events() -> None:
    assert _event_index == 6
my_data = 42
consume(count=my_data)
my_data = make_widget(count=42)
consume(count=my_data)
verify_events()
