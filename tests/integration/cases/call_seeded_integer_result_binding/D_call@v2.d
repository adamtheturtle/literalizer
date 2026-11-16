import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [2, 42, 1, 42, 2, 142];
    assert(eventIndex < 6 && actual == expected[eventIndex]);
    eventIndex++;
}
long make_widget(long count) { observeEvent(1); observeEvent(count); return count + 100; }
long make_widget(JSONValue count) { observeEvent(1); observeEvent(count.integer); return count.integer + 100; }
void consume(long count) { observeEvent(2); observeEvent(count); }
void consume(JSONValue count) { observeEvent(2); observeEvent(count.integer); }
void verify_events() { assert(eventIndex == 6); }
void main() {
auto my_data = JSONValue(42);
consume(my_data);
my_data = make_widget(42);
consume(my_data);
verify_events();
}
