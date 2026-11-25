#include <cstddef>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::string, std::vector<std::nullptr_t>>>{
    "SGVsbG8=",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
