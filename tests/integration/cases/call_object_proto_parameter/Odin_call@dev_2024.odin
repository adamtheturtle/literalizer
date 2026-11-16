#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 1}
    assert(event_index < 2 && actual == expected[event_index])
    event_index += 1
}
capture :: proc(__proto__: int) -> int { observe_event(1); observe_event(__proto__); return __proto__ + 100 }
verify_events :: proc() { assert(event_index == 2) }

main :: proc() {
capture(1);
verify_events();
}
