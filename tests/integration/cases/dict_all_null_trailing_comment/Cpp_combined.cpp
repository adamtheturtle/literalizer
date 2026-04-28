#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::nullptr_t>{
    {"a", nullptr},
    {"b", nullptr},
    // trailing
};
(void)my_data;
my_data = std::map<std::string, std::nullptr_t>{
    {"a", nullptr},
    {"b", nullptr},
    // trailing
};
    (void)my_data;
    return 0;
}
