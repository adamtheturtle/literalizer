#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{2, 42, 1, 42, 2, 142}
    assert(event_index < 6 && actual == expected[event_index])
    event_index += 1
}
make_widget :: proc(count: int) -> int { observe_event(1); observe_event(count); return count + 100 }
consume_widget :: proc(count: int) { observe_event(2); observe_event(count) }
verify_events :: proc() { assert(event_index == 6) }

main :: proc() {
my_data := 42
consume_widget(my_data);
my_data = make_widget(42) // note
// extra
consume_widget(my_data);
verify_events();
}
