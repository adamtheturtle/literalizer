#include <initializer_list>
#include <string>
#include <cstddef>
#include <unordered_map>
#include <variant>
int main() {
auto my_data = std::unordered_map<std::string, std::variant<std::string, int, bool, std::nullptr_t>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
};
    (void)my_data;
    return 0;
}
