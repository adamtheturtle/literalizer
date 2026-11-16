#include <cstdlib>

template <typename Actual, typename Expected>
void assert_equal(const Actual& actual, const Expected& expected) {
    if (actual != expected) { std::abort(); }
}
int main() {
auto my_data = 0;
auto shared = 1;
assert_equal(my_data, 0);
my_data = shared;
auto expected_data = 1;
assert_equal(my_data, expected_data);
    return 0;
}
