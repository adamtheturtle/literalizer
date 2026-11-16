#+feature dynamic-literals
package main
event_index: int
observe_event :: proc(actual: int) {
    expected := [?]int{2, 0, 1, 1, 2, 101}
    assert(event_index < 6 && actual == expected[event_index])
    event_index += 1
}
make_widget :: proc(count: int) -> int { observe_event(1); observe_event(count); return count + 100 }
consume_widget :: proc(count: int) { observe_event(2); observe_event(count) }
verify_events :: proc() { assert(event_index == 6) }

main :: proc() {
my_data := 0
consume_widget(my_data);
my_data = make_widget(1)
consume_widget(my_data);
verify_events();
}
