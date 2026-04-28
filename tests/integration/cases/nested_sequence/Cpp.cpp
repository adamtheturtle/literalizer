#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
auto main() -> int {
auto my_data = std::vector<std::variant<bool, std::string, std::vector<int>, std::nullptr_t>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
    (void)my_data;
    return 0;
}
