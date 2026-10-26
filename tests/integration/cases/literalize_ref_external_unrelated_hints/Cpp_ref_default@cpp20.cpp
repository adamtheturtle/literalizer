#include <initializer_list>
#include <vector>
#include <type_traits>
#include <cstddef>
#include <variant>
#include <cstdlib>

template <typename Actual, typename Expected>
void assert_equal(const Actual& actual, const Expected& expected) {
    if (actual != expected) { std::abort(); }
}
int main() {
auto missing = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move_if_noexcept(missing);
auto expected_data = std::vector<int>{
    1,
    2,
};
assert_equal(my_data, expected_data);
    return 0;
}
