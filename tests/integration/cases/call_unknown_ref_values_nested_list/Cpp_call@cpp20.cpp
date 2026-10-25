#include <initializer_list>
#include <vector>
#include <cstddef>
#include <type_traits>
auto process(auto...) { return 0; }
int main() {
auto unknown_value = std::vector<std::nullptr_t>{};
process(std::vector<std::common_type_t<decltype(unknown_value)>>{unknown_value});
    return 0;
}
