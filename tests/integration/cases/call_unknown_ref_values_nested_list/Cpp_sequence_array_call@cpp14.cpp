#include <initializer_list>
#include <array>
#include <cstddef>
#include <type_traits>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto unknown_value = std::array<std::nullptr_t, 0>{};
process(std::array<std::common_type_t<decltype(unknown_value)>, 1>{unknown_value});
    return 0;
}
