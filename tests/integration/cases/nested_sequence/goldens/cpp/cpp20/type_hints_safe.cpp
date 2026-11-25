#include <cstddef>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<bool, std::string, std::vector<int>, std::nullptr_t>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
    (void)my_data;
    return 0;
}
