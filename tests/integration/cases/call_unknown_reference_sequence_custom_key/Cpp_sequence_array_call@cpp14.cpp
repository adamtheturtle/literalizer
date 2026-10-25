#include <initializer_list>
#include <array>
#include <cstddef>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto untyped_value = std::array<std::nullptr_t, 0>{};
process(std::array<typename std::common_type<decltype(untyped_value), decltype(untyped_value)>::type, 2>{untyped_value, untyped_value});
    return 0;
}
