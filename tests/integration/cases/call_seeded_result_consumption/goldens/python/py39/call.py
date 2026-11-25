_expected_events = (2, 0, 1, 1, 2, 101,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 6 and actual == _expected_events[_event_index]
    _event_index += 1
def make_widget(count: int) -> int:
    observe_event(1); observe_event(count)
    return count + 100
def consume_widget(count: int) -> None:
    observe_event(2); observe_event(count)
def verify_events() -> None:
    assert _event_index == 6
my_data = 0
consume_widget(count=my_data)
my_data = make_widget(count=1)
consume_widget(count=my_data)
verify_events()
