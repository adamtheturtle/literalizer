#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int, bool, std::nullptr_t>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", "2024-01-15"},
    {"last_login", "2024-01-15T12:30:00+00:00"},
    {"avatar", "48656c6c6f"},
};
    (void)my_data;
    return 0;
}
