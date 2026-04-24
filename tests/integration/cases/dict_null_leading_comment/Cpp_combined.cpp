#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
void check_() {
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
}
