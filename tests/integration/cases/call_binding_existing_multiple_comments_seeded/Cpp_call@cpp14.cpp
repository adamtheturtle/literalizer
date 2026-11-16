#include <cassert>
static int event_index = 0;
static void observe_event(int actual) {
    const int expected[] = {2, 42, 1, 42, 2, 142};
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
auto my_data = 42;
consume_widget(my_data);
my_data = make_widget(my_data); // note
// extra
consume_widget(my_data);
verify_events();
    return 0;
}
