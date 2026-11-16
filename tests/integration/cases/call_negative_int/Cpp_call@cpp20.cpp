#include <cassert>
#include <array>
#include <cstddef>
#include <iterator>
int main() {
const std::array<int, 6> expected_events{{1, -1, 1, -2, 1, -3}};
std::ptrdiff_t event_index = 0;
const auto observe_event = [&expected_events, &event_index](int actual) {
    assert(event_index < 6 && actual == *std::next(expected_events.cbegin(), event_index));
    ++event_index;
};
const auto process = [&observe_event](int argument) {
    observe_event(1); observe_event(argument);
    return argument + 100;
};
const auto verify_events = [&event_index] { assert(event_index == 6); };
process(-1);
process(-2);
process(-3);
verify_events();
    return 0;
}
