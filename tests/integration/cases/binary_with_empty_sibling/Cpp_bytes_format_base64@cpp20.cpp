#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::string, std::vector<std::nullptr_t>>>{
    "SGVsbG8=",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
