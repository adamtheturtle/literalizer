#include <initializer_list>
#include <vector>
#include <cstddef>
#include <type_traits>
auto process(auto...) { return 0; }
int main() {
auto unknown_value = std::vector<std::nullptr_t>{};
process(std::vector<typename std::common_type<decltype(unknown_value)>::type>{unknown_value});
    return 0;
}
