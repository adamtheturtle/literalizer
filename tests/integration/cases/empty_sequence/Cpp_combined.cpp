#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
const auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::map<std::string, std::nullptr_t>>>{
    std::vector<std::nullptr_t>{},
    std::map<std::string, std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::map<std::string, std::nullptr_t>>>{
    std::vector<std::nullptr_t>{},
    std::map<std::string, std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
