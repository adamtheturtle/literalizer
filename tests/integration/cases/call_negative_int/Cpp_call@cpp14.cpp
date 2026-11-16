#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {1, -1, 1, -2, 1, -3};
    assert(event_index < 6 && actual == expected[event_index]);
    ++event_index;
}
static int process(int value) {
    observe_event(1); observe_event(value);
    return value + 100;
}
static void verify_events() { assert(event_index == 6); }
int main() {
process(-1);
process(-2);
process(-3);
verify_events();
    return 0;
}
