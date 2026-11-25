#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::vector<int>>, std::vector<std::vector<std::string>>>>{
    {"a", std::vector<std::vector<int>>{std::vector<int>{1}, std::vector<int>{2}}},
    {"b", std::vector<std::vector<std::string>>{std::vector<std::string>{"x"}, std::vector<std::string>{"y"}}},
};
    (void)my_data;
    return 0;
}
