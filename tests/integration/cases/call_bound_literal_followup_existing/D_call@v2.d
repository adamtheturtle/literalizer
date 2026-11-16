import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [2, 42, 1, 42, 2, 142];
    assert(eventIndex < 6 && actual == expected[eventIndex]);
    eventIndex++;
}
long make_widget(long value) { observeEvent(1); observeEvent(value); return value + 100; }
long make_widget(JSONValue value) { observeEvent(1); observeEvent(value.integer); return value.integer + 100; }
void consume(long value) { observeEvent(2); observeEvent(value); }
void consume(JSONValue value) { observeEvent(2); observeEvent(value.integer); }
void verify_events() { assert(eventIndex == 6); }
void main() {
auto my_data = JSONValue(42);
consume(my_data);
my_data = make_widget(42);
consume(my_data);
verify_events();
}
