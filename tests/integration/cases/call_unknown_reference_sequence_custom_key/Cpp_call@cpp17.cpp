#include <initializer_list>
#include <vector>
#include <cstddef>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto untyped_value = std::vector<std::nullptr_t>{};
process(std::vector<typename std::common_type<decltype(untyped_value), decltype(untyped_value)>::type>{untyped_value, untyped_value});
    return 0;
}
