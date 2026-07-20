#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<int>>>>{
    {"lint", std::vector<std::variant<int, std::vector<int>>>{2, std::vector<int>{1}}},
    {"test", std::vector<std::variant<int, std::vector<int>>>{5, std::vector<int>{7}}},
};
    (void)my_data;
    return 0;
}
