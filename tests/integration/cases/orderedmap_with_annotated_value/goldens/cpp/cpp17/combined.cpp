#include <cstddef>
#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::vector<std::nullptr_t>, int>>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", 1},
};
(void)my_data;
my_data = std::vector<std::pair<std::string, std::variant<std::vector<std::nullptr_t>, int>>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", 1},
};
    (void)my_data;
    return 0;
}
