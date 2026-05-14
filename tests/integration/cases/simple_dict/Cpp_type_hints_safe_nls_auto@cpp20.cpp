#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, long, bool, std::nullptr_t>>{
    {"name", "Alice"},
    {"age", 30L},
    {"active", true},
    {"score", nullptr},
};
    (void)my_data;
    return 0;
}
