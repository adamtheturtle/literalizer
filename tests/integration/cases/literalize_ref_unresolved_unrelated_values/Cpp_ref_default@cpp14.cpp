#include <initializer_list>
#include <vector>
#include <cstddef>
#include <cstdlib>

template <typename Actual, typename Expected>
void assert_equal(const Actual& actual, const Expected& expected) {
    if (actual != expected) { std::abort(); }
}
int main() {
auto a = 0;
auto my_data = std::vector<int>{
    std::move_if_noexcept(a),
    1,
};
auto expected_data = std::vector<int>{
    0,
    1,
};
assert_equal(my_data, expected_data);
    return 0;
}
