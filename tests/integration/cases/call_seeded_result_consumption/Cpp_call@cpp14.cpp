#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {2, 0, 1, 1, 2, 101};
    assert(event_index < 6 && actual == expected[event_index]);
    ++event_index;
}
static int make_widget(int count) {
    observe_event(1); observe_event(count);
    return count + 100;
}
static void consume_widget(int count) { observe_event(2); observe_event(count); }
static void verify_events() { assert(event_index == 6); }
int main() {
auto my_data = 0;
consume_widget(my_data);
my_data = make_widget(1);
consume_widget(my_data);
verify_events();
    return 0;
}
