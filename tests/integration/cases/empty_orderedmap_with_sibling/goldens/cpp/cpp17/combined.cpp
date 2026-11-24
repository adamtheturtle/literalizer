#include <cstddef>
#include <string>
#include <utility>
#include <variant>
#include <vector>
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
