#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<int, double, bool, std::string>>{
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
my_data = std::vector<std::variant<int, double, bool, std::string>>{
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
}
