#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {1, 1};
    assert(event_index < 2 && actual == expected[event_index]);
    ++event_index;
}
static int process(int value) {
    observe_event(1); observe_event(value);
    return value + 100;
}
static void verify_events() { assert(event_index == 2); }
int main() {
process(1);
verify_events();
    return 0;
}
