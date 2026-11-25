#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 42, 2, 142}
    assert(event_index < 4 && actual == expected[event_index])
    event_index += 1
}
process :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
emit :: proc(value: int) { observe_event(2); observe_event(value) }
verify_events :: proc() { assert(event_index == 4) }

main :: proc() {
emit(process(42));
verify_events();
}
