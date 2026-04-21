#include <initializer_list>
#include <string>
#include <map>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
my_data = std::map<std::string, std::variant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
}
