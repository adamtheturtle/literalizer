#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, std::map<std::string, std::vector<int>>, std::vector<std::variant<int, std::string>>>>{
    {"numbers", std::vector<int>{1, 2}},
    {"nested", std::map<std::string, std::vector<int>>{{"inner", std::vector<int>{3}}}},
    {"mixed", std::vector<std::variant<int, std::string>>{4, "five"}},
};
    (void)my_data;
    return 0;
}
