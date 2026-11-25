import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 1, 2, 101, 3, 42];
    assert(eventIndex < 6 && actual == expected[eventIndex]);
    eventIndex++;
}
long process(long value) { observeEvent(1); observeEvent(value); return value + 100; }
long process(JSONValue value) { observeEvent(1); observeEvent(value.integer); return value.integer + 100; }
void emit(long actual, long zipped) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped); }
void verify_events() { assert(eventIndex == 6); }
void main() {
emit(process(1), 42);
verify_events();
}
