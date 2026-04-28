#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
auto main() -> int {
    static const auto my_data = std::map<std::string, std::variant<std::string, int, bool, std::nullptr_t>>{
        {"name", "Alice"},
        {"age", 30},
        {"active", true},
        {"score", nullptr},
    };
    (void)my_data;
    return 0;
}
