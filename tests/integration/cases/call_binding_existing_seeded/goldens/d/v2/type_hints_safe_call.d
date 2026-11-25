import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 42, 1, 42, 1, 142];
    assert(eventIndex < 6 && actual == expected[eventIndex]);
    eventIndex++;
}
long make_widget(long count) { observeEvent(1); observeEvent(count); return count + 100; }
long make_widget(JSONValue count) { observeEvent(1); observeEvent(count.integer); return count.integer + 100; }
void verify_events() { assert(eventIndex == 6); }
void main() {
auto my_data = JSONValue(42);
make_widget(my_data);
my_data = make_widget(my_data);
make_widget(my_data);
verify_events();
}
