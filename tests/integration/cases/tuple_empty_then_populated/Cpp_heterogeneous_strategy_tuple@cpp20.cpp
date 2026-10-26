#include <cstddef>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<int, std::vector<std::nullptr_t>>>, std::vector<std::variant<int, std::vector<int>>>>>{
    std::vector<std::variant<int, std::vector<int>>>{1, std::vector<int>{}},
    std::vector<std::variant<int, std::vector<int>>>{2, std::vector<int>{3}},
};
    (void)my_data;
    return 0;
}
