#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<int, std::string, bool, std::monostate>>{
    1,
    "hello",
    true,
    nullptr,
};
my_data = std::vector<std::variant<int, std::string, bool, std::monostate>>{
    1,
    "hello",
    true,
    nullptr,
};
}
