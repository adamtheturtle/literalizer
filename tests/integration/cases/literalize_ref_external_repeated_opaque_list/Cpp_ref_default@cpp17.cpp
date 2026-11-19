#include <cstddef>
#include <vector>
#include <type_traits>
#include <cstdlib>
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
((my_data) != (expected_data) ? std::abort() : static_cast<void>(0));
    return 0;
}
