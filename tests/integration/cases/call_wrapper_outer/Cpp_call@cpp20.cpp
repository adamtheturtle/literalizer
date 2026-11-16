#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {1, 42, 2, 142};
    assert(event_index < 4 && actual == expected[event_index]);
    ++event_index;
}
static int process(int value) {
    observe_event(1); observe_event(value);
    return value + 100;
}
static void emit(int value) { observe_event(2); observe_event(value); }
static void verify_events() { assert(event_index == 4); }
int main() {
emit(process(42));
verify_events();
    return 0;
}
