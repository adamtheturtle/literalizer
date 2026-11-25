#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, std::map<std::string, std::variant<int, std::string>>>, std::map<std::string, std::nullptr_t>>>{
    std::map<std::string, std::map<std::string, std::variant<int, std::string>>>{{"nested", std::map<std::string, std::variant<int, std::string>>{{"count", 1}, {"name", "value"}}}},
    std::map<std::string, std::map<std::string, std::variant<int, std::string>>>{},
};
    (void)my_data;
    return 0;
}
