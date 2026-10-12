#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>, std::vector<std::variant<std::vector<std::nullptr_t>, std::tuple<int, std::string>>>>>{
    {"first", std::vector<std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>{std::make_tuple(1, "value"), std::vector<std::nullptr_t>{}}},
    {"second", std::vector<std::variant<std::vector<std::nullptr_t>, std::tuple<int, std::string>>>{std::vector<std::nullptr_t>{}, std::make_tuple(2, "other")}},
};
    (void)my_data;
    return 0;
}
