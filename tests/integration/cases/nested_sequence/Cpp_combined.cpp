#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<bool, std::string, std::vector<int>, std::monostate>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
my_data = std::vector<std::variant<bool, std::string, std::vector<int>, std::monostate>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
}
