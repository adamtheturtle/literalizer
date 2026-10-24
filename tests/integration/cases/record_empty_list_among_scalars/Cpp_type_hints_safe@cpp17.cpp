#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<std::nullptr_t>>>>{
    {"a", std::vector<std::variant<int, std::vector<std::nullptr_t>>>{1, std::vector<std::nullptr_t>{}}},
};
    (void)my_data;
    return 0;
}
