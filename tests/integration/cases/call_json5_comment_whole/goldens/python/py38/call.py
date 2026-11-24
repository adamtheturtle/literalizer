_expected_events = (1, 42,)
_event_index = 0
def observe_event(actual: int, /) -> None:
    global _event_index
    assert _event_index < 2 and actual == _expected_events[_event_index]
    _event_index += 1
def f(a: int) -> int:
    observe_event(1); observe_event(a)
    return a + 100
def verify_events() -> None:
    assert _event_index == 2
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(a=42)
verify_events()
