#include <cstddef>
#include <string>
#include <unordered_map>
#include <variant>
int main() {
auto my_data = std::unordered_map<std::string, std::unordered_map<std::string, std::variant<int, std::string, std::nullptr_t>>>{
    {"outer", std::unordered_map<std::string, std::variant<int, std::string, std::nullptr_t>>{{"a", 1}, {"b", "x"}, {"c", nullptr}}},
};
    (void)my_data;
    return 0;
}
