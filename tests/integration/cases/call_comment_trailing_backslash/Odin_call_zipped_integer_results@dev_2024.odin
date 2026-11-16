#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42}
    assert(event_index < 12 && actual == expected[event_index])
    event_index += 1
}
process :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
emit :: proc(actual: int, zipped: int) { observe_event(2); observe_event(actual); observe_event(3); observe_event(zipped) }
verify_events :: proc() { assert(event_index == 12) }

main :: proc() {
emit(process(1), 41);
emit(process(2), 42);
verify_events();
}
