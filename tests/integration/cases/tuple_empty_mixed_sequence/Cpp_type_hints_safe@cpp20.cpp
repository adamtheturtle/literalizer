#include <cstddef>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::vector<std::variant<int, std::string>>, std::vector<int>>>{
    std::vector<std::nullptr_t>{},
    std::vector<std::variant<int, std::string>>{1, "value"},
    std::vector<int>{2, 3},
};
    (void)my_data;
    return 0;
}
