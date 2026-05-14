#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::string, std::vector<std::nullptr_t>>>{
    "48656c6c6f",
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::variant<std::string, std::vector<std::nullptr_t>>>{
    "48656c6c6f",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
