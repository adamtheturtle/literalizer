#include <cstddef>
#include <vector>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto untyped_value = std::vector<std::nullptr_t>{};
process(std::vector<std::common_type_t<decltype(untyped_value), decltype(untyped_value)>>{untyped_value, untyped_value});
    return 0;
}
