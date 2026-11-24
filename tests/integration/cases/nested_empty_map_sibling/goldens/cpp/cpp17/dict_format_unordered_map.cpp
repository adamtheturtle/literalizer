#include <cstddef>
#include <string>
#include <unordered_map>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::unordered_map<std::string, std::unordered_map<std::string, std::nullptr_t>>, std::unordered_map<std::string, std::nullptr_t>>>{
    std::unordered_map<std::string, std::unordered_map<std::string, std::nullptr_t>>{{"mapping", std::unordered_map<std::string, std::nullptr_t>{}}},
    std::unordered_map<std::string, std::unordered_map<std::string, std::nullptr_t>>{},
};
    (void)my_data;
    return 0;
}
