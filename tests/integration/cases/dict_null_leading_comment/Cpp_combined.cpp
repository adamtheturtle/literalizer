#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t>>{
    // comment
    {"name", "Alice"},
    {"score", nullptr},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, std::nullptr_t>>{
    // comment
    {"name", "Alice"},
    {"score", nullptr},
};
    (void)my_data;
    return 0;
}
