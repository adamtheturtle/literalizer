#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<std::nullptr_t>>>>{
    {"a", std::vector<std::variant<int, std::vector<std::nullptr_t>>>{1, std::vector<std::nullptr_t>{}}},
};
    (void)my_data;
    return 0;
}
