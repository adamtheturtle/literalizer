import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 42, 2, 142];
    assert(eventIndex < 4 && actual == expected[eventIndex]);
    eventIndex++;
}
long process(long value) { observeEvent(1); observeEvent(value); return value + 100; }
long process(JSONValue value) { observeEvent(1); observeEvent(value.integer); return value.integer + 100; }
void emit(long value) { observeEvent(2); observeEvent(value); }
void verify_events() { assert(eventIndex == 4); }
void main() {
emit(process(42));
verify_events();
}
