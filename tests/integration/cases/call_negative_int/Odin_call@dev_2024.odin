#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, -1, 1, -2, 1, -3}
    assert(event_index < 6 && actual == expected[event_index])
    event_index += 1
}
process :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
verify_events :: proc() { assert(event_index == 6) }

main :: proc() {
process(-1);
process(-2);
process(-3);
verify_events();
}
