#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<std::map<std::string, int>, std::map<std::string, std::nullptr_t>, int>>, std::vector<std::variant<std::map<std::string, int>, std::map<std::string, std::string>, int>>, std::vector<std::map<std::string, std::variant<int, std::nullptr_t>>>, std::vector<std::map<std::string, std::variant<int, std::string>>>>>{
    std::vector<std::variant<std::map<std::string, int>, std::map<std::string, std::nullptr_t>, int>>{std::map<std::string, int>{{"a", 1}}, std::map<std::string, std::nullptr_t>{{"a", nullptr}}, 42},
    std::vector<std::variant<std::map<std::string, int>, std::map<std::string, std::string>, int>>{std::map<std::string, int>{{"a", 1}}, std::map<std::string, std::string>{{"a", "s"}}, 42},
    std::vector<std::map<std::string, std::variant<int, std::nullptr_t>>>{std::map<std::string, std::variant<int, std::nullptr_t>>{{"a", 1}}, std::map<std::string, std::variant<int, std::nullptr_t>>{{"a", nullptr}}},
    std::vector<std::map<std::string, std::variant<int, std::string>>>{std::map<std::string, std::variant<int, std::string>>{{"a", 1}}, std::map<std::string, std::variant<int, std::string>>{{"a", "s"}}},
};
    (void)my_data;
    return 0;
}
