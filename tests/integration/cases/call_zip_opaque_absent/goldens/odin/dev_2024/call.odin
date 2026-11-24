#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 1}
    assert(event_index < 2 && actual == expected[event_index])
    event_index += 1
}
process :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
verify_events :: proc() { assert(event_index == 2) }

main :: proc() {
process(1);
verify_events();
}
