#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t, int>>{
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, std::nullptr_t, int>>{
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
    (void)my_data;
    return 0;
}
