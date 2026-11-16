#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {1, 42};
    assert(event_index < 2 && actual == expected[event_index]);
    ++event_index;
}
static int f(int a) {
    observe_event(1); observe_event(a);
    return a + 100;
}
static void verify_events() { assert(event_index == 2); }
int main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
verify_events();
    return 0;
}
