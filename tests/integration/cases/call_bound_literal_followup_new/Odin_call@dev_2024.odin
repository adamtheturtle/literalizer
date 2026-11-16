#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{1, 42, 2, 142}
    assert(event_index < 4 && actual == expected[event_index])
    event_index += 1
}
make_widget :: proc(value: int) -> int { observe_event(1); observe_event(value); return value + 100 }
consume :: proc(value: int) { observe_event(2); observe_event(value) }
verify_events :: proc() { assert(event_index == 4) }

main :: proc() {
my_data := make_widget(42)
consume(my_data);
verify_events();
}
