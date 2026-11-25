#include <cstddef>
#include <map>
#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::pair<std::string, std::nullptr_t>>, int>>{
    {"a", std::vector<std::pair<std::string, std::nullptr_t>>{}},
    {"b", 1},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::vector<std::pair<std::string, std::nullptr_t>>, int>>{
    {"a", std::vector<std::pair<std::string, std::nullptr_t>>{}},
    {"b", 1},
};
    (void)my_data;
    return 0;
}
