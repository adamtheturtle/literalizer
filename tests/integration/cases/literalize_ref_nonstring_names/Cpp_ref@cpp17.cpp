#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
#include <vector>
#include <variant>
int main() {
auto actual = std::map<std::string, std::variant<int, std::nullptr_t, std::string>>{
    {"_", "_"},
};
auto my_data = std::vector<std::map<std::string, std::variant<int, std::nullptr_t, std::string>>>{
    std::map<std::string, std::variant<int, std::nullptr_t, std::string>>{{"$ref", 1}},
    std::map<std::string, std::variant<int, std::nullptr_t, std::string>>{{"$ref", nullptr}},
    std::move(actual),
};
    (void)my_data;
    return 0;
}
