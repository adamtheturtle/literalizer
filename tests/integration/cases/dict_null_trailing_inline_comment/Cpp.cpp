#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
};
}
