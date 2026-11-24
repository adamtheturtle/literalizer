#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>>{
    {"server", std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>{
        {"host", "localhost"},
        {"port", nullptr},  // not configured yet
        {"debug", true},
    }},
};
(void)my_data;
my_data = std::map<std::string, std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>>{
    {"server", std::map<std::string, std::variant<std::string, std::nullptr_t, bool>>{
        {"host", "localhost"},
        {"port", nullptr},  // not configured yet
        {"debug", true},
    }},
};
    (void)my_data;
    return 0;
}
