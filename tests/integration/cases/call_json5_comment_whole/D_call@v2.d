import std.json;
int eventIndex;
void observeEvent(long actual) {
    const long[] expected = [1, 42];
    assert(eventIndex < 2 && actual == expected[eventIndex]);
    eventIndex++;
}
long f(long a) { observeEvent(1); observeEvent(a); return a + 100; }
long f(JSONValue a) { observeEvent(1); observeEvent(a.integer); return a.integer + 100; }
void verify_events() { assert(eventIndex == 2); }
void main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
verify_events();
}
