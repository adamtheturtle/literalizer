import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 1, 1, 2];
    assert(eventIndex < 4 && actual == expected[eventIndex]);
    eventIndex++;
}
long process(long value) { observeEvent(1); observeEvent(value); return value + 100; }
long process(JSONValue value) { observeEvent(1); observeEvent(value.integer); return value.integer + 100; }
void verify_events() { assert(eventIndex == 4); }
void main() {
process(1);
process(2);
verify_events();
}
