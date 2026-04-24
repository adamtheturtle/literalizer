#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::vector<std::variant<int, std::vector<std::nullptr_t>>>, std::vector<std::variant<int, std::vector<std::string>>>>>{
    {"lint", std::vector<std::variant<int, std::vector<std::nullptr_t>>>{2, std::vector<std::nullptr_t>{}}},
    {"test", std::vector<std::variant<int, std::vector<std::string>>>{5, std::vector<std::string>{"compile"}}},
};
    (void)my_data;
}
