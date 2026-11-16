#include <cassert>
#include <array>
#include <cstddef>
#include <iterator>
int main() {
const std::array<int, 4> expected_events{{1, 42, 2, 142}};
std::ptrdiff_t event_index = 0;
const auto observe_event = [&expected_events, &event_index](int actual) {
    assert(event_index < 4 && actual == *std::next(expected_events.cbegin(), event_index));
    ++event_index;
};
const auto process = [&observe_event](int argument) {
    observe_event(1); observe_event(argument);
    return argument + 100;
};
const auto emit = [&observe_event](int argument) { observe_event(2); observe_event(argument); };
const auto verify_events = [&event_index] { assert(event_index == 4); };
emit(process(42));
verify_events();
    return 0;
}
