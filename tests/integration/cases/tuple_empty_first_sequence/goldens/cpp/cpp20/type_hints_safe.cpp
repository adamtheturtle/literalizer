#include <cstddef>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::vector<std::variant<int, std::string>>>>{
    std::vector<std::variant<int, std::string>>{},
    std::vector<std::variant<int, std::string>>{1, "value"},
    std::vector<std::variant<int, std::string>>{2, "other"},
};
    (void)my_data;
    return 0;
}
