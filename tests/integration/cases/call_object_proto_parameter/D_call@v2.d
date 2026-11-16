import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 1];
    assert(eventIndex < 2 && actual == expected[eventIndex]);
    eventIndex++;
}
long capture(long __proto__) { observeEvent(1); observeEvent(__proto__); return __proto__ + 100; }
long capture(JSONValue __proto__) { observeEvent(1); observeEvent(__proto__.integer); return __proto__.integer + 100; }
void verify_events() { assert(eventIndex == 2); }
void main() {
capture(1);
verify_events();
}
