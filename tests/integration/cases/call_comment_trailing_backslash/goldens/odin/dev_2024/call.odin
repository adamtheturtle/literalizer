#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 1, 1, 2}
    assert(event_index < 4 && actual == expected[event_index])
    event_index += 1
}
process :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
verify_events :: proc() { assert(event_index == 4) }

main :: proc() {
process(1);  // trail \ .
process(2);  // second
verify_events();
}
