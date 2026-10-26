#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
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
