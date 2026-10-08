#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::map<std::string, int>>, std::vector<std::vector<int>>>>{
    {"a", std::vector<std::map<std::string, int>>{std::map<std::string, int>{}, std::map<std::string, int>{{"x", 1}}}},
    {"b", std::vector<std::vector<int>>{std::vector<int>{}, std::vector<int>{1}}},
};
    (void)my_data;
    return 0;
}
