#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<int>>>>{
    {"a", std::vector<std::variant<int, std::vector<int>>>{1, std::vector<int>{2}, std::vector<int>{2}}},
};
    (void)my_data;
    return 0;
}
