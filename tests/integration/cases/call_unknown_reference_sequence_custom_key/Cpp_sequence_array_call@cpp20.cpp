#include <array>
#include <cstddef>
#include <type_traits>
auto process(auto...) { return 0; }
int main() {
auto untyped_value = std::array<std::nullptr_t, 0>{};
process(std::array<std::common_type_t<decltype(untyped_value), decltype(untyped_value)>, 2>{untyped_value, untyped_value});
    return 0;
}
