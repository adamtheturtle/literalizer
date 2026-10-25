#include <initializer_list>
#include <vector>
#include <cstddef>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto unknown_value = std::vector<std::nullptr_t>{};
process(std::vector<typename std::common_type<decltype(unknown_value)>::type>{unknown_value});
    return 0;
}
