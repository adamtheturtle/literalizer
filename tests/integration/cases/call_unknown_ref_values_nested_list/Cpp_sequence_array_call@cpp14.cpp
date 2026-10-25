#include <initializer_list>
#include <array>
#include <cstddef>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto unknown_value = std::array<std::nullptr_t, 0>{};
process(std::array<typename std::common_type<decltype(unknown_value)>::type, 1>{unknown_value});
    return 0;
}
