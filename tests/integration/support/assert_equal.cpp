#include <cstdlib>

template <typename Actual, typename Expected>
void assert_equal(const Actual& actual, const Expected& expected) {
    if (actual != expected) { std::abort(); }
}
