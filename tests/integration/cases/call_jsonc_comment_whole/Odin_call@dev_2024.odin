#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 42}
    assert(event_index < 2 && actual == expected[event_index])
    event_index += 1
}
f :: proc(a: int) -> int { observe_event(1); observe_event(a); return a + 100 }
verify_events :: proc() { assert(event_index == 2) }

main :: proc() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
verify_events();
}
