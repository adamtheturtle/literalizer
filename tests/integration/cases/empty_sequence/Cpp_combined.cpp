#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::map<std::string, std::nullptr_t>>>{
    std::vector<std::nullptr_t>{},
    std::map<std::string, std::nullptr_t>{},
};
my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::map<std::string, std::nullptr_t>>>{
    std::vector<std::nullptr_t>{},
    std::map<std::string, std::nullptr_t>{},
};
}
