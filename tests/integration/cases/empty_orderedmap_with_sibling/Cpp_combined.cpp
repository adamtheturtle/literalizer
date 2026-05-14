#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::pair<std::string, std::nullptr_t>>, std::vector<std::nullptr_t>>>{
    std::vector<std::pair<std::string, std::nullptr_t>>{},
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::variant<std::vector<std::pair<std::string, std::nullptr_t>>, std::vector<std::nullptr_t>>>{
    std::vector<std::pair<std::string, std::nullptr_t>>{},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
