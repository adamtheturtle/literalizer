import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [2, 42, 1, 42, 2, 142];
    assert(eventIndex < 6 && actual == expected[eventIndex]);
    eventIndex++;
}
long make_widget(long count) { observeEvent(1); observeEvent(count); return count + 100; }
long make_widget(JSONValue count) { observeEvent(1); observeEvent(count.integer); return count.integer + 100; }
void consume_widget(long count) { observeEvent(2); observeEvent(count); }
void consume_widget(JSONValue count) { observeEvent(2); observeEvent(count.integer); }
void verify_events() { assert(eventIndex == 6); }
void main() {
auto my_data = JSONValue(42);
consume_widget(my_data);
my_data = make_widget(my_data); // note
consume_widget(my_data);
verify_events();
}
