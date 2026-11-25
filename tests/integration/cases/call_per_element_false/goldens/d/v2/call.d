import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 1];
    assert(eventIndex < 2 && actual == expected[eventIndex]);
    eventIndex++;
}
long process(long data) { observeEvent(1); observeEvent(data); return data + 100; }
long process(JSONValue data) { observeEvent(1); observeEvent(data.integer); return data.integer + 100; }
void verify_events() { assert(eventIndex == 2); }
void main() {
process(1);
verify_events();
}
