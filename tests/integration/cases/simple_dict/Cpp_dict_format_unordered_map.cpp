#include <initializer_list>
#include <string>
#include <cstddef>
#include <unordered_map>
#include <variant>
void check_() {
auto my_data = std::unordered_map<std::string, std::variant<std::string, int, bool, std::monostate>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
};
}
