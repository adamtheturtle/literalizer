#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::variant<int, std::string>>>>{
    {"first", std::vector<std::vector<std::variant<int, std::string>>>{std::vector<std::variant<int, std::string>>{1, "value"}, std::vector<std::variant<int, std::string>>{}}},
    {"second", std::vector<std::vector<std::variant<int, std::string>>>{std::vector<std::variant<int, std::string>>{}, std::vector<std::variant<int, std::string>>{2, "other"}}},
};
    (void)my_data;
    return 0;
}
