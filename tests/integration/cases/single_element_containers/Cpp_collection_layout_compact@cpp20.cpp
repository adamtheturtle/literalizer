#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::map<std::string, std::nullptr_t>>, std::vector<std::vector<int>>, std::vector<std::vector<std::vector<int>>>>>{
    {"single_map", std::vector<std::map<std::string, std::nullptr_t>>{std::map<std::string, std::nullptr_t>{}}},
    {"single_list", std::vector<std::vector<int>>{std::vector<int>{1}}},
    {"single_deep", std::vector<std::vector<std::vector<int>>>{std::vector<std::vector<int>>{std::vector<int>{2}}}},
};
    (void)my_data;
    return 0;
}
