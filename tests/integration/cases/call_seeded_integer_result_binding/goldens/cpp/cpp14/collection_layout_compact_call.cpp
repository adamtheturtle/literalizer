#include <cassert>
#include <array>
#include <cstddef>
#include <iterator>
int main() {
const std::array<int, 6> expected_events{{2, 42, 1, 42, 2, 142}};
std::ptrdiff_t event_index = 0;
const auto observe_event = [&expected_events, &event_index](int actual) {
    assert(event_index < 6 && actual == *std::next(expected_events.cbegin(), event_index));
    ++event_index;
};
const auto make_widget = [&observe_event](int argument) {
    observe_event(1); observe_event(argument);
    return argument + 100;
};
const auto consume = [&observe_event](int argument) { observe_event(2); observe_event(argument); };
const auto verify_events = [&event_index] { assert(event_index == 6); };
auto my_data = 42;
consume(my_data);
my_data = make_widget(42);
consume(my_data);
verify_events();
    return 0;
}
