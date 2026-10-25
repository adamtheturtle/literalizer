#include <initializer_list>
#include <vector>
#include <type_traits>
#include <cstddef>
#include <cstdlib>

template <typename Actual, typename Expected>
void assert_equal(const Actual& actual, const Expected& expected) {
    if (actual != expected) { std::abort(); }
}
int main() {
auto item = std::vector<std::nullptr_t>{};
auto my_data = std::vector<std::common_type_t<decltype(item), decltype(item)>>{
    item,
    item,
};
auto expected_data = std::vector<std::vector<std::nullptr_t>>{
    std::vector<std::nullptr_t>{},
    std::vector<std::nullptr_t>{},
};
assert_equal(my_data, expected_data);
    return 0;
}
