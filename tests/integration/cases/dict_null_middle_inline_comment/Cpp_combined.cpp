#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
    {"debug", true},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
    {"debug", true},
};
    (void)my_data;
    return 0;
}
