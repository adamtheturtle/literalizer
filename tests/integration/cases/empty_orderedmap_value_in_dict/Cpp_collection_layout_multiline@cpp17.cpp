#include <initializer_list>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::pair<std::string, std::nullptr_t>>, int>>{
    {"a", std::vector<std::pair<std::string, std::nullptr_t>>{}},
    {"b", 1},
};
    (void)my_data;
    return 0;
}
