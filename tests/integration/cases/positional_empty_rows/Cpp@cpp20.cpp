#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::vector<std::variant<int, std::string>>>>{
    std::vector<std::vector<std::variant<int, std::string>>>{std::vector<std::variant<int, std::string>>{1, "value"}, std::vector<std::variant<int, std::string>>{}},
    std::vector<std::vector<std::variant<int, std::string>>>{std::vector<std::variant<int, std::string>>{}, std::vector<std::variant<int, std::string>>{2, "other"}},
};
    (void)my_data;
    return 0;
}
