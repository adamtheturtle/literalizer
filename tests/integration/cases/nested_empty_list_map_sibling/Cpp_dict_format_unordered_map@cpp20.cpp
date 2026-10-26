#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::unordered_map<std::string, std::vector<std::nullptr_t>>>{
    std::unordered_map<std::string, std::vector<std::nullptr_t>>{{"values", std::vector<std::nullptr_t>{}}},
    std::unordered_map<std::string, std::vector<std::nullptr_t>>{},
};
    (void)my_data;
    return 0;
}
