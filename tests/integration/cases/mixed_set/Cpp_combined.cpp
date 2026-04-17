#include <initializer_list>
#include <string>
#include <variant>
void check_() {
auto my_data = std::initializer_list<std::variant<bool, int, std::string>>{
    true,
    42,
    "apple",
};
my_data = std::initializer_list<std::variant<bool, int, std::string>>{
    true,
    42,
    "apple",
};
}
