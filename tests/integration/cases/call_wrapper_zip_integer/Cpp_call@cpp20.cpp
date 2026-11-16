#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {1, 1, 2, 101, 3, 42};
    assert(event_index < 6 && actual == expected[event_index]);
    ++event_index;
}
static int process(int value) {
    observe_event(1); observe_event(value);
    return value + 100;
}
static void emit(int actual, int zipped) { observe_event(2); observe_event(actual); observe_event(3); observe_event(zipped); }
static void verify_events() { assert(event_index == 6); }
int main() {
emit(process(1), 42);
verify_events();
    return 0;
}
