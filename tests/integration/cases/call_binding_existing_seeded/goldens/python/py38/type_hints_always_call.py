from __future__ import annotations
_expected_events = (1, 42, 1, 42, 1, 142,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 6 and actual == _expected_events[_event_index]
    _event_index += 1
def make_widget(count: int) -> int:
    observe_event(1); observe_event(count)
    return count + 100
def verify_events() -> None:
    assert _event_index == 6
my_data: int = 42
make_widget(count=my_data)
my_data = make_widget(count=my_data)
make_widget(count=my_data)
verify_events()
