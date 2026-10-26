#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::variant<int, std::string, std::nullptr_t>>>{
    {"outer", std::map<std::string, std::variant<int, std::string, std::nullptr_t>>{{"a", 1}, {"b", "x"}, {"c", nullptr}}},
};
    (void)my_data;
    return 0;
}
