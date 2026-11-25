import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 1];
    assert(eventIndex < 2 && actual == expected[eventIndex]);
    eventIndex++;
}
long process(long value) { observeEvent(1); observeEvent(value); return value + 100; }
long process(JSONValue value) { observeEvent(1); observeEvent(value.integer); return value.integer + 100; }
void verify_events() { assert(eventIndex == 2); }
void main() {
auto value = JSONValue(1);
process(value);
verify_events();
}
